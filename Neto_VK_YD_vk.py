import requests


class VkRequest:
    url_base = 'https://api.vk.com/method/'

    def __init__(self, vk_token, version):
        self.params = {
            'access_token': vk_token,
            'v': version
        }

    def get_photos(self, vk_id, count=5):
        """ Get list of links to photo, name of photos and type of size """
        method = 'photos.get'
        album_id = 'profile'
        get_photos_url = self.url_base + method
        get_photos_params = {
            'owner_id': vk_id,
            'album_id': album_id,
            'extended': 1,
            'photo_sizes': 0,
            'count': count
        }
        res = requests.get(get_photos_url, params={**self.params, **get_photos_params}).json()
        info_list = []

        # Check for errors from VK API:
        if 'error' in res:
            print(f"<{res['error']['error_msg']}>")
            return info_list

        for i, photo in enumerate(res['response']['items']):
            num_likes = photo['likes']['count']

            # Сalculate and choose the maximum size:
            if photo['sizes'][0]['height']:
                link = max(photo['sizes'], key=lambda _: _['height'] * _['width'])['url']
                type_size = max(photo['sizes'], key=lambda _: _['height'] * _['width'])['type']

            # Select the last value if the exact size is not specified:
            else:
                link = photo['sizes'][-1]['url']
                type_size = photo['sizes'][-1]['type']

            info_list.append({'file_name': f'id{vk_id}_{i + 1}_{num_likes}.jpg', 'type': type_size, 'link': link})
        return info_list
