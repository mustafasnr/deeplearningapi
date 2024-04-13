from fastapi import FastAPI,UploadFile,Depends
from keras.applications.vgg16 import VGG16
from pydantic import BaseModel
import numpy as np
from PIL import Image
import io
from keras.applications.imagenet_utils import decode_predictions
import json


app= FastAPI()

class Info(BaseModel):
    size:int


def create_result(preds,top=5): # son tahmin aşamasında 1000 tane sınıftan ilk n sayıda tahminin json formatında sonuçları 
    a=np.array(decode_predictions(preds, top=top)[0])
    siniflar,olasiliklar=[],[]

    for i in range(top):
        res=a[i][:][1:3]
        siniflar.append(res[0].strip())
        olasiliklar.append(float(res[1]))
    veri = {metin: sayi for metin, sayi in zip(siniflar, olasiliklar)}

    return json.loads(json.dumps(veri))

def ImageToArray(data): # files parametresinde taşınan resmin 224x224 boyutuna getirip numpy dizisine çevirme aşamaları
    byteImgIO = io.BytesIO(data)
    image=Image.open(byteImgIO)
    image=image.resize((224, 224))
    numpy_image=np.array([image])
    return numpy_image

@app.post("/models/vgg16/")
async def predict(file:UploadFile,item:Info=Depends()):
    model=VGG16(input_shape=(224,224,3))

    image=ImageToArray(await file.read())
    
    pred=model.predict(image,batch_size=1)
    result= create_result(pred,item.size)
    return result