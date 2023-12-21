from fastapi import FastAPI
from pydantic import BaseModel
from predict import get_prediction

app = FastAPI()

#domain where this api is hosted for example : localhost:5000/docs to see swagger documentation automagically generated.

class URLInput(BaseModel):
    url: str

@app.get("/")
def home():
    return {"result":"Hello World!!!"}

@app.post("/")
async def process_url(url_input: URLInput):
    received_url = url_input.url
    #hasil_predict = get_prediction(received_url, "sibi.h5", "weights.43-1.09.hdf5")
    hasil_predict = received_url
    return {"result": f"{hasil_predict}"}