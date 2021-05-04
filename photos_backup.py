import requests
from datetime import datetime
import json
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
MY_FILE = os.path.join(APP_DIR, 'token_vk.txt')
with open(MY_FILE) as file_object:
    token_vk = file_object.read().strip()


class VKPhotos:

    def __init__(self, ):
        self.token = token_vk
        self.host = 'https://api.vk.com/method/'
        self.version = '5.130'
        self.params = {
            'access_token': token_vk,
            'v': '5.130',
        }

    def _api_request(self, http_method, api_method, params, response_type):
        response = ''
        try:
            response = requests.request(http_method, f'{self.host}/{api_method}', params=params)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
        if response_type == 'json':
            return response

    def get_photos(self, vk_user_id, vk_album_id, photo_range=5):
        name_url = {}
        photos_json = []
        http_method = 'get'
        api_method = 'photos.get'
        response_type = 'json'
        photos_params = {
            'user_id': vk_user_id,
            'album_id': vk_album_id,
            'extended': 1,
            'photo_sizes': 1,
        }
        params = {**self.params, **photos_params}
        res = self._api_request(http_method, api_method, params, response_type)
        photos = res.json()['response']['items']
        for i in range(photo_range):
            # берём ссылку на максимальный размер фотографии
            photo_url = str(photos[i]['sizes'][len(photos[i]['sizes']) - 1]['url'])
            # считаем лайки
            likes_count = photos[i]['likes']['count']
            # смотрим размер фотки
            photo_size = str(photos[i]['sizes'][len(photos[i]['sizes']) - 1]['type'])
            # берем дату публикации фотки
            ts = (photos[i]['date'])
            date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
            # формируем словарь с именем файла и ссылкой
            file_name = f'{likes_count}-{date}.jpg'
            name_url[file_name] = photo_url
            # формируем выходной json
            photos_json.append({'file_name': file_name, 'size': photo_size})
            # пишем в json
        with open('photos.json', 'a') as outfile:
            json.dump(photos_json, outfile)
        return name_url
