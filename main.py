from photos_backup import VKPhotos
from yandex import YaUploader

vk = VKPhotos()
ya = YaUploader()

ya.upload_file_to_disk(vk.get_photos('2236706', 'wall', 5))
