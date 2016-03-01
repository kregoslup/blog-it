from rest_framework import serializers
from apps.blog.serializers import UserSerializer, BlogSerializer
from apps.posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    blog = BlogSerializer()
    author = UserSerializer()

    class Meta:
        model = Post
        fields = ('title', 'created', 'updated', 'body', 'blog', 'author')
