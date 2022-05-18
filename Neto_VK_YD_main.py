from Neto_VK_YD_vk import VkRequest
from Neto_VK_YD_yandex import YdiskUploader


VK_TOKEN = 'a67f00c673c3d4b12800dd0ba29579ec56d804f3c5f3bbcef5328d4b3981fa5987b951cf2c8d8b24b9abd'
VK_VERSION = '5.131'

# with open('YD_token.txt', 'r') as f:
#     yd_token = f.read().strip()

if __name__ == '__main__':
    vk_id = int(input('Введите id VK: '))
    yd_token = input('Введите токен Яндекс Диска: ')

    vk_item = VkRequest(VK_TOKEN, VK_VERSION)
    info_list = vk_item.get_photos(vk_id, 5)

    if info_list:
        path_to_disk = f'VK_Photo_{vk_id}'          # целевая папка на Яндекс диске
        yd_uploader = YdiskUploader(yd_token)
        info_list = yd_uploader.upload_by_url(path_to_disk, info_list)
        yd_uploader.write_info_file(info_list)
    else:
        print(f'<Фото не обнaружено>')
