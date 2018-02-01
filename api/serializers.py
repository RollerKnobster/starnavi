from rest_framework import permissions
from rest_framework import serializers
from .models import Post, User


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """
    A data serializer for post. Specifying what fields are being output on
    response and to send username of an author instead of his pk.
    """
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ('url', 'id', 'title', 'body', 'likes', 'created', 'author')


class UserSerializer(serializers.ModelSerializer):
    """
    A data serializer for post. Specifying what fields are being output on
    response and to list all posts by user, and not to show password.
    """
    posts = serializers.HyperlinkedRelatedField(many=True,
                                                view_name='post-detail',
                                                read_only=True)
    password = serializers.CharField(min_length=8, max_length=128,
                                     write_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'first_name', 'last_name',
                  'posts', 'password')

    def create(self, validated_data):
        """
        Manually overriding the method to behave like an actual user creator 
        including (and most importantly) hashing the password.
        """
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Manually overriding the method only to hash the retrieved password. 
        """
        super(UserSerializer, self).update(instance, validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
