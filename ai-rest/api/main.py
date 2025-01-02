#ライブラリ
import os
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
import io
import numpy as np
from PIL import Image
import tensorflow as tf

app = FastAPI()
model = tf.keras.models.load_model("/app/model/dogorcat.h5")

# CORS の設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 許可するオリジン
    allow_credentials=True,
    allow_methods=["*"],  # 許可する HTTP メソッド
    allow_headers=["*"],  # 許可する HTTP ヘッダー
)

@app.post("/")
async def root(request: Request):
    
    # blob形式でimageを受け取る
    image = await request.body()
    
    #レスポンス 0:cat 1:dog
    return judge_type(image)

def judge_type(image):
    #ここにAIの処理を書く
    try:
        # BlobをPillow Imageに変換
        image = Image.open(io.BytesIO(image)).convert("RGB")

        # モデルの入力サイズにリサイズ (例: 224x224)
        image = image.resize((100, 100))

        # 配列に変換して正規化 (0～1にスケール)
        img_array = np.array(image) / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # バッチ次元を追加

        # モデルで推論
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]
        # 犬と猫の確率を取得
        dog_probability = predictions[0][1]  # 犬の確率 (例: 1 が犬の場合)
        cat_probability = predictions[0][0]  # 猫の確率 (例: 0 が猫の場合)

        # 犬か猫の判定 (モデルのクラス定義に応じて調整)
        return {
            "type":int(predicted_class),
            "dog": float(dog_probability),
            "cat": float(cat_probability),
        }
    except Exception as e:
        print(e)
        return -1
    