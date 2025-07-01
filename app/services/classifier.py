import tensorflow as tf
import cv2
import numpy as np
from typing import Tuple

# Load pre-trained MobileNetV2 (replace with fine-tuned model later)
model = tf.keras.applications.MobileNetV2(weights="imagenet", include_top=False)

def preprocess_image(image_path: str) -> np.ndarray:
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    return np.expand_dims(img, axis=0)

def classify_image(image_path: str) -> Tuple[str, str, str]:
    img = preprocess_image(image_path)
    preds = model.predict(img)  # Replace with your fine-tuned model
    # Placeholder logic (update with actual classification)
    category = "shirt"
    color = "blue"
    style = "casual"
    return category, color, style