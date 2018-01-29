from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Necessary fields: username, password, email, first_name, last_name.
    Overriden so that email is required.
    """
    email = models.EmailField('email address')


class Post(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def likes(self):
        return Like.objects.filter(post=self.id).count()

    class Meta:
        ordering = ('pk', )


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='post_likes')
