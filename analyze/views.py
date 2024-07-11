# analyze/views.py
import requests
from django.shortcuts import render
from .forms import ImageUploadForm
from .models import UploadedImage

FASTAPI_URL = 'http://127.0.0.1:8001/predict/'

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            with open(image_instance.image.path, 'rb') as f:
                response = requests.post(FASTAPI_URL, files={'file': f})
                if response.status_code == 200:
                    try:
                        result = response.json()
                    except requests.exceptions.JSONDecodeError:
                        result = {"error": "Invalid JSON response"}
                else:
                    result = {"error": f"Error from FastAPI server: {response.status_code}"}
                return render(request, 'analyze/result.html', {'result': result, 'image': image_instance})
    else:
        form = ImageUploadForm()
    return render(request, 'analyze/upload.html', {'form': form})

def result_image(request):
    return render(request, 'analyze/result.html')
