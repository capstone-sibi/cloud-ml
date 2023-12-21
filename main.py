from fastapi import FastAPI
from pydantic import BaseModel
from predict import get_prediction

app = FastAPI()

#domain where this api is hosted for example : localhost:5000/docs to see swagger documentation automagically generated.


@app.get("/")
def home():
    return {"message":"Hello TutLinks.com"}

class URLInput(BaseModel):
    url: str

@app.post("/")
async def process_url(url_input: URLInput):
    received_url = url_input.url
    hasil_predict = get_prediction(received_url, "sibi.h5", "weights.43-1.09.hdf5")
    return {"message": f"URL received: {hasil_predict}"}