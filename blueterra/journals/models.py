from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField(
        upload_to='uploads/',
        storage=S3Boto3Storage(
            bucket_name='mybucket',
            endpoint_url='https://f30c97b5e92eb15944ca7c0536b63e54.r2.cloudflarestorage.com'
        )
    )

    def __str__(self):
        return self.name






from django.db import models

# Create your models here.



class BlogPost(models.Model):
    title = models.TextField()
    slug = models.TextField(unique=True)
    meta_title = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    category_name = models.TextField()
    blog_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    # preview_image = models.ImageField(blank=True, null=True)
    preview_image = models.FileField(
        upload_to='uploads/',
        storage=S3Boto3Storage(
            bucket_name='mybucket',
            endpoint_url='https://f30c97b5e92eb15944ca7c0536b63e54.r2.cloudflarestorage.com'
        )
    )

    def __str__(self):
        return f'{self.title} {self.pk}' 



class BlogCategory(models.Model):
    category = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)


    def __str__(self):
        return self.category


