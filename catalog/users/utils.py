import json
import os


def save_user(name, phone, message):
    data = {'name': name, 'phone': phone, 'message': message}
    users_list = json.load(open(os.path.abspath("catalog/users/users.json"), 'r', encoding='utf-8'))
    users_list.append(data)
    json.dump(users_list, open(os.path.abspath("catalog/users/users.json"), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    print('Информация о клиенте сохранена')