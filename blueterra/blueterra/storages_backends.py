# storages_backends.py
from storages.backends.s3boto3 import S3Boto3Storage

class R2PublicStorage(S3Boto3Storage):
    # bucket_name = 'mybucket'
    bucket_name = 'blueterra'
    default_acl = 'public-read'
    querystring_auth = False
    # endpoint_url='https://f30c97b5e92eb15944ca7c0536b63e54.r2.cloudflarestorage.com'
    endpoint_url='https://5460cd38eb6302241df51013ad399321.r2.cloudflarestorage.com'

    
