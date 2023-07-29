from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.core.files.storage import default_storage

# from aws_project.aws_project.settings import AWS_S3_REGION_NAME, AWS_STORAGE_BUCKET_NAME
from .models import UploadedFile
import boto3
import os
from io import BytesIO 
from dotenv import load_dotenv

load_dotenv()


def page2(request):
    # Get the latest uploaded file details from the database
    latest_file = UploadedFile.objects.latest('id')

    return render(request, 'page2.html', {'s3_url': latest_file.s3_url})




def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        file_name = request.POST['file_name']
        file_description = request.POST['file_description']

        # Ensure file is read in binary mode (bytes-like object)
        file_content = file.read()
        
        print("File Content:", file_content)
        print("File Content Type:", type(file_content))

        bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
        bucket_region = os.getenv('AWS_S3_REGION_NAME')
        
        # Upload file to AWS S3 bucket
        s3 = boto3.client('s3')
        s3_file_path = f"uploaded_files/{file.name}"
        
        
        s3.upload_fileobj(BytesIO(file_content), bucket_name, s3_file_path, ExtraArgs={'ACL': 'public-read'})
        
        # s3.upload_fileobj(file_content, {bucket_name}, s3_file_path, ExtraArgs={'ACL': 'public-read'})

        
        # Save file details in the database
        UploadedFile.objects.create(
            file_name=file_name,
            file_description=file_description,
            s3_url=f"https://{bucket_name}.s3.{bucket_region}.amazonaws.com/{s3_file_path}"
        )

        return redirect('page2')

    return render(request, 'page1.html')