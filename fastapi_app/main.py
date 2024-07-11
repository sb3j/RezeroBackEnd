import logging
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
from huggingface_hub import hf_hub_download
import webcolors
from .models import PredictionResult
from .utils import load_image_into_numpy_array, get_dominant_color, closest_color

# 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

app = FastAPI()

# 모델 파일 다운로드 및 로드 (서버 시작 시 한 번만 실행)
logging.info("Downloading and loading models...")
category_model_file = hf_hub_download(repo_id="ssoypark/fine_tuned_clothing_models", filename="fine_tuned_clothing_model.h5")
category_model = tf.keras.models.load_model(category_model_file)

material_model_file = hf_hub_download(repo_id="ssoypark/fine_tuned_clothing_models", filename="fine_tuned_material_model.h5")
material_model = tf.keras.models.load_model(material_model_file)
logging.info("Models loaded successfully.")

@app.post("/predict/", response_model=PredictionResult)
async def predict(file: UploadFile = File(...)):
    try:
        img_data = await file.read()
        img_array = load_image_into_numpy_array(img_data)
        img_batch = np.expand_dims(img_array, axis=0)

        predictions_ct = category_model.predict(img_batch)
        predicted_class_ct = np.argmax(predictions_ct, axis=1)

        predictions_mt = material_model.predict(img_batch)
        predicted_class_mt = np.argmax(predictions_mt, axis=1)

        category_labels = ["t-shirt", "sweater", "shirt"]
        material_labels = ["Cotton", "Polyester", "Wool"]

        predicted_label_ct = category_labels[predicted_class_ct[0]]
        predicted_label_mt = material_labels[predicted_class_mt[0]]

        dominant_color_hex = get_dominant_color(img_data)
        dominant_rgb = webcolors.hex_to_rgb(dominant_color_hex)
        color_name = closest_color(dominant_rgb)

        response_data = {
            "category": predicted_label_ct,
            "material": predicted_label_mt,
            "color": color_name,
        }

        logging.info("Response Data: %s", response_data)
        return JSONResponse(response_data)
    except Exception as e:
        logging.error("Error processing request: %s", e)
        return JSONResponse({"error": "Internal server error"}, status_code=500)