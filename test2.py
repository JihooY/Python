from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "포트포워딩 성공!", "status": "online"}

@app.get("/test")
def test_page():
    return {"detail": "외부 접속이 원활하게 이루어지고 있습니다."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)