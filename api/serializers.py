from rest_framework import permissions
from rest_framework import serializers
from .models import Post, User


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ('url', 'id', 'title', 'body', 'likes', 'created', 'author')


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True,
                                                view_name='post-detail',
                                                read_only=True)
    password = serializers.CharField(min_length=8, max_length=128,
                                     write_only=True)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'first_name', 'last_name',
                  'posts', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
