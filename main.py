from urllib import response
from fastapi import FastAPI, Request, File, UploadFile
import shutil
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
@app.get("/")
async def read_root():
  return { 
    "message": "Welcome to SALARY PREDICT API!",
   }

@app.post('/salary_with_formdata')
async def predictor_with_formdata(request: Request):
    # handle with data type is form data
    data = await request.json()
    try:
        # get data object from request
        data = data.get('data')

        # build model and salary prediction
        response = build_and_predict(data)
        return response
    except Exception:
        return {'message': "Error to fecth data of salary with form data"}

        
@app.post("/salary_with_singlefile")
async def upload(file: UploadFile = File()):
    # handle with data type is file data, include: single file or multiple files
    try:
        file_location = f"files/{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
        print(file_location)
        response = await build_and_predict(file_location, 'singlefile')
        print('response: ', response)
        return response
        # return {"message": "Success to upload"}
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    
