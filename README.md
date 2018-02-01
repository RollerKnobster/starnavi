# starnavi

A simple restful api based social network.

## Prerequisites

What packages you need to install

pip install -r requirements.txt

## Deployment

python manage.py makemigrations

python manage.py migrate

python bot.py (MAKE SURE THE DATABASE IS FRESH AND EMPTY, AND THE SERVER IS RUNNING)

python manage.py runserver

## Note on hunter.io and clearbit

Even though Elizabeth generates fake emails, hunter.io still thinks they're legit because it only checks them with a regex and pokes the SMTP server for liveliness. Because of the same reason, clearbit is unable to fetch first and last names for users based on their emails. This is why to check their implementations for correctness you'll have to manually send a request for registering with emails which are clearly fake or broken for hunter, or real for clearbit.

## API endpoints

/api/posts/ ['GET'] — get a list of posts. Requires authentication.

/api/posts/ ['POST'] — create a post. A request should contain the title and body of a post. Requires authentication.

/api/posts/pk/ ['GET'] — get a detailed view for a post. Requires authentication.

/api/posts/pk/ ['PUT'] — update a post. A request should contain the new title and body of a post. Requires authentication. User can only update his own posts.

/api/posts/pk/ ['DELETE'] — delete a post. Requires authentication. User can only delete his own posts.

/api/posts/pk/like/ ['GET'] — like a post. Send again to unlike. Requires authentication.

/api/users/ ['GET'] — get a list of users. Requires authentication.

/api/users/ ['POST'] — register. A request should contain a username, a password and an email. Password must be 8+ characters. Does not require authentication.

/api/users/pk/ ['GET'] — get a detailed view for a user. Requires authentication.

/api/users/pk/ ['PUT'] — update a user. A request should contain the new username, password and email. Password must be 8+ characters. Requires authentication. User can only update his own account.

/api/users/pk/ ['DELETE'] — delete a user. Requires authentication. User can only delete his own account.

/api-auth/ ['POST'] — authorize. A request should contain a username and a password. Send retrieved token with each consequent request. Does not require authentication (duh).

All methods are allowed to superusers/staff.

## Request/Response examples

### Registering a user

Request:
```
{
    url: '127.0.0.1:8000/api/users/',
    method: 'POST',
    data: {
        'username': 'haystack',
        'password': 'stackhay',
        'email': 'hayhay@stack.com'
    }
}
```
Response:
```
{
    status: '200 OK',
    response: {
        "url": "http://127.0.0.1:8000/api/users/1/",
        "username": "haystack",
        "email": "hayhay@stack.com",
        "first_name": "",
        "last_name": "",
        "posts": []
    }
}
```

### Authenticating

Request:
```
{
    url: '127.0.0.1:8000/api-auth/',
    method: 'POST',
    data: {
        'username': 'haystack',
        'password': 'stackhay'
    }
}
```
Response:
```
{
    status: "200 OK",
    response: {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6ImxvdmV0dGEtMTI3NyIsImV4cCI6MTUxNzQ3NjE4NiwiZW1haWwiOiJrZWVsZXlfNzExOUBsaXZlLmNvbSJ9.tz5Xqnj67M0i9fNGAFOsYl-Umc32tXkzVhysJNQZWxU"
    }
}
```

### Creating a post

Request:
```
{
    url: '127.0.0.1:8000/api/posts/',
    method: 'POST',
    data: {
        'title': 'Some title',
        'body': 'Some Body once told me the world is gonna roll me.'
    },
    headers: {
        'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6ImxvdmV0dGEtMTI3NyIsImV4cCI6MTUxNzQ3NjE4NiwiZW1haWwiOiJrZWVsZXlfNzExOUBsaXZlLmNvbSJ9.tz5Xqnj67M0i9fNGAFOsYl-Umc32tXkzVhysJNQZWxU'
    }
}
```
Response:
```
{
    status: "201 CREATED",
    response: {
        "url": "http://127.0.0.1:8000/api/posts/1/",
        "id": 1,
        "title": "Some title",
        "body": "Some Body once told me the world is gonna roll me.",
        "likes": 0,
        "created": "%TIMESTAMP%",
        "author": "haystack"
    }
}
```

### Getting a post

Request:
```
{
    url: '127.0.0.1:8000/api/posts/1/',
    method: 'GET',
    headers: {
        'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6ImxvdmV0dGEtMTI3NyIsImV4cCI6MTUxNzQ3NjE4NiwiZW1haWwiOiJrZWVsZXlfNzExOUBsaXZlLmNvbSJ9.tz5Xqnj67M0i9fNGAFOsYl-Umc32tXkzVhysJNQZWxU'
    }
}
```
Response:
```
{
    status: "200 OK",
    response: {
        "url": "http://127.0.0.1:8000/api/posts/1/",
        "id": 1,
        "title": "Some title",
        "body": "Some Body once told me the world is gonna roll me.",
        "likes": 0,
        "created": "%TIMESTAMP%",
        "author": "haystack"
    }
}
```

### Deleting a post

Request:
```
{
    url: '127.0.0.1:8000/api/posts/1/',
    method: 'DELETE',
    headers: {
        'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6ImxvdmV0dGEtMTI3NyIsImV4cCI6MTUxNzQ3NjE4NiwiZW1haWwiOiJrZWVsZXlfNzExOUBsaXZlLmNvbSJ9.tz5Xqnj67M0i9fNGAFOsYl-Umc32tXkzVhysJNQZWxU'
    }
}
```
Response:
```
{
    status: "204 NO CONTENT",
    response: {
    }
}
```

### Getting a user without authenticating

Request:
```
{
    url: '127.0.0.1:8000/api/users/1/',
    method: 'GET'
}
```
Response:
```
{
    status: "401 UNAUTHORIZED",
    response: {
        'non_field_error': 'Credentials have not been provided for this action.'
    }
}
```

### Trying to update someone else's post

Request:
```
{
    url: '127.0.0.1:8000/api/posts/2/',
    method: 'PUT',
    data: {
        'title': 'New title',
        'body': 'New body'
    },
    headers: {
        'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6ImxvdmV0dGEtMTI3NyIsImV4cCI6MTUxNzQ3NjE4NiwiZW1haWwiOiJrZWVsZXlfNzExOUBsaXZlLmNvbSJ9.tz5Xqnj67M0i9fNGAFOsYl-Umc32tXkzVhysJNQZWxU'
    }
}
```
Response:
```
{
    status: "403 FORBIDDEN",
    response: {
        'detail': 'You do not have permission to perform this action.'
    }
}
```

## Common HTTP errors

400 Bad Request — Most likely you entered an invalid email.
401 Unauthorized — You are trying to perform an action unauthorized, like trying to get a post detail etc.
402 Payment Required — You've exceeded your free requests to ClearBit API.
403 Forbidden — You are trying to perform an action you are not allowed, like deleting someone else's post.
