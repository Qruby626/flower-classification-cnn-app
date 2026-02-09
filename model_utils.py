import os
import numpy as np
import keras
from keras.preprocessing import image
from keras.models import load_model

# Configuration
IMG_SIZE = (224, 224)
MODEL_PATH = 'model/flower_model.keras'
CLASS_NAMES = ['Daisy', 'Dandelion', 'Rose', 'Sunflower', 'Tulip']

# Load model once
_model = None

def get_model():
    global _model
    if _model is None:
        if os.path.exists(MODEL_PATH):
            _model = load_model(MODEL_PATH)
            print(f"Model loaded from {MODEL_PATH}")
        else:
            print(f"Error: Model not found at {MODEL_PATH}")
            return None
    return _model

def preprocess_image(img_path):
    """
    Preprocessing: Resize to 224x224 and normalize (0-1)
    """
    img = image.load_img(img_path, target_size=IMG_SIZE)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) # (1, 224, 224, 3)
    img_array = img_array / 255.0  # Normalisasi (0-1)
    return img_array

def predict_flower(img_path):
    model = get_model()
    if model is None:
        return None, 0, []

    processed_img = preprocess_image(img_path)
    predictions = model.predict(processed_img)[0]
    
    top_index = np.argmax(predictions)
    confidence = predictions[top_index]
    label = CLASS_NAMES[top_index]
    
    all_probs = [
        {"class": CLASS_NAMES[i], "probability": float(predictions[i])}
        for i in range(len(CLASS_NAMES))
    ]
    # Sort descending by probability
    all_probs.sort(key=lambda x: x['probability'], reverse=True)
    
    return label, confidence, all_probs
