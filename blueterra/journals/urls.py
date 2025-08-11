



from django.urls import path,include

from .views import *


# router = DefaultRouter()
# router.register(r'journals', BlogPostViewSet, basename='blogpost')

urlpatterns = [
   path('hello/', hello_api, name='grettings'),
    path('journals/', BlogPostAPIView.as_view(), name='create-blog'),
     path('journals/<int:pk>/', BlogPostDetailAPIView.as_view(), name='blog-detail'),
    path('journal-categories/', BlogCategoryAPIView.as_view(), name='categories'),

   path('get-journal-categories/', get_journal_categories, name='get_journal_categories'),
   path('get-journals/', get_journals, name='get_journals'),
   path('get-featured-journals/', get_featured_journals, name='get_featured_journals'),
 path('upload-blog-image/', UploadBlogImageView.as_view(), name='upload-blog-image'),


    

]