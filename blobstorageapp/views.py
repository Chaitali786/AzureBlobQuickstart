import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Set up the BlobServiceClient with the connection string
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = 'datacontainer'  # Set a fixed container name or create dynamically

def index(request):
    return render(request, 'blobstorageapp/index.html')

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        upload_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(upload_file.name, upload_file)
        uploaded_file_url = fs.url(filename)

        # Upload to Azure Blob Storage
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

        with open(fs.path(filename), "rb") as data:
            blob_client.upload_blob(data)
        
        return render(request, 'blobstorageapp/upload_file.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'blobstorageapp/upload_file.html')

def download_file(request):
    
    if request.method == 'POST':
        filename = request.POST.get('filename')
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
        download_file_path = os.path.join(settings.MEDIA_ROOT, filename)

        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

        with open(download_file_path, "rb") as download_file:
            response = HttpResponse(download_file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

    # Fetch the list of blob files from the container
    blob_list = [blob.name for blob in blob_service_client.get_container_client(container_name).list_blobs()]

    return render(request, 'blobstorageapp/download_file.html', {'files': blob_list})
