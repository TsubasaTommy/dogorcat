#ライブラリ
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
    
    #レスポンス 1:dog 2:cat 3:other
    return {"type": judge_type(image)}

def judge_type(image):
    #ここにAIの処理を書く
    return 1