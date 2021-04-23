# 2. Сделать прогресс-бар
# 3. Оформить код в функции и классы
# 4. Поправить photos_json

# Добавить функционал:
# - Сохранять фотографии и из других альбомов.
# - Сохранять фотографии из других социальных сетей. [Одноклассники](https://apiok.ru/) и [Инстаграмм](https://www.instagram.com/developer/)
# - Сохранять фотографии на Google.Drive.

# - сделать удобную менюшку
# - проверка контрольной суммы

# userid = '2236706'  # '552934290'

import requests
from yandex import YaUploader
from pprint import pprint
from datetime import datetime
import json

with open('token_vk.txt', 'r') as file_object:
    token_vk = file_object.read().strip()

with open('token_ya.txt', 'r') as file_object:
    token_ya = file_object.read().strip()


class VKPhotos:
    URL = 'https://api.vk.com/method/'

    def __init__(self, ):
        self.token = token_vk
        self.version = '5.130'
        self.params = {
            # 'user_id': vk_user_id,
            # 'album_id': 'profile',
            # 'extended': 1,
            # 'photo_sizes': 1,
            'access_token': token_vk,
            'v': '5.130',
        }

    def get_photos(self):
        # URL = 'https://api.vk.com/method/photos.get'
        vk_user_id = str(input("Введите id пользователя: "))
        photo_range = int(input("Введите количество фотографий для загрузки(по умолчанию 5): "))
        urls = []
        photo_json = {}
        name_url = {}
        photos_params = {
            'user_id': vk_user_id,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
        }
        res = requests.get(self.URL+'photos.get', params={**self.params, **photos_params})
        photos = res.json()['response']['items']
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
            # формируем словарь с именем файла и размером
            file_name = f'{likes_count}-{date}.jpg'
            photo_json['file_name'] = file_name
            photo_json['size'] = photo_size
            name_url[file_name] = photo_url
            # пишем в json
            with open('photos.json', 'a') as outfile:
                json.dump(photo_json, outfile)
            # собираем список ссылок на фотки
            # urls.append(photo_url)
        return name_url

ya = YaUploader(token=token_ya)
ya.upload_file_to_disk(name_url)
