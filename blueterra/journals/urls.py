
from django.urls import path,include

from .views import *

urlpatterns = [
    
   path('hello/', hello_api, name='grettings'),
   path('journals/', BlogPostAPIView.as_view(), name='create-blog'),
   path('journals/<int:pk>/', BlogPostDetailAPIView.as_view(), name='blog-detail'),
   path('journal-categories/', BlogCategoryAPIView.as_view(), name='categories'),
   path('journal-categories/<int:pk>/', BlogCategoryAPIView.as_view(), name='categories'),

   path('get-journal-categories/', get_journal_categories, name='get_journal_categories'),
   path('get-journals/', get_journals, name='get_journals'),
   path('get-featured-journals/', get_featured_journals, name='get_featured_journals'),
   path('upload-blog-image/', UploadBlogImageView.as_view(), name='upload-blog-image'),
   path('blog/<slug:slug>/', blog_detail, name='blog-detail'),

   path('get-related-journals/', get_related_journals, name='get_related_journals'),

   path('get-five-journals/', get_five_journals, name='get_five_journals'),

]
