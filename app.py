from urllib import response
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from models.main import *

# app config
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# routers
@app.get("/", tags=["Root"])
async def read_root():
  return { 
    "message": "Welcome to my notes application, use the /docs route to proceed"
   }

@app.post('/salary')
async def predictor(request: Request):
    data = await request.json()
    if data:
        type = data.get('type')
        data = data.get('data')
        if type == 'single':
            response = build_and_predict(data)
            return response
        else:
            print('multi handle')
            return '1'
    