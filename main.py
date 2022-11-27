# Get the models before running
# https://drive.google.com/file/d/19B1fGVMn9-pSBemAbsl62L9tHawrjVe5/view?usp=drivesdk
# https://drive.google.com/file/d/1-1g6ME8LA8FR2pPbgZ2md5wTr7BjkpM7/view?usp=drivesdk
from fastapi import FastAPI, File, UploadFile
from PyPDF2 import PdfFileReader
import io
from bs4 import BeautifulSoup

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "I am glad you are here, we have some cookies, come here!"}




def analyzePDF(request_object_content):
    parts=[]
    def visitor_body(text, cm, tm, fontDict, fontSize):
        parts.append(text)

    pdf = PdfFileReader(io.BytesIO(request_object_content))
    pages = pdf.pages

    for i in pages:
        i.extract_text(visitor_text=visitor_body)
    words = []
    for i in parts:
        tmp = i.split(" ")
        for j in tmp:
            if j!= "" and j!="\n":
                word = ''.join(c for c in j.lower() if (48<=ord(c)<=57 or 97<=ord(c)<=122 or ord(c)==58))
                words.append(word)
    return [len(pages),words]

from checkers import checkers

@app.post("/contractKeywordChecking")
async def contract(file: UploadFile):
    request_object_content = await file.read()
    numberOfPages, text = analyzePDF(request_object_content)
    print("landlord" in " ".join(text))
    warnings = [checker(" ".join(text)) for checker in checkers]
    print(warnings)
    return [warning for warning in warnings if warning != "Included"]



@app.post("/appendToPDF")
async def contract(file: UploadFile, text: str):
    request_object_content = await file.read()
    
import tensorflow as tf
import pickle
import numpy as np
with open("word_to_token.pkl", "rb") as f:
    word_to_token = pickle.load(f)

max_length = 170
model1 = tf.keras.models.load_model('model1.h5')
model2 = tf.keras.models.load_model('model2.h5')

@app.post("/pp")
def ppML(text):
    text = text.lower().split(". ")
    frame = []
    for i in text:
        tmp = []
        for j in i.split(" "):
            try:
                tmp.append(word_to_token[j])
            except:
                # print("WWWWW")
                tmp.append(0)
        if len(tmp)>=max_length:
            print("PP")
            print(len(tmp[0:max_length+1]))
            frame.append(tmp[0:max_length+1])

            # for i in range(0,len(tmp),max_length+1):
            #     frame.append(tmp[i:i+max_length+1])
        else:
            tmp.extend([0]*(max_length+1-len(tmp)))
            frame.append(tmp)

            # print(len(tmp))
        # tmp.extend([0]*(max_length+1-len(i)))
    print(len(frame[10]))
    frame = np.array(frame)
    # for i in frame:
    #     print(len(frame))
    negative = np.array(model1.predict(np.array(frame)))
    positive = np.array(model2.predict(np.array(frame)))
    returns = []
    print(text)
    print(positive,negative)
    for i in range(negative.shape[0]):
        returns.append([text[i], "positive" if positive[i]>0.5 else "negative" if negative[i]>0.5 else "neutral"])
    return returns

async def contract(text: str):
    return ppML(text)

import requests
@app.post("/ppURL")
async def contract2(url: str):
    if url==" ":
        url = "https://www.linkedin.com/legal/privacy-policy"
    # From https://matix.io/extract-text-from-webpage-using-beautifulsoup-and-python/
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    text = soup.find_all(text=True)
    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        # there may be more elements you don't want, such as "style", etc.
    ]

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)  

    # End from
    
    return ppML(output)