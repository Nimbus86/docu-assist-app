from fastapi import FastAPI
from pydantic import BaseModel
import base64

app = FastAPI()

class Page(BaseModel):
    imageBase64: str

class DocumentRequest(BaseModel):
    pages: list[Page]

@app.post("/analyze_document")
def analyze_document(data: DocumentRequest):
    page_count = len(data.pages)

    return {
        "message": "Document ontvangen",
        "page_count": page_count
    }
