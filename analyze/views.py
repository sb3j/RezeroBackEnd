import requests
from django.shortcuts import render, redirect
from .forms import ImageUploadForm, DesignForm
from .models import OrderInfo
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UploadedImageSerializer
from rest_framework.views import APIView

FASTAPI_URL = 'http://127.0.0.1:8001/predict/'
DALLE_API_URL = 'https://api.openai.com/v1/images/generations'

class UploadImageView(generics.CreateAPIView):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        form = ImageUploadForm(request.POST, request.FILES)
        design_form = DesignForm(request.POST)

        if form.is_valid() and design_form.is_valid():
            image_instance = form.save(commit=False)
            image_instance.user = request.user
            image_instance.save()

            with open(image_instance.image.path, 'rb') as f:
                response = requests.post(FASTAPI_URL, files={'file': f})
                if response.status_code == 200:
                    try:
                        result = response.json()
                        request.session['result'] = result
                        request.session['image_url'] = image_instance.image.url
                        request.session['image_id'] = image_instance.id

                        # Design data를 세션에 저장
                        design_data = design_form.cleaned_data
                        request.session['design_data'] = design_data

                        image_instance.material = result.get('material', '')
                        image_instance.category = result.get('category', '')
                        image_instance.color = result.get('color', '')
                        image_instance.neck_line = design_data.get('neck_line', '')
                        image_instance.sleeve_length = design_data.get('sleeve_length', '')
                        image_instance.pattern = design_data.get('pattern', '')
                        image_instance.pocket = design_data.get('pocket', '')
                        image_instance.zip = design_data.get('zip', '')
                        image_instance.button = design_data.get('button', '')
                        image_instance.b_shape = design_data.get('b_shape', '')
                        image_instance.b_color = design_data.get('b_color', '')
                        image_instance.addt_design = design_data.get('addt_design', '')
                        image_instance.save()

                        print("Session data saved:")
                        print("result:", request.session.get('result'))
                        print("image_url:", request.session.get('image_url'))
                        print("image_id:", request.session.get('image_id'))
                        print("design_data:", request.session.get('design_data'))

                    except requests.exceptions.JSONDecodeError:
                        result = {"error": "Invalid JSON response"}
                else:
                    result = {"error": f"Error from FastAPI server: {response.status_code}"}

            return Response({"message": "Image uploaded and analyzed successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Invalid form data"}, status=status.HTTP_400_BAD_REQUEST)

class DalleResultAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("Session data in DalleResultAPIView:")
        print("image_id:", request.session.get('image_id'))
        print("design_data:", request.session.get('design_data'))
        print("result:", request.session.get('result'))

        image_id = request.session.get('image_id')
        design_data = request.session.get('design_data')
        result = request.session.get('result')

        if image_id is None or design_data is None or result is None:
            return Response({"error": "Missing data in the session"}, status=status.HTTP_400_BAD_REQUEST)

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

            image_instance = UploadedImage.objects.get(id=image_id)
            image_instance.prompt = prompt
            image_instance.dalle_image_url = image_url
            image_instance.save()

            serializer = UploadedImageSerializer(image_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Error from DALL-E API"}, status=response.status_code)

def make_prompt(result, design_data):
    material = result['material']
    category = result['category']
    color = result['color']
    
    neck_line = design_data['neck_line']
    sleeve_length = design_data['sleeve_length']
    pattern = design_data.get('pattern', '')
    pocket = design_data.get('pocket', '')
    zip = design_data.get('zip', '')
    button = design_data.get('button', '')
    b_shape = design_data.get('b_shape', '')
    b_color = design_data.get('b_color', '')
    addt_design = design_data.get('addt_design', '').split()   

    shirts_common_prompt = f"There's a {material} {category}. The color of this {category} is {color}. This {neck_line} {category} is {sleeve_length}."
    pocket_prompt = f"This {category} has a pocket on its {pocket} chest. "

    sweater_neck_common_prompt = f"There's a {material} {category}. The color of this {category} is {color}. This {neck_line} {category} is {pattern} pattern and {sleeve_length}. "
    zip_prompt = f"Also, the {category} is a {zip}."

    if button:
        button_prompt = f"Also, this {category} has buttons {button}. They are on the {category} at regular intervals. "
    else:
        button_prompt = ""

    crop_prompt = f"The waist of the {category} is a short cropped shape. "
    fit_prompt = f"This {category} is shrunk to fit body shape. "
    background_prompt = f"And it's hanging on a hanger. The background should be plain white. "

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
            if zip == 'x':
                if button == 'x':
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
            elif zip == 'half zip-up':
                if len(addt_design) == 0:
                    full_prompt = sweater_neck_common_prompt + zip_prompt + background_prompt
                elif len(addt_design) == 1:
                    if addt_design[0] == 'crop':
                        full_prompt = sweater_neck_common_prompt + zip_prompt + crop_prompt + background_prompt
                    else:
                        full_prompt = sweater_neck_common_prompt + zip_prompt + fit_prompt + background_prompt
                elif len(addt_design) == 2:
                    full_prompt = sweater_neck_common_prompt + zip_prompt + crop_prompt + fit_prompt + background_prompt
            elif zip == 'full zip-up':
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
        if pocket == 'x':
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
