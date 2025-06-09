import os
from fastapi import FastAPI, Request, Response, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import io
from PIL import Image
import torch
from torchvision import transforms, models
import asyncio
import time
import logging

# ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# モデルの初期化
def load_model():
    logger.info("Loading model...")
    model = models.vgg16(pretrained=False)
    # 最後の層を2クラス分類用に変更
    model.classifier[6] = torch.nn.Linear(4096, 2)
    # 保存したモデルの重みを読み込む
    state_dict = torch.load("/app/model/my_model_pytorch.pth", map_location=torch.device("cpu"))
    
    # state_dictのキーから'vgg16.'プレフィックスを削除
    new_state_dict = {}
    for key, value in state_dict.items():
        new_key = key.replace('vgg16.', '')
        new_state_dict[new_key] = value
    
    model.load_state_dict(new_state_dict)
    model.eval()
    logger.info("Model loaded successfully")
    return model

model = load_model()

# フロントエンドのURL
FRONTEND_URL = "http://localhost:5173"
logger.info(f"Frontend URL configured as: {FRONTEND_URL}")

app.add_middleware(
    CORSMiddleware,

    allow_origins=[FRONTEND_URL],
    allow_credentials=False,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]

)

@app.options("/{rest_of_path:path}")
async def preflight_handler(rest_of_path: str):
    logger.info(f"Handling OPTIONS request for path: {rest_of_path}")
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = FRONTEND_URL
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@app.post("/")
async def root(file: UploadFile = File(...)):
    logger.info("Received file upload request")
    try:
        image_data = await file.read()
        logger.info(f"File read successfully, size: {len(image_data)} bytes")
        loop = asyncio.get_event_loop()
        # judge_type 関数の処理を別スレッドで実行
        result = await loop.run_in_executor(None, judge_type, image_data)
        logger.info(f"Processing complete, result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in root: {str(e)}")
        return {"error": str(e)}

def judge_type(image):
    start_time = time.time()
    try:
        print("judge_type 開始")
        image = Image.open(io.BytesIO(image)).convert("RGB")
        image = image.resize((224, 224))  # VGG16の入力サイズ
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        img_tensor = transform(image)
        img_tensor = img_tensor.unsqueeze(0)
        
        with torch.no_grad():
            output = model(img_tensor)
            probabilities = torch.softmax(output, dim=1)
            
        predicted_class = int(torch.argmax(probabilities, dim=1).item())
        cat_probability = float(probabilities[0][0].item())
        dog_probability = float(probabilities[0][1].item())
        
        result = {
            "type": predicted_class,
            "dog": dog_probability,
            "cat": cat_probability,
        }
        print("judge_type 終了、処理時間:", time.time() - start_time)
        return result
    except Exception as e:
        print("judge_type エラー:", e)
        return {"error": str(e)}
