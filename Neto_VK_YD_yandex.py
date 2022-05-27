import requests


class YdiskUploader:
    url_base = 'https://cloud-api.yandex.net'

    def __init__(self, yd_token: str):
        self.token = yd_token
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': f'OAuth {self.token}'}

    def create_folder(self, path_to_disk):
        """ Create a new folder on Yandex disk """
        url = f'{self.url_base}/v1/disk/resources/'
        params = {'path': path_to_disk}
        res = requests.put(url, headers=self.headers, params=params)
        if res.status_code == 201:
            print(f"<Папка '{path_to_disk}' на Яндекс диске создана>")
        elif res.status_code == 409:
            print(f"<Папка '{path_to_disk}' на Яндекс диске существует>")
        return res.status_code

    def upload_by_url(self, path_to_disk, info_list):
        """ Upload photos to Yandex disk by url list """
        self.create_folder(path_to_disk)
        url = f'{self.url_base}/v1/disk/resources/upload/'
        for i, item in enumerate(info_list):
            params = {'path': f'{path_to_disk}/{item["file_name"]}',
                      'url': item['link']}
            del info_list[i]['link']
            res_post = requests.post(url, headers=self.headers, params=params)
            if res_post.status_code == 202:
                print(f'<{i + 1}/{len(info_list)} files uploaded>')
            else:
                print(f'<Ошибка. Код: {res_post.status_code}>')
        return info_list
