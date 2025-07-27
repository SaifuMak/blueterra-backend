from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import *
from .serializers import *
from .paginations import *
# Create your views here.

from rest_framework.response import Response
from rest_framework.decorators import api_view
# from rest_framework.parsers import MultiPartParser, FormParser

@api_view(['GET'])
def hello_api(request):
    return Response({"message": "Hello from Django!"})


class BlogPostAPIView(APIView):
    # parser_classes = [MultiPartParser, FormParser] 
     
    def get(self, request):

        status_param = request.query_params.get('status')

        blogs = BlogPost.objects.all().order_by('-created_at')
        # serializer = BlogPostSerializer(blogs, many=True)
        if status_param == 'Published':
            blogs = blogs.filter(is_published=True)
        else:
            blogs = blogs.filter(is_published=False)


        paginator = GeneralPagination()
        result_page = paginator.paginate_queryset(blogs, request)
        serializer = BlogPostSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
    
        return Response(serializer.data, status= status.HTTP_200_OK)
     
    def post(self, request):
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Blog post created successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request):
        print(request.data)
        # return Response({"error": "Blog is not selected."}, status=status.HTTP_400_BAD_REQUEST)

        blog_id = request.data.get("id")
        if not blog_id:
            return Response({"error": "Blog is not selected."}, status=status.HTTP_400_BAD_REQUEST)

        blog = get_object_or_404(BlogPost, pk=blog_id)

        # If only is_published is being updated
        if "status" in request.data and len(request.data) == 2:
            if  request.data["status"] == 'publish':
                blog.is_published = True
            else:
                blog.is_published =  False
            blog.save()
            return Response({"message": "Publish status updated successfully."}, status=status.HTTP_200_OK)
        

        # manage the faetured status of the blog 
        if "featured_status" in request.data and len(request.data) == 2:
            blog.is_featured = not blog.is_featured
            blog.save()
            return Response({"message": "Featured status updated successfully."}, status=status.HTTP_200_OK)

        # Otherwise handle normal updates (title, content, etc.)
        serializer = BlogPostSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Blog post updated successfully!', 'data': serializer.data}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   


class BlogPostDetailAPIView(APIView):
    
    def get(self, request, pk):

        print('entered the blog details -------------------------')

        try:
            blog = get_object_or_404(BlogPost, pk=pk)
            serializer = BlogPostSerializer(blog)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
    
    def delete(self, request, pk):
        blog = get_object_or_404(BlogPost, pk=pk)
        blog.delete()
        return Response({"message": "Journal deleted successfully"}, status=status.HTTP_200_OK)



class BlogCategoryAPIView(APIView):
     
    def get(self, request):
        blogs = BlogCategory.objects.all().order_by('-created_at')
        serializer = BlogCategorySerializer(blogs, many=True)
        return Response(serializer.data, status= status.HTTP_200_OK)
     
    def post(self, request):
        serializer = BlogCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Category created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def get_journal_categories(request):
    blogs = BlogCategory.objects.all()
    serializer = BlogCategoryUserSerializer(blogs, many=True)
    return Response(serializer.data, status= status.HTTP_200_OK)


@api_view(['GET'])
def get_journals(request):

    category = request.query_params.get('category')
    blogs = BlogPost.objects.all().filter(is_published=True).order_by('-created_at')
    if category and category != 'View All':
        blogs = blogs.filter(category_name = category)

    paginator = JournalPagination()
    result_page = paginator.paginate_queryset(blogs, request)
    serializer = BlogsUserSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)



@api_view(['GET'])
def get_featured_journals(request):

    blogs = BlogPost.objects.all().filter(is_featured =True)[:3]
   
    serializer = FeaturedBlogsUserSerializer(blogs, many=True)






