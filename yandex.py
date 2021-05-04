import requests
from datetime import datetime, time
import time
from tqdm import tqdm
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
MY_FILE = os.path.join(APP_DIR, 'token_ya.txt')

with open(MY_FILE) as file:
    token_ya = file.read().strip()


class YaUploader:

    def __init__(self):
        self.token = token_ya
        self.host = 'https://cloud-api.yandex.net/v1/disk'

    def _api_request(self, http_method, api_method, headers, params, response_type):
        response = ''
        try:
            response = requests.request(http_method, f'{self.host}/{api_method}', headers=headers, params=params)
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

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, disk_file_path):
        # upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        api_method = 'resources/upload'
        http_method = 'get'
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response_type = 'json'
        response = self._api_request(http_method, api_method, headers, params, response_type)
        return response.json()

    def create_folder(self):
        api_method = 'resources'
        http_method = 'put'
        headers = self.get_headers()
        dirname = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        dirname = f'VK{dirname}'
        params = {"path": dirname}
        response_type = 'json'
        response = self._api_request(http_method, api_method, headers, params, response_type)
        timestamp = datetime.now().strftime('[%H:%M:%S %d-%m-%Y]:')
        if response.status_code == 201:
            with open('upload_log.txt', 'a', encoding='utf-8') as logfile:
                logfile.write(f'{timestamp} Папка {dirname} успешно создана!\n')
        return dirname

    def upload_file_to_disk(self, name_url):
        directory = self.create_folder()
        for key, value in tqdm(name_url.items()):
            # получаем ссылку для загруски на диск
            href = self._get_upload_link(f"{directory}/{key}").get("href", "")
            # считываем файл по ссылке
            r = requests.get(value)
            image_data = r.content
            # загружаем файл на яндекс диск
            response = requests.put(href, data=image_data)
            response.raise_for_status()
            timestamp = datetime.now().strftime('[%H:%M:%S %d-%m-%Y]:')
            if response.status_code == 201:
                with open('upload_log.txt', 'a', encoding='utf-8') as logfile:
                    logfile.write(f'{timestamp} Файл {key} успешно загружен!\n')
            else:
                message = 'Что-то пошло не так!'
                print(message)
                with open('upload_log.txt', 'a') as logfile:
                    logfile.write(f'{timestamp} Ошибка {response.status_code} при загрузке {key}!\n')
            time.sleep(1)
        print('Загрузка завершена!')
