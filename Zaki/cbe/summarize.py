import pdfplumber
import requests
import io

API_URL = "https://router.huggingface.co/featherless-ai/v1/chat/completions"
HEADERS = {
    "Authorization": "Bearer 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",
}

# Next step: configure gmail automationto run the app solely atonomus
def extract_text_from_pdf(file: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(file)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def summarize_rfi(text: str) -> str:
    prompt = ("Summarize the following RFI document. Please extract the Requester's Question/Clarification and any Referenced drawings or documents. Format your output as follows:" 
                  "Requester Question / Clarification: [The main question or clarification requested in one sentence]"
                   " Referenced drawings or documents: [List of any referenced documents or drawings]"
                   " Full Summary: [A concise overall summary of the RFI in a one short, concise, clear and to the point paragraph]"
                   f"The document: {text}")


    payload = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.6,
        "top_p": 0.7,
        "model": "google/gemma-2-2b-it"
    }
    #in-plan: sending the summary in a new email to the involved stake holder
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
