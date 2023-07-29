from django.db import models

# Create your models here.

class UploadedFile(models.Model):
    file_name = models.CharField(max_length=255)
    file_description = models.TextField()
    s3_url = models.URLField()