import requests
from yandex import YaUploader
from pprint import pprint
from datetime import datetime
import json

with open('token_vk.txt', 'r') as file_object:
    token_vk = file_object.read().strip()

with open('token_ya.txt', 'r') as file_object:
    token_ya = file_object.read().strip()

userid = '552934290'
# ts = int("1284101485")

## Задание:
# Нужно написать программу, которая будет:
# 1. Получать фотографии с профиля. Для этого нужно использовать метод [photos.get](https://vk.com/dev/photos.get).
# 2. Сохранять фотографии максимального размера(ширина/высота в пикселях) на Я.Диске.
# 3. Для имени фотографий использовать количество лайков.
# 4. Сохранять информацию по фотографиям в json-файл с результатами.

# vk_user_id = str(input("Введите id пользователя: "))
URL = 'https://api.vk.com/method/photos.get'
params = {
    'user_id': userid,
    'album_id': 'profile',
    'extended': 1,
    'photo_sizes': 1,
    'access_token': token_vk,
    'v': '5.130',
    # 'fields': 'education, sex'
}
res = requests.get(URL, params=params, verify=False)
pprint(res.json())
photos = res.json()['response']['items']
# pprint(photos)
urls = []
photo_json = {}
photos_json = []
# date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
# обрабатываем каждую фотографию
for i in range(len(photos)):
    # берём ссылку на максимальный размер фотографии
    photo_url = str(photos[i]['sizes'][len(photos[i]['sizes']) - 1]['url'])
    likes_count = photos[i]['likes']['count']
    photo_size = str(photos[i]['sizes'][len(photos[i]['sizes']) - 1]['type'])
    ts = (photos[i]['date'])
    date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
    photo_json['file_name'] = f'{likes_count}-{date}.jpg'
    photo_json['size'] = photo_size
    # j = photo_json.json()
    # photos_json = [value for value in photo_json.values() if isinstance(value, dict) ]
    # photos_json.append(photo_json)
    with open('users.json', 'a') as outfile:
        json.dump(photo_json, outfile)
    
    # urls.append(photo_url)
    # pprint(photo_json)
    # pprint(photos_json)
    # pprint(urls)
# with open('users.json', encoding = "utf-8") as f:
#     data = json.load(f)
#     pprint(data)
print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

# ya = YaUploader(token=token_ya)
# ya.upload_file_to_disk("D:/IT/Python/netology/Full_Course/requests/test.txt")













# if you encounter a "year is out of range" error the timestamp
# may be in milliseconds, try ts /= 1000 in that case






# for i in res.json()['response']['items']:
#     # pprint(i)
#     # В каждой фото вытаскиваем список размеров
#     for f in i['sizes']:
#         size = f['height'] * f['width']
#         sizes_list.append([f['url'], size])
#         pprint(sizes_list)
    # max_size.append(max(sizes_list[1]))
    # pprint(max_size)

# v = list(res.json.values())
# k = list(res.json.keys())
# best_hero = k[v.index(max(v))]
# print(f'Самый умный супергерой: {best_hero}')
# pprint(res.json())
#


# class VkUser:
#     url = 'https://api.vk.com/method/'
#
#     def __init__(self, token, version):
#         self.token = token
#         self.version = version
#         self.params = {
#             'user_id': '552934290',
#             'access_token': self.token,
#             'v': self.version
#         }
#         self.owner_id = requests.get(self.url + 'users.get', self.params).json()['response'][0]['id']
#
#     def get_followers(self, user_id=None):
#         if user_id is None:
#             user_id = self.owner_id
#         followers_url = self.url + 'users.getFollowers'
#         followers_params = {
#             'count': 1000,
#             'user_id': user_id
#         }
#         res = requests.get(followers_url, params={**params, **followers_params})
#         return res.json()
#
#     def get_groups(self, user_id=None):
#         if user_id is None:
#             user_id = self.owner_id
#         groups_url = self.url + 'groups.get'
#         groups_params = {
#             'count': 1000,
#             'user_id': user_id,
#             'extended': 1,
#             'fields': 'members_count'
#         }
#         res = requests.get(groups_url, params={**params, **groups_params})
#         return res.json()
#
#     # In[13]:
#
#
# # получим свои группы
# vk_client = VkUser(token, '5.130')
# vk_client.get_groups(552934290)
