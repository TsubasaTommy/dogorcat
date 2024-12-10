#ライブラリ
from fastapi import FastAPI
import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt

app = FastAPI()


@app.get("/")
async def root():
 main.py-library

    return {"message": "野獣先輩"}

image_path = ""
image_size = 100
image = cv2.imread(image_path)

if image is None:
    print("画像を読み込めません")
    exit()


   
 main
