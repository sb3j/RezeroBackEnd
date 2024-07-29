import requests
from django.shortcuts import render, redirect
from .forms import ImageUploadForm, DesignForm
from .models import OrderInfo
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UploadedImageSerializer, DesignRequestSerializer
from rest_framework.views import APIView
import os
from django.core.files.storage import default_storage

FASTAPI_URL = 'http://127.0.0.1:8001/predict/'
DALLE_API_URL = 'https://api.openai.com/v1/images/generations'


from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import OrderInfo
from .serializers import UploadedImageSerializer
from .forms import ImageUploadForm

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import OrderInfo
from .serializers import UploadedImageSerializer
from .forms import ImageUploadForm

class UploadImageView(generics.CreateAPIView):
    queryset = OrderInfo.objects.all()
    serializer_class = UploadedImageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        form = ImageUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            image_instance = form.save(commit=False)
            image_instance.user = request.user
            image_instance.save()

            before_image_url = request.build_absolute_uri(image_instance.image.url)
            image_instance.before_image_url = before_image_url
            image_instance.save()

            with open(image_instance.image.path, 'rb') as f:
                response = requests.post(FASTAPI_URL, files={'file': f})
                if response.status_code == 200:
                    try:
                        result = response.json()
                        image_instance.material = result.get('material', '')
                        image_instance.category = result.get('category', '')
                        image_instance.color = result.get('color', '')
                        image_instance.save()

                        return Response({
                            "message": "Image uploaded and analyzed successfully",
                            "category": result.get('category'),
                            "material": result.get('material'),
                            "color": result.get('color'),
                            "before_image_url": before_image_url,
                            "image_id": image_instance.id
                        }, status=status.HTTP_201_CREATED)

                    except requests.exceptions.JSONDecodeError:
                        return Response({"error": "Invalid JSON response"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error": f"Error from FastAPI server: {response.status_code}"}, status=response.status_code)

        else:
            return Response({"error": "Invalid form data"}, status=status.HTTP_400_BAD_REQUEST)

class RequestDesignView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DesignRequestSerializer

    def post(self, request, *args, **kwargs):
        design_form = DesignForm(request.POST)

        if design_form.is_valid():
            design_data = design_form.cleaned_data
            
            try:
                # 사용자의 최신 업로드 이미지를 가져옴
                image_instance = OrderInfo.objects.filter(user=request.user).latest('uploaded_at')
                
                image_instance.neck_line = design_data.get('neck_line', '')
                image_instance.sleeve_length = design_data.get('sleeve_length', '')
                image_instance.pattern = design_data.get('pattern', '')
                image_instance.pocket = design_data.get('pocket', '')
                image_instance.zip = design_data.get('zip', '')
                image_instance.button = design_data.get('button', '')
                image_instance.addt_design = design_data.get('addt_design', '')
                image_instance.save()

                return Response({"message": "Design request saved successfully"}, status=status.HTTP_201_CREATED)

            except OrderInfo.DoesNotExist:
                return Response({"error": "Image not found or not authorized"}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({"error": "Invalid design form data"}, status=status.HTTP_400_BAD_REQUEST)
        
class DalleResultAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # 사용자의 최신 업로드 이미지를 가져옴
            image_instance = OrderInfo.objects.filter(user=request.user).latest('uploaded_at')
            result = {
                "material": image_instance.material,
                "category": image_instance.category,
                "color": image_instance.color,
            }
            design_data = {
                "neck_line": image_instance.neck_line,
                "sleeve_length": image_instance.sleeve_length,
                "pattern": image_instance.pattern,
                "pocket": image_instance.pocket,
                "zip": image_instance.zip,
                "button": image_instance.button,
                "addt_design": image_instance.addt_design,
            }
            prompt = make_prompt(result, design_data)

            headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
            data = {
                "model": "dall-e-3",
                "prompt": prompt,
                "size": "1024x1024",
                "quality": "standard",
                "n": 1,
            }
            response = requests.post(DALLE_API_URL, headers=headers, json=data)
            if response.status_code == 200:
                image_url = response.json()['data'][0]['url']
                
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    folder_path = os.path.join(settings.MEDIA_ROOT, 'images/after')
                    os.makedirs(folder_path, exist_ok=True)

                    file_name = f"dalle_{image_instance.id}.png"
                    file_path = os.path.join(folder_path, file_name)
                    
                    with open(file_path, 'wb') as f:
                        f.write(image_response.content)
                    
                    image_instance.prompt = prompt
                    after_image_url = request.build_absolute_uri(default_storage.url(os.path.join('images/after', file_name)))
                    image_instance.dalle_image_url = after_image_url
                    image_instance.save()

                    serializer = UploadedImageSerializer(image_instance)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Error downloading the image"}, status=image_response.status_code)
            else:
                return Response({"error": "Error from DALL-E API"}, status=response.status_code)

        except OrderInfo.DoesNotExist:
            return Response({"error": "Image not found or not authorized"}, status=status.HTTP_404_NOT_FOUND)


def make_prompt(result, design_data):
    material = result['material']
    category = result['category']
    color = result['color']
    
    neck_line = design_data['neck_line']
    sleeve_length = design_data['sleeve_length']
    pattern = design_data.get('pattern', 'n/a') if design_data.get('pattern', 'n/a') != '' else 'n/a'
    pocket = design_data.get('pocket', 'n/a') if design_data.get('pocket', 'n/a') != '' else 'n/a'
    zip = design_data.get('zip', 'n/a') if design_data.get('zip', 'n/a') != '' else 'n/a'
    button = design_data.get('button', 'n/a') if design_data.get('button', 'n/a') != '' else 'n/a'
    addt_design = design_data.get('addt_design', '').split()   

    shirts_common_prompt = f"There's a {material} {category}. The color of this {category} is {color}. This {neck_line} {category} is {sleeve_length}. "
    pocket_prompt = f"This {category} has a pocket on its {pocket} chest. "

    sweater_neck_common_prompt = f"There's a {material} {category}. The color of this {category} is {color}. This {neck_line} {category} is {pattern} pattern and {sleeve_length}. "
    zip_prompt = f"Also, the {category} is a {zip}. "

    if button:
        button_prompt = f"Also, this {category} has buttons {button}. They are on the {category} at regular intervals. "
    else:
        button_prompt = ""

    crop_prompt = f"The waist of the {category} is a short cropped shape. "
    fit_prompt = f"This {category} is shrunk to fit body shape. "
    background_prompt = f"There should be only clothing. The background should be plain white. "

    full_prompt = ""

    if category == 'sweater':
        if neck_line in ['turtle neck', 'mock neck']:
            if len(addt_design) == 0:
                full_prompt = sweater_neck_common_prompt + background_prompt
            elif len(addt_design) == 1:
                if addt_design[0] == 'crop':
                    full_prompt = sweater_neck_common_prompt + crop_prompt + background_prompt
                else:
                    full_prompt = sweater_neck_common_prompt + fit_prompt + background_prompt
            elif len(addt_design) == 2:
                full_prompt = sweater_neck_common_prompt + crop_prompt + fit_prompt + background_prompt
        else:
            if zip == 'n/a':
                if button == 'n/a':
                    if len(addt_design) == 0:
                        full_prompt = sweater_neck_common_prompt + background_prompt
                    elif len(addt_design) == 1:
                        if addt_design[0] == 'crop':
                            full_prompt = sweater_neck_common_prompt + crop_prompt + background_prompt
                        else:
                            full_prompt = sweater_neck_common_prompt + fit_prompt + background_prompt
                    elif len(addt_design) == 2:
                        full_prompt = sweater_neck_common_prompt + crop_prompt + fit_prompt + background_prompt
                elif button == 'half':
                    button = 'from the neck to the chest'
                    if len(addt_design) == 0:
                        full_prompt = sweater_neck_common_prompt + button_prompt + background_prompt
                    elif len(addt_design) == 1:
                        if addt_design[0] == 'crop':
                            full_prompt = sweater_neck_common_prompt + button_prompt + crop_prompt + background_prompt
                        else:
                            full_prompt = sweater_neck_common_prompt + button_prompt + fit_prompt + background_prompt
                    elif len(addt_design) == 2:
                        full_prompt = sweater_neck_common_prompt + button_prompt + crop_prompt + fit_prompt + background_prompt
                elif button == 'full':
                    if len(addt_design) == 0:
                        full_prompt = sweater_neck_common_prompt + button_prompt + background_prompt
                    elif len(addt_design) == 1:
                        if addt_design[0] == 'crop':
                            full_prompt = sweater_neck_common_prompt + button_prompt + crop_prompt + background_prompt
                        else:
                            full_prompt = sweater_neck_common_prompt + button_prompt + fit_prompt + background_prompt
                    elif len(addt_design) == 2:
                        full_prompt = sweater_neck_common_prompt + button_prompt + crop_prompt + fit_prompt + background_prompt
            elif zip == 'half':
                zip = 'half zip-up'
                if len(addt_design) == 0:
                    full_prompt = sweater_neck_common_prompt + zip_prompt + background_prompt
                elif len(addt_design) == 1:
                    if addt_design[0] == 'crop':
                        full_prompt = sweater_neck_common_prompt + zip_prompt + crop_prompt + background_prompt
                    else:
                        full_prompt = sweater_neck_common_prompt + zip_prompt + fit_prompt + background_prompt
                elif len(addt_design) == 2:
                    full_prompt = sweater_neck_common_prompt + zip_prompt + crop_prompt + fit_prompt + background_prompt
            elif zip == 'full':
                zip = 'full zip-up'
                if len(addt_design) == 0:
                    full_prompt = sweater_neck_common_prompt + zip_prompt + background_prompt
                elif len(addt_design) == 1:
                    if addt_design[0] == 'crop':
                        full_prompt = sweater_neck_common_prompt + zip_prompt + crop_prompt + background_prompt
                    else:
                        full_prompt = sweater_neck_common_prompt + zip_prompt + fit_prompt + background_prompt
                elif len(addt_design) == 2:
                    full_prompt = sweater_neck_common_prompt + zip_prompt + crop_prompt + fit_prompt + background_prompt
    else:
        if pocket == 'n/a':
            if len(addt_design) == 0:
                full_prompt = shirts_common_prompt + background_prompt
            elif len(addt_design) == 1:
                if addt_design[0] == 'crop':
                    full_prompt = shirts_common_prompt + crop_prompt + background_prompt
                else:
                    full_prompt = shirts_common_prompt + fit_prompt + background_prompt
            elif len(addt_design) == 2:
                full_prompt = shirts_common_prompt + crop_prompt + fit_prompt + background_prompt
        else:
            if len(addt_design) == 0:
                full_prompt = shirts_common_prompt + pocket_prompt + background_prompt
            elif len(addt_design) == 1:
                if addt_design[0] == 'crop':
                    full_prompt = shirts_common_prompt + pocket_prompt + crop_prompt + background_prompt
                else:
                    full_prompt = shirts_common_prompt + pocket_prompt + fit_prompt + background_prompt
            elif len(addt_design) == 2:
                full_prompt = shirts_common_prompt + pocket_prompt + crop_prompt + fit_prompt + background_prompt

    print("전체 프롬프트: ", full_prompt)

    return full_prompt

def make_prompt(result, design_data):
    material = result['material']
    category = result['category']
    color = result['color']
    
    neck_line = design_data['neck_line']
    sleeve_length = design_data['sleeve_length']
    pattern = design_data.get('pattern', 'n/a') if design_data.get('pattern', 'n/a') != '' else 'n/a'
    pocket = design_data.get('pocket', 'n/a') if design_data.get('pocket', 'n/a') != '' else 'n/a'
    zip = design_data.get('zip', 'n/a') if design_data.get('zip', 'n/a') != '' else 'n/a'
    button = design_data.get('button', 'n/a') if design_data.get('button', 'n/a') != '' else 'n/a'
    addt_design = design_data.get('addt_design', '').split()   

    shirts_common_prompt = f"There's a {material} {category}. The color of this {category} is {color}. This {neck_line} {category} is {sleeve_length}. "
    pocket_prompt = f"This {category} has a pocket on its {pocket} chest. "

    sweater_neck_common_prompt = f"There's a {material} {category}. The color of this {category} is {color}. This {neck_line} {category} is {pattern} pattern and {sleeve_length}. "
    zip_prompt = f"Also, the {category} is a {zip}. "

    if button:
        button_prompt = f"Also, this {category} has buttons {button}. They are on the {category} at regular intervals. "
    else:
        button_prompt = ""

    crop_prompt = f"The waist of the {category} is a short cropped shape. "
    fit_prompt = f"This {category} is shrunk to fit body shape. "
    background_prompt = f"There should be only clothing. The background should be plain white. "

    full_prompt = ""

    if category == 'sweater':
        if neck_line in ['turtle neck', 'mock neck']:
            if len(addt_design) == 0:
                full_prompt = sweater_neck_common_prompt + background_prompt
            elif len(addt_design) == 1:
                if addt_design[0] == 'crop':
                    full_prompt = sweater_neck_common_prompt + crop_prompt + background_prompt
                else:
                    full_prompt = sweater_neck_common_prompt + fit_prompt + background_prompt
            elif len(addt_design) == 2:
                full_prompt = sweater_neck_common_prompt + crop_prompt + fit_prompt + background_prompt
        else:
            if zip == 'n/a':
                if button == 'n/a':
                    if len(addt_design) == 0:
                        full_prompt = sweater_neck_common_prompt + background_prompt
                    elif len(addt_design) == 1:
                        if addt_design[0] == 'crop':
                            full_prompt = sweater_neck_common_prompt + crop_prompt + background_prompt
                        else:
                            full_prompt = sweater_neck_common_prompt + fit_prompt + background_prompt
                    elif len(addt_design) == 2:
                        full_prompt = sweater_neck_common_prompt + crop_prompt + fit_prompt + background_prompt
                elif button == 'half':
                    button = 'from the neck to the chest'
                    if len(addt_design) == 0:
                        full_prompt = sweater_neck_common_prompt + button_prompt + background_prompt
                    elif len(addt_design) == 1:
                        if addt_design[0] == 'crop':
                            full_prompt = sweater_neck_common_prompt + button_prompt + crop_prompt + background_prompt
                        else:
                            full_prompt = sweater_neck_common_prompt + button_prompt + fit_prompt + background_prompt
                    elif len(addt_design) == 2:
                        full_prompt = sweater_neck_common_prompt + button_prompt + crop_prompt + fit_prompt + background_prompt
                elif button == 'full':
                    if len(addt_design) == 0:
                        full_prompt = sweater_neck_common_prompt + button_prompt + background_prompt
                    elif len(addt_design) == 1:
                        if addt_design[0] == 'crop':
                            full_prompt = sweater_neck_common_prompt + button_prompt + crop_prompt + background_prompt
                        else:
                            full_prompt = sweater_neck_common_prompt + button_prompt + fit_prompt + background_prompt
                    elif len(addt_design) == 2:
                        full_prompt = sweater_neck_common_prompt + button_prompt + crop_prompt + fit_prompt + background_prompt
            elif zip == 'half':
                zip = 'half zip-up'
                if len(addt_design) == 0:
                    full_prompt = sweater_neck_common_prompt + zip_prompt + background_prompt
                elif len(addt_design) == 1:
                    if addt_design[0] == 'crop':
                        full_prompt = sweater_neck_common_prompt + zip_prompt + crop_prompt + background_prompt
                    else:
                        full_prompt = sweater_neck_common_prompt + zip_prompt + fit_prompt + background_prompt
                elif len(addt_design) == 2:
                    full_prompt = sweater_neck_common_prompt + zip_prompt + crop_prompt + fit_prompt + background_prompt
            elif zip == 'full':
                zip = 'full zip-up'
                if len(addt_design) == 0:
                    full_prompt = sweater_neck_common_prompt + zip_prompt + background_prompt
                elif len(addt_design) == 1:
                    if addt_design[0] == 'crop':
                        full_prompt = sweater_neck_common_prompt + zip_prompt + crop_prompt + background_prompt
                    else:
                        full_prompt = sweater_neck_common_prompt + zip_prompt + fit_prompt + background_prompt
                elif len(addt_design) == 2:
                    full_prompt = sweater_neck_common_prompt + zip_prompt + crop_prompt + fit_prompt + background_prompt
    else:
        if pocket == 'n/a':
            if len(addt_design) == 0:
                full_prompt = shirts_common_prompt + background_prompt
            elif len(addt_design) == 1:
                if addt_design[0] == 'crop':
                    full_prompt = shirts_common_prompt + crop_prompt + background_prompt
                else:
                    full_prompt = shirts_common_prompt + fit_prompt + background_prompt
            elif len(addt_design) == 2:
                full_prompt = shirts_common_prompt + crop_prompt + fit_prompt + background_prompt
        else:
            if len(addt_design) == 0:
                full_prompt = shirts_common_prompt + pocket_prompt + background_prompt
            elif len(addt_design) == 1:
                if addt_design[0] == 'crop':
                    full_prompt = shirts_common_prompt + pocket_prompt + crop_prompt + background_prompt
                else:
                    full_prompt = shirts_common_prompt + pocket_prompt + fit_prompt + background_prompt
            elif len(addt_design) == 2:
                full_prompt = shirts_common_prompt + pocket_prompt + crop_prompt + fit_prompt + background_prompt

    print("전체 프롬프트: ", full_prompt)

    return full_prompt