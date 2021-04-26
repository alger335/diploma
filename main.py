from photos_backup import *
from yandex import *

vk = VKPhotos()
ya = YaUploader()

ya.upload_file_to_disk(vk.get_photos())
