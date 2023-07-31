from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
from .models import UploadedFile
import boto3
from io import BytesIO
import requests 
from django.http import Http404, HttpResponse
from django.http import JsonResponse



def page2(request):
    # Get the latest uploaded file details from the database
    latest_file = UploadedFile.objects.latest('id')
    
    # Send the file URL as a JSON response
    return JsonResponse({'s3_url': latest_file.s3_url})


def generate_presigned_url(bucket_name, object_name, expiration=3600):
        s3_client = boto3.client('s3')
        try:
            response = s3_client.generate_presigned_url('put_object',
                                                     Params={'Bucket': bucket_name,
                                                             'Key': object_name,
                                                            },
                                                     ExpiresIn=expiration,)
        except Exception as e:
            print("Error generating pre-signed URL:", e)
            return None
        
        return response
    
def upload_file_to_s3(url, file_content):
        try:
            print('n tryy')
            response = requests.put(url, data=BytesIO(file_content))
            print('responseee  : ',response)
                
            if response.status_code == 200:
                print("File uploaded successfully!")
                return True
            else:
                print(f"Failed to upload file. Response status code: {response.status_code}")
                print(response.text)
                return False
        except Exception as e:
            print("Error uploading file:", e)
            return False
        
        
@csrf_exempt  # Add the csrf_exempt decorator to the view
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        file_name = request.POST['file_name']
        file_description = request.POST['file_description']

        # Ensure file is read in binary mode (bytes-like object)
        file_content = file.read()
        
        # object_name = os.path.basename(file_path)
        presigned_url = generate_presigned_url('django-project-s3', file_name)
    
        if presigned_url: 
            # Upload the file to S3 using the presigned URL
            
            upload_result = upload_file_to_s3(presigned_url,file_content)
            if upload_result:
                print("File upload process completed successfully.")
            else:
                print("File upload process failed.")
                return None
        else:
            print("Presigned URL generation failed.")
            return None

        return redirect('page2')
    return render(request, 'page1.html')



