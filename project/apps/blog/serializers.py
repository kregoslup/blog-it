from rest_framework import serializers

from project.apps.blog.models import User, Blog


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=200, required=True)
    access_token = serializers.CharField(max_length=300, required=True)

    class Meta:
        model = User


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
