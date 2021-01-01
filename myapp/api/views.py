from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter,OrderingFilter

from django.contrib.auth.models import User
from myapp.models import *
from myapp.api.serializers import ProfileSerializer,PostSerializer
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework import mixins

class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_field = 'pk'

    def get(self,request,pk=None):
        if pk:
            return self.retrieve(request)
        else:
            return self.list(request)

    @permission_classes((IsAuthenticated,))

    def post(self, request):
        return self.create(request)

    @permission_classes((IsAuthenticated,))

    def put(self, request, pk=None):
        return self.update(request, pk)

    @permission_classes((IsAuthenticated,))

    def delete(self, request, pk=None):
        return self.destroy(request, pk)


@api_view(['GET','POST'])
@permission_classes((IsAuthenticated,))
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(posts,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated,))
def post_detail(request,pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user =request.user
    if post.user!=user:
        return Response({'response':'You are not authorized to edit this post'})
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
