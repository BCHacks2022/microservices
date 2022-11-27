from fastapi import FastAPI, File, UploadFile
from PyPDF2 import PdfFileReader
import io

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
    