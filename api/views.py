import clearbit
from pyhunter import PyHunter
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from starnavi.settings import CLEARBIT_API_KEY, HUNTER_API_KEY
from .serializers import PostSerializer, UserSerializer
from .models import Post, User, Like


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @detail_route()
    def like(self, request, pk=None):
        """
        API endpoint to like a post.
        """
        post = self.get_object()
        query_result = Like.objects.filter(user=request.user.id, post=post.id)
        if query_result:
            query_result[0].delete()
        else:
            new_row = Like(user=request.user, post=post)
            new_row.save()

        return Response(status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action is 'create':
            self.permission_classes = [AllowAny, ]
        return super(self.__class__, self).get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get('email', {})
        hunter = PyHunter(HUNTER_API_KEY)
        hunter_res = hunter.email_verifier(email)
        if hunter_res.get('result', {}) == 'undeliverable':
            data = {
                'email': ['This email is invalid.']
            }
            return Response(data, status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)

        new_user = User.objects.get(username=request.data['username'])
        if new_user:
            clearbit.key = CLEARBIT_API_KEY
            clear_res = clearbit.Enrichment.find(email=email, stream=True)
            if clear_res is not None:
                name = clear_res['person']['name']
                if name.get('givenName', {}) or name.get('familyName', {}):
                    new_user.first_name = name.get('givenName', '')
                    new_user.last_name = name.get('familyName', '')
                    new_user.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)
