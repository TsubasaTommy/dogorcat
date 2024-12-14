#ライブラリ
from fastapi import FastAPI
import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt

app = FastAPI()

#モデルをロードする
model_path = "dogorcat.h5"
model = tf.keras.models.load_model(model_path)

#画像の読み込み
image_path = "画像のファイル名"
image_size = 100
image = cv2.imread(image_path)

#BGR -> RGBに変換
image = cv2.cvColor(image,cv2.COLOR_BGR2RGB)

#リサイズ
image_resized = cv2.resize(image,(img_size, img_size))

#正規化を行う
image_normalized = image_resized / 255.0

#次元を追加してバッチ化
input_data = np.expand_dims(image_normalized, axis = 0)

#モデルで画像を判別
predictions = model.predict(input_data)

print("予測結果：", predictions)


@app.get("/")
async def root():
    return("犬猫判別AI")
    
if image is None:
    print("画像を読み込めません")
    exit()