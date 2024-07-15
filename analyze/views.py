# analyze/views.py
import requests
from django.shortcuts import render, redirect
from .forms import ImageUploadForm, DesignForm
from .models import UploadedImage
from django.conf import settings

FASTAPI_URL = 'http://127.0.0.1:8001/predict/'
DALLE_API_URL = 'https://api.openai.com/v1/images/generations'

def upload_image(request):
    if request.method == 'GET':
        # 새로고침 시 세션 데이터 초기화
        request.session.pop('result', None)
        request.session.pop('image_url', None)
        request.session.pop('design_data', None)

    result = None
    image_instance = None
    design_form = DesignForm()

    if request.method == 'POST' and 'upload' in request.POST:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            with open(image_instance.image.path, 'rb') as f:
                response = requests.post(FASTAPI_URL, files={'file': f})
                if response.status_code == 200:
                    try:
                        result = response.json()
                        request.session['result'] = result
                        request.session['image_url'] = image_instance.image.url
                    except requests.exceptions.JSONDecodeError:
                        result = {"error": "Invalid JSON response"}
                else:
                    result = {"error": f"Error from FastAPI server: {response.status_code}"}
            # 이미지와 결과가 저장된 후 사용자 입력 폼을 조건에 맞게 표시
            if result['category'] == 'sweater':
                design_form.fields['pattern'].required = True
                design_form.fields['zip'].required = True
                design_form.fields['button'].required = True
                design_form.fields['b_shape'].required = True
                design_form.fields['b_color'].required = True
            else:
                design_form.fields['pocket'].required = True

    elif request.method == 'POST' and 'design' in request.POST:
        design_form = DesignForm(request.POST)
        if design_form.is_valid():
            design_data = design_form.cleaned_data
            request.session['design_data'] = design_data
            return redirect('dalle_result')

    else:
        form = ImageUploadForm()

    result = request.session.get('result', None)
    image_url = request.session.get('image_url', None)

    return render(request, 'analyze/upload.html', {
        'form': form,
        'result': result,
        'image_url': image_url,
        'design_form': design_form
    })

def dalle_result(request):
    if 'regenerate' in request.POST:
        prompt = request.session.get('prompt')
    else:
        design_data = request.session.get('design_data')
        result = request.session.get('result')
        prompt = make_prompt(result, design_data)
        request.session['prompt'] = prompt

    headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "size": "1024x1024",
        "quality": "standard",
        "n": 1,
    }
    response = requests.post(DALLE_API_URL, headers=headers, json=data)
    image_url = response.json()['data'][0]['url']
    return render(request, 'analyze/dalle_result.html', {'image_url': image_url})

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
    addt_design = design_data.get('addt_design', '').split()   


     # 프롬프트
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

def create_order(request):
    # 주문서 작성 로직 구현
    return render(request, 'analyze/create_order.html') 