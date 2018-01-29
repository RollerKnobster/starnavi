from django.urls import re_path
from rest_framework_jwt.views import obtain_jwt_token
from . import views

app_name = 'api'

urlpatterns = [
    re_path(r'^$', views.api_root),
    re_path(r'^posts/(?P<pk>[0-9]+)/like/$',
            views.PostViewSet.as_view({'get': 'like'}), name='like'),
    re_path(r'^jwt-auth/$', obtain_jwt_token)
]
