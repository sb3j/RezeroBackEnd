# fastapi_app/main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
from PIL import Image
import io
from huggingface_hub import hf_hub_download

app = FastAPI()

# 모델 파일 다운로드 및 로드
category_model_file = hf_hub_download(repo_id="ssoypark/fine_tuned_clothing_models", filename="fine_tuned_clothing_model.h5")
category_model = tf.keras.models.load_model(category_model_file)

material_model_file = hf_hub_download(repo_id="ssoypark/fine_tuned_clothing_models", filename="fine_tuned_material_model.h5")
material_model = tf.keras.models.load_model(material_model_file)

def load_image_into_numpy_array(data):
    image = Image.open(io.BytesIO(data))
    image = image.resize((224, 224))
    return np.array(image) / 255.0

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    img_data = await file.read()
    img_array = load_image_into_numpy_array(img_data)
    img_batch = np.expand_dims(img_array, axis=0)

    # 카테고리 모델 예측
    predictions_ct = category_model.predict(img_batch)
    predicted_class_ct = np.argmax(predictions_ct, axis=1)

    # 재질 모델 예측
    predictions_mt = material_model.predict(img_batch)
    predicted_class_mt = np.argmax(predictions_mt, axis=1)

    category_labels = ["t-shirt", "sweater", "shirt"]
    material_labels = ["Cotton", "Polyester", "Wool"]

    predicted_label_ct = category_labels[predicted_class_ct[0]]
    predicted_label_mt = material_labels[predicted_class_mt[0]]

    return JSONResponse({
        "category": predicted_label_ct,
        "material": predicted_label_mt
    })
