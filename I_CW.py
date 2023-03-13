# Уважаемые проверяющие!
#  Прошу прщения!
# Ввиду отсутствия времени направляю на проверку "сырую" версию курсовой работы.
# Выполнены не все условия, указанные в ДАНО, но работает!!!
# Прошу Вас вернуть на доработку.


import requests
from pprint import pprint
from tqdm import tqdm
import time


class YaDisk:
    host = 'https://cloud-api.yandex.net:443'

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}

    # создание папки на Я-диске
    def create_folder(self, folder):
        url = f'{self.host}/v1/disk/resources'
        params = {'path': folder}
        response = requests.put(url, headers = self.get_headers(), params=params)
        pprint(response.json())

    # Получение содержимого с Я-диска
    def get_files_list(self):
        url = f'{self.host}/v1/disk/resources/files/'
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        bar()
        pprint(response.json())
        print(response.status_code)

    # Получение ссылки для загрузки
    def get_upload_link(self, disk_file_name):
        url = f'{self.host}/v1/disk/resources/upload/'
        params = {'path': f'/{disk_file_name}'}
        response = requests.get(url, headers=self.get_headers(), params=params)
        print(response.json())
        print(response.status_code)
        return response.json()['href']

    # Загрузка на Я-диск
    def upload_file(self, local_file_name, disk_file_name):
        upload_link = self.get_upload_link(disk_file_name)
        # headers = self.get_headers()
        response = requests.put(upload_link, headers=self.get_headers(), data=open(local_file_name, 'rb'))
        print(response.status_code)
        # print(response.status_code)
        if response.status_code == 201:
            print('OK')

    # Загрузка на Я-диск из интеренета
    def upload_from_internet(self, file_url, file_name, folder):
        url = f'{self.host}/v1/disk/resources/upload/'
        params = {'path': f'/{folder}/{file_name}', 'url': file_url}

        response = requests.post(url, headers=self.get_headers(), params=params)
        # print(response.status_code)
        if response.status_code == 202:
            print(f'Загрузка файла "{file_name}" прошла успешно!')


# Токен в ВК
with open('D:/Учеба/Нетология 2022/VK_токен/Токен_vk.txt', encoding='utf-8') as file:
    access_token = file.readline().rstrip()

# Ввод id
user_id = '421795508'
# vk = VK(access_token, user_id)
# pprint(vk.users_info())


# Запрос photos.get на ВК
URL = 'https://api.vk.com/method/photos.get'
params = {
    # 'user_ids': '421795508',
    'access_token': access_token, # токен и версия api являются обязательными параметрами во всех запросах к vk
    'v':'5.131',
    'owner_id': user_id,
    'album_id': 'wall',
    'extended': '1'
    # 'photo_sizes': '0'
}

# dict_new = {}
# Готовим пустые списки для хранения ЛАЙКОВ, ДАТ и ссылок на фото
list_likes = []
list_date = []
list_url = []


# Итерируемся по результату запроса для создания спискок для хранения ЛАЙКОВ, ДАТ и ссылок на фото
res = requests.get(URL, params=params)
# pprint(res.json())
dict_ = res.json()
for k, v in tqdm(dict_.items()):
    time.sleep(0.3)
    # print(k)
    # print()
    # print(v)
    # print()
    for k1, v1 in v.items():
        # pprint(k1)
        # print(v1)

        if k1 == 'items':
            for k2 in v1:
                # print(k2)
                for k3, v3 in k2.items():
                    # pprint(k3)
                    if k3 == 'likes':
                        for k4, v4 in v3.items():
                            # print(k4)

                            if k4 == 'count':
                                # print(v4)
                                list_likes.append(v4)
                    if k3 == 'date':
                        # print(v3)
                        list_date.append(v3)

                    # Максимальная площадь  = ширина * высоту картинки
                    sq_max = 0
                    h_max = 0
                    w_max = 0
                    url_max = ""

                    if k3 == 'sizes':
                        for k5 in v3:
                            # print(len(v3))
                            # print(k5)
                            for k6, v6 in k5.items():
                                if k6 == 'url':
                                    u = v6
                                if k6 == 'height':
                                    h = v6
                                if k6 == 'width':
                                    w = v6
                            if w * h > sq_max:
                                sq_max = w * h
                                w_max = w
                                h_max = h
                                url_max = u
                            # print(sq_max)
                        list_url.append([url_max, h_max, w_max])


# Готовы  списки для хранения ЛАЙКОВ, ДАТ и ссылок на фото
print('Список с ЛАЙКАМИ:', list_likes)
# Тут НЕОБХОДИМО добавить проверку на равенство ЛАЙКОВ и тогда добавить ДАТУ
# print(list_date)
print('Список ссылок с размерами:')
pprint(list_url)


# Открываем ЯНДЕКС ТОКЕН
with open('D:/Учеба/Нетология 2022/Яндекс токен/Токен с Полигон.txt', encoding='utf-8') as file:
    TOKEN = file.readline().rstrip()

# Создаем папку на Я-диске
yadisk = YaDisk(TOKEN)
yadisk.create_folder('new_folder')

# Итерируемся по СПИСКУ ЛАЙКОВ и ССЫЛОК и записываем на Я-диск
for i in range(len(list_likes)):
    file_url = list_url[i]
    name_ = list_likes[i]
    yadisk.upload_from_internet(file_url, f'{name_}.jpg', 'new_folder')

