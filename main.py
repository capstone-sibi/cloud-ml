from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from predict import get_prediction
from google.cloud import storage
import uuid


GOOGLE_APPLICATION_CREDENTIALS="capstone-sibi.json"

app = FastAPI()

client = storage.Client()
bucket_name = "storage-capstone-sibi"

#domain where this api is hosted for example : localhost:5000/docs to see swagger documentation automagically generated.

class URLInput(BaseModel):
    url: str

def upload_to_gcs(file_name, file_content):
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(file_content)

@app.get("/")
def home():
    return {"result":"Hello World!!!"}

@app.post("/")
async def process_url(url_input: URLInput):
    received_url = url_input.url
    hasil_predict = get_prediction(received_url, "sibi.h5", "weights.43-1.09.hdf5")
    return {"result": f"{hasil_predict}"}

@app.post("/predict/")
async def upload_video(file: UploadFile = File(...)):
    myuuid = uuid.uuid4()
    file_content = await file.read()
    file_name = str(myuuid) + file.filename

    # Memanggil fungsi untuk mengupload ke GCS
    upload_to_gcs(file_name, file_content)
    res_url = f"https://storage.googleapis.com/{bucket_name}/{file_name}"
    hasil_predict = get_prediction(res_url, "sibi.h5", "weights.43-1.09.hdf5")
    
    return {"result": hasil_predict, "url_path": res_url}