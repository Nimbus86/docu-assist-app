from fastapi import FastAPI
from pydantic import BaseModel
import base64
import requests
import os

app = FastAPI()

AZURE_ENDPOINT = os.getenv("AZURE_ENDPPOINT")
AZURE_KEY = os.getenv("AZURE_KEY")


class Page(BaseModel):
    imageBase64: str

class DocumentRequest(BaseModel):
    pages: list[Page]


def ocr_image(base64_image: str) -> str:
    image_bytes = base64.b64decode(base64_image)

    url = f"{AZURE_ENDPOINT}/vision/v3.2/ocr?language=unk&detectOrientation=true"

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/octet-stream"
    }

    response = requests.post(url, headers=headers, data=image_bytes)
    result = response.json()

    extracted_text = ""

    for region in result.get("regions", []):
        for line in region.get("lines", []):
            words = [w["text"] for w in line.get("words", [])]
            extracted_text += " ".join(words) + "\n"

    return extracted_text.strip()


@app.post("/analyze_document")
def analyze_document(data: DocumentRequest):
    all_text = ""

    # 1. Voor elke pagina OCR uitvoeren
    for page in data.pages:
        text = ocr_image(page.imageBase64)
        all_text += text + "\n\n"

    all_text = all_text.strip()

    # 2. Dummy velden voor nu (later vervangen door AI)
    summary = "Samenvatting volgt later via AI."
    risks = ["Risico-analyse volgt later via AI."]
    advice = "Advies volgt later via AI."

    # 3. Antwoord dat de app makkelijk kan tonen
    return {
        "success": True,
        "page_count": len(data.pages),
        "text": all_text,
        "summary": summary,
        "risks": risks,
        "advice": advice
    }

