# starnavi

A simple restful api based social network.

## Prerequisites

What packages you need to install

pip install django, djangorestframework, pyhunter, clearbit, requests, elizabeth

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
