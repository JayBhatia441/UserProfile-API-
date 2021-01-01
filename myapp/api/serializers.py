from rest_framework import serializers
from myapp.models import *
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = Profile
        fields = ['username','name','surname','bio','city','country','age','profile_image']

    def get_username(self,profile):
        username = profile.user.username
        return username


class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')
    class Meta:
        model = Post
        fields = ['username','name','image']

    def get_username(self,post):
        username = post.user.username
        return username
