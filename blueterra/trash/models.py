from django.db import models

# Create your models here.



class FilePendingDelete(models.Model):
    file_path = models.CharField(max_length=500)  # key in R2 (e.g., "uploads/image.png")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_path