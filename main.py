from photos_backup import *
from yandex import *

vk = VKPhotos()
ya = YaUploader(token=token_ya)

ya.upload_file_to_disk(vk.get_photos())
