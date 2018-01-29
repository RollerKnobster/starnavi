import requests
import json
from random import randint
from elizabeth import Personal, Text


person = Personal('en')
text = Text('en')
address = 'http://127.0.0.1:8000/api/'
config = {
    'number_of_users': 5,
    'max_posts_per_user': 5,
    'max_likes_per_user': 5
}

with open('config.json') as inf:
    values = json.load(inf)
    config['number_of_users'] = values.get('number_of_users')
    config['max_posts_per_user'] = values.get('max_posts_per_user')
    config['max_likes_per_user'] = values.get('max_likes_per_user')

users = {}
posts = 0

for i in range(config['number_of_users']):
    user = {
        'username': person.username(),
        'password': person.password(8),
        'email': person.email()
    }
    payload = user
    response = requests.post(address + 'users/', data=payload)
    print(response.content)

    payload = {
        'username': user.get('username'),
        'password': user.get('password')
    }
    response = requests.post(address + 'jwt-auth/', data=payload)
    print(response.content)

    user['token'] = response.json().get('token')

    for j in range(randint(0, config['max_posts_per_user'] + 1)):
        payload = {
            'title': text.title(),
            'body': text.text(5)
        }
        headers = {'Authorization': 'JWT {}'.format(user['token'])}
        response = requests.post(address + 'posts/', data=payload,
                                 headers=headers)
        print(response.content)
        posts += 1

    users[str(i)] = user

for user in users:
    for _ in range(randint(0, config['max_likes_per_user'])):
        headers = {'Authorization': 'JWT {}'.format(users[user]['token'])}
        response = requests.get(address + 'posts/{}/like'
                                .format(randint(1, posts + 1)),
                                headers=headers)
        print(response.content)
