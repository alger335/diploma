import requests
from yandex import YaUploader
from pprint import pprint
from datetime import datetime
import json

with open('token_vk.txt', 'r') as file_object:
    token_vk = file_object.read().strip()

with open('token_ya.txt', 'r') as file_object:
    token_ya = file_object.read().strip()


# 1. Для загруженных фотографий нужно создать свою папку.
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
photo_range = int(input("Введите количество фотографий для загрузки(по умолчанию 5): "))

vk_user_id = str(input("Введите id пользователя: "))
URL = 'https://api.vk.com/method/photos.get'
params = {
    'user_id': vk_user_id,
    'album_id': 'profile',
    'extended': 1,
    'photo_sizes': 1,
    'access_token': token_vk,
    'v': '5.130',
}

res = requests.get(URL, params=params)  # , verify=False)
photos = res.json()['response']['items']
urls = []
photo_json = {}
photos_json = []
name_url = {}
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
    urls.append(photo_url)

ya = YaUploader(token=token_ya)
ya.upload_file_to_disk(name_url)
