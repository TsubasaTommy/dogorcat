from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "野獣先輩"}
