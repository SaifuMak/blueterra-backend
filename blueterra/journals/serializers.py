
from rest_framework import serializers
from .models import *

class BlogPostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d %B %Y', read_only=True)

    class Meta:
        model = BlogPost
        fields = '__all__'


class BlogCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogCategory
        fields = '__all__'




class BlogCategoryUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogCategory
        fields = ['category']


class BlogsUserSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d %B %Y', read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'slug', 'created_at','title', 'blog_content', 'preview_image','category_name', 'image_public_url']


class FeaturedBlogsUserSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d %B %Y', read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id','created_at', 'slug','blog_content','title','preview_image','category_name','meta_title','image_public_url']



