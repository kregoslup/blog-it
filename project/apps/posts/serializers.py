from rest_framework import serializers

from project.apps.posts.models import Post, Commit


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('title', 'created', 'updated', 'body', 'blog', 'author')


class CommitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Commit
