import requests
from botconf import (
    ADDRESS, NUMBER_OF_USERS, MAX_LIKES_PER_USER, MAX_POSTS_PER_USER, person,
    text,
)
from random import randint

users = {}
posts = 0

for i in range(NUMBER_OF_USERS):
    user = {
        'username': person.username(),
        'password': person.password(8),
        'email': person.email()
    }
    payload = user
    response = requests.post(ADDRESS + 'users/', data=payload)
    print(response.content)

    payload = {
        'username': user.get('username'),
        'password': user.get('password')
    }
    response = requests.post(ADDRESS + 'jwt-auth/', data=payload)
    print(response.content)

    user['token'] = response.json().get('token')

    for j in range(randint(0, MAX_POSTS_PER_USER + 1)):
        payload = {
            'title': text.title(),
            'body': text.text(5)
        }
        headers = {'Authorization': 'JWT {}'.format(user['token'])}
        response = requests.post(ADDRESS + 'posts/', data=payload,
                                 headers=headers)
        print(response.content)
        posts += 1

    users[str(i)] = user

for user in users:
    for _ in range(randint(0, MAX_LIKES_PER_USER)):
        headers = {'Authorization': 'JWT {}'.format(users[user]['token'])}
        response = requests.get(ADDRESS + 'posts/{}/like'
                                .format(randint(1, posts + 1)),
                                headers=headers)
        print(response.content)
