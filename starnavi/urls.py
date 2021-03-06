"""starnavi_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import re_path, include
from rest_framework import routers
from api import views
from rest_framework_jwt.views import obtain_jwt_token

router = routers.DefaultRouter()

router.register('users', views.UserViewSet)
router.register('posts', views.PostViewSet)

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/', include(router.urls)),
    re_path(r'^api-auth/$', obtain_jwt_token,),
]
