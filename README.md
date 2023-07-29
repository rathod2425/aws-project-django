# aws-project-django

## Django Project with minimal UI, uploads a file in s3.

### Usage :
    Create a .env file inside root project

    Create the following variables, 

    AWS_ACCESS_KEY_ID=
    AWS_SECRET_ACCESS_KEY=
    AWS_STORAGE_BUCKET_NAME=
    AWS_S3_REGION_NAME=

    Paste the credentials.

    pip install -r requirements.txt
    python mange.py migrate
    python manage.py runserver
