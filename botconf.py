import json
from elizabeth import Personal, Text

person = Personal('en')
text = Text('en')
ADDRESS = 'http://127.0.0.1:8000/api/'

try:
    inf = open('config.json')
    with inf:
        values = json.load(inf)
        NUMBER_OF_USERS = values.get('number_of_users', 5)
        MAX_POSTS_PER_USER = values.get('max_posts_per_user', 5)
        MAX_LIKES_PER_USER = values.get('max_likes_per_user', 5)
except:
    NUMBER_OF_USERS = 5
    MAX_POSTS_PER_USER = 5
    MAX_LIKES_PER_USER = 5
