from fastapi import FastAPI
from backend.router import router
import uvicorn

app = FastAPI(title="AI Chatbot")
app.include_router(router)

if __name__ == "__main__":
  uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)
