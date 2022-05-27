import json
import configparser
from Neto_VK_YD_vk import VkRequest
from Neto_VK_YD_yandex import YdiskUploader


VK_VERSION = '5.131'

config = configparser.ConfigParser()
config.read('tokens.ini')
vk_token = config['VK']['vk_token']
yd_token = config['YD']['yd_token']


def write_info_file(info_list):
    """ Write a file in json format """
    with open('info_file.json', 'w', encoding='utf-8') as f:
        json.dump(info_list, f, ensure_ascii=False, indent=4)
    print("<Файл 'info_file.json' сохранен>")


if __name__ == '__main__':
    vk_item = VkRequest(vk_token, VK_VERSION)
    vk_id = input('Введите id или screen_name VK: ')
    try:
        int(vk_id)
    except ValueError:
        vk_id = vk_item.get_id(vk_id)               # if it is a screen_name
    count = int(input('Введите количество загружаемых фото: '))

    info_list = vk_item.get_photos(vk_id, count)
    if info_list:
        path_to_disk = f'VK_Photo_{vk_id}'          # target folder on Yandex disk
        yd_uploader = YdiskUploader(yd_token)
        info_list = yd_uploader.upload_by_url(path_to_disk, info_list)
        write_info_file(info_list)
    else:
        print(f'<Фото не обнaружено>')
