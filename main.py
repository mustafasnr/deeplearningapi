from fastapi import FastAPI,UploadFile
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.applications.vgg16 import VGG16
from pydantic import BaseModel
import numpy as np
from PIL import Image
import io
from tensorflow.keras.applications.imagenet_utils import decode_predictions
import json

app= FastAPI()

origins = ["*"]
model=VGG16(input_shape=(224,224,3))
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Info(BaseModel):
    size:int
    lenght:int


def create_result(preds,top=5): # first n pred 
    a=np.array(decode_predictions(preds, top=top)[0])
    siniflar,olasiliklar=[],[]

    for i in range(top):
        res=a[i][:][1:3]
        siniflar.append(res[0].strip())
        olasiliklar.append(float(res[1]))
    veri = {metin: sayi for metin, sayi in zip(siniflar, olasiliklar)}

    return json.loads(json.dumps(veri))

def ImageToArray(data,name): 
    byteImgIO = io.BytesIO(data)
    image=Image.open(byteImgIO)
    # image.save("resimler/"+name)
    image=image.resize((224, 224))
    image.save("resimler/"+name)# 224x224 image saved
    numpy_image=np.array([image])
    return numpy_image

@app.post("/models/vgg16/")
async def predict(file:UploadFile):
    image=ImageToArray(await file.read(),file.filename)
    pred=model.predict(image)
    result= create_result(pred,5)
    print(result)
    return result