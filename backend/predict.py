import os
import tensorflow as tf
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "deepfake_model.h5")

model = tf.keras.models.load_model(MODEL_PATH)

def predict_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (128,128))
    img = img/255.0
    img = np.reshape(img, (1,128,128,3))

    result = model.predict(img)[0][0]

    if result > 0.5:
        return "FAKE"
    else:
        return "REAL"
