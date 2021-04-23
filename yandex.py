import requests
from datetime import datetime, date, time
from pprint import pprint
import time
from tqdm import tqdm


class YaUploader:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        # pprint(response.json())
        return response.json()

    def create_folder(self):
        mkdir_url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        dirname = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        dirname = f'VK{dirname}'
        params = {"path": dirname}
        response = requests.put(mkdir_url, headers=headers, params=params)
        # print(response.json())
        return dirname

    def upload_file_to_disk(self, name_url):
        directory = self.create_folder()
        timestamp = datetime.now().strftime('[%H:%M:%S %d-%m-%Y]:')
        for key, value in name_url.items():
            # print(key)
            # print(value)
            # filename = key
            # получаем ссылку для загруски на диск
            href = self._get_upload_link(f"{directory}/{key}").get("href", "")
            # pprint(href)
            # считываем файл по ссылке
            r = requests.get(value)
            image_data = r.content
            # загружаем файл на яндекс диск
            response = requests.put(href, data=image_data)
            # прогресс-бар
            mylist = [1, 2, 3, 4, 5]
            for i in tqdm(mylist):
                time.sleep(1)
            response.raise_for_status()
            if response.status_code == 201:
                message = f"{timestamp} Файл {key} успешно загружен!"
                print(message)
                with open('upload_log.txt', 'a') as logfile:
                    logfile.write(f'{message}\n')
            time.sleep(1)



#
# mylist = [1,2,3,4,5,6,7,8]
# for i in tqdm(range(len(name_url))):
# for i in tqdm(mylist):
#     time.sleep(1)