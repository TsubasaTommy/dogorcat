from fastapi import FastAPI

app = FastAPI()


def getImage():
    ~~~~~

@app.get("/")
async def root():
    return {"message": "Hello World"}
