from trash.models import FilePendingDelete
from django.conf import settings
import boto3
from .const import S3_ENDPOINT

def mark_file_for_deletion(file_path: str):
    FilePendingDelete.objects.create(file_path=file_path)

def clean_trash():

    s3 = boto3.client(
        "s3",
        endpoint_url= S3_ENDPOINT,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    files = FilePendingDelete.objects.all()

    for f in files:
        try:
            s3.delete_object(Bucket=bucket_name, Key=f.file_path)
        
            f.delete()  # remove record from DB after deletion
        except Exception as e:
            print({"file": f.file_path, "error": str(e)})

    