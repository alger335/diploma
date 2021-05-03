import requests
from datetime import datetime
import json
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
# print(APP_DIR)
MY_FILE = os.path.join(APP_DIR, 'token_vk.txt')
with open(MY_FILE) as file_object:
    token_vk = file_object.read().strip()


class VKPhotos:
    URL = 'https://api.vk.com/method/'

    def __init__(self, ):
        self.token = token_vk
        self.version = '5.130'
        self.params = {
            'access_token': token_vk,
            'v': '5.130',
        }

    def get_photos(self, vk_user_id, vk_album_id, photo_range=5):
        # vk_user_id = str(input("Введите id пользователя: "))
        # photo_range = int(input("Введите количество фотографий для загрузки: "))
        name_url = {}
        photos_json = []
        photos_params = {
            'user_id': vk_user_id,
            'album_id': vk_album_id,
            'extended': 1,
            'photo_sizes': 1,
        }
        res = requests.get(self.URL + 'photos.get', params={**self.params, **photos_params})
        res.raise_for_status()
        # print(res.status_code)
        # print(res.json())
        photos = res.json()['response']['items']

        # if res.status_code == 201:
        #     with open('upload_log.txt', 'a', encoding='UTF-8') as logfile:
        #         logfile.write(f'{timestamp} Папка {dirname} успешно создана!\n')
        # обрабатываем каждую фотографию
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
