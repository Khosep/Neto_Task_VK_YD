import requests
import datetime as dt


class VkRequest:
    url_base = 'https://api.vk.com/method/'

    def __init__(self, vk_token, version):
        self.params = {
            'access_token': vk_token,
            'v': version
        }

    def get_photos(self, vk_id, count):
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

        likes = set()
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

            # Add the date to the file name if the number of likes is the same
            if num_likes in likes:
                date_photo = dt.datetime.utcfromtimestamp(photo['date']).strftime('%Y-%m-%d')
                info_list.append({'file_name': f'id{vk_id}_{i + 1}_{num_likes}_{date_photo}.jpg',
                                  'type': type_size, 'link': link})
            else:
                info_list.append({'file_name': f'id{vk_id}_{i + 1}_{num_likes}.jpg', 'type': type_size, 'link': link})
                likes.add(num_likes)
        return info_list

    def get_id(self, screen_name):
        """ Get user id by user_name """
        method = 'utils.resolveScreenName'
        get_photos_url = self.url_base + method
        get_id_params = {'screen_name': screen_name}
        res = requests.get(get_photos_url, params={**self.params, **get_id_params}).json()
        if not res['response']:
            vk_id = 0
        elif res['response']['type'] != 'user':
            vk_id = -res['response']['object_id']
        else:
            vk_id = res['response']['object_id']
        return vk_id
