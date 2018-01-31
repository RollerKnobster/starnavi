# starnavi

A simple restful api based social network. Check readme file for more info.

### Prerequisites

What things you need to install the software and how to install them

pip install django, djangorestframework, pyhunter, clearbit, requests, elizabeth

## Deployment

python manage.py makemigrations

python manage.py migrate

python bot.py (MAKE SURE THE DATABASE IS FRESH AND EMPTY)

python manage.py runserver

## API endpoints

/api/posts/ ['GET', 'POST']

/api/posts/pk/ ['GET', 'UPDATE', 'DELETE']
  
/api/posts/pk/like/ ['GET']
  
/api/users/ ['GET', 'POST']

/api/users/pk/ ['GET', 'UPDATE', 'DELETE']
  
/api-auth/ ['POST']
