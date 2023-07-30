from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
from .models import UploadedFile
import boto3
from io import BytesIO 
from django.http import Http404, HttpResponse
from django.http import JsonResponse



def page2(request):
    # Get the latest uploaded file details from the database
    latest_file = UploadedFile.objects.latest('id')
    
    # Send the file URL as a JSON response
    return JsonResponse({'s3_url': latest_file.s3_url})


# To resolve the 403 Forbidden error, you can try adding CSRF protection to 
# your Django API views. You can do this by using the @csrf_exempt decorator 
# for the views that handle API requests.


@csrf_exempt    # Add the csrf_exempt decorator to the view
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        file_name = request.POST['file_name']
        file_description = request.POST['file_description']

        # Ensure file is read in binary mode (bytes-like object)
        file_content = file.read()
        
        # Upload file to AWS S3 bucket
        s3 = boto3.client('s3')
        s3_file_path = f"uploaded_files/{file.name}"      
        s3.upload_fileobj(BytesIO(file_content), settings.AWS_STORAGE_BUCKET_NAME , s3_file_path, ExtraArgs={'ACL': 'public-read'})
        
        # Save file details in the database
        UploadedFile.objects.create(
            file_name=file_name,
            file_description=file_description,
            s3_url=f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{s3_file_path}"
        )

        return redirect('page2')
    return HttpResponse("Please use POST method !!!")
    # return render(request, 'page1.html')