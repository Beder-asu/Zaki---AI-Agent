from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse
from cbe.summarize import extract_text_from_pdf, summarize_rfi
from cbe.generate_report import generate_daily_report, generate_daily_report_doc
import os
import logging
import re
import mimetypes
import time

# Set up logging
logging.basicConfig(filename="zaki.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Zaki AI Agent API", description="API for Zaki: AI Agent Manager for Real Estate and Construction")

@app.post(
    "/summarize-rfi/",
    summary="Summarize RFI Document",
    description="Upload a PDF file containing an RFI to generate a summary of the requester's question, referenced documents, and a concise overview."
)
async def summarize_rfi_endpoint(file: UploadFile = File(..., description="PDF file containing the RFI")):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    content = await file.read()

    try:
        extracted_text = extract_text_from_pdf(content)
        if not extracted_text.strip():
            raise ValueError("No text found in PDF.")
        summary = summarize_rfi(extracted_text)
    except Exception as e:
        logger.error(f"RFI summarization failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")

    return {
        "filename": file.filename,
        "summary": summary
    }

@app.post(
    "/generate-daily-report/",
    summary="Generate Daily Site Report",
    description="Generate a professional daily site report from construction site inputs (weather, manpower, progress, safety, date, and optional photos). Returns a downloadable Word document with embedded photo if provided. Files are saved in the 'not_needed' subfolder.",
    responses={
        200: {
            "content": {"application/vnd.openxmlformats-officedocument.wordprocessingml.document": {}},
            "description": "Returns a Word document with the daily site report, including any uploaded photo."
        }
    }
)
async def generate_daily_report_endpoint(
    weather: str = Form(..., description="Weather conditions (e.g., 'Sunny, 75°F')"),
    manpower: str = Form(..., description="Manpower details (e.g., '20 workers, 2 absent')"),
    progress: str = Form(..., description="Progress updates (e.g., 'Completed foundation pour')"),
    safety: str = Form(..., description="Safety observations (e.g., 'No incidents')"),
    date: str = Form(..., description="Report date (e.g., '2025-07-03')"),
    photos: UploadFile = File(None, description="Optional photo upload (e.g., site image, .jpg or .png)")
):
    try:
        logger.info(f"Received report request: weather={weather}, manpower={manpower}, progress={progress}, safety={safety}, date={date}, photos={photos.filename if photos else 'None'}")
        
        # Validate inputs
        if not all([weather.strip(), manpower.strip(), progress.strip(), safety.strip(), date.strip()]):
            raise ValueError("All text fields (weather, manpower, progress, safety, date) must be non-empty.")

        # Sanitize date for filename
        safe_date = re.sub(r'[^a-zA-Z0-9\-]', '_', date)
        
        # Create not_needed directory
        not_needed_dir = os.path.join(os.getcwd(), "not_needed")
        os.makedirs(not_needed_dir, exist_ok=True)
        
        # Handle optional photo
        photo_description = photos.filename if photos else "No photos uploaded"
        temp_photo_path = None
        if photos:
            # Validate image format
            mime_type, _ = mimetypes.guess_type(photos.filename)
            if mime_type not in ["image/jpeg", "image/png"]:
                raise ValueError("Only JPEG or PNG images are supported")
            # Save photo to not_needed subfolder with timestamp
            timestamp = int(time.time())
            photo_filename = f"photo_{safe_date}_{timestamp}.{photos.filename.split('.')[-1]}"
            temp_photo_path = os.path.join(not_needed_dir, photo_filename)
            with open(temp_photo_path, "wb") as f:
                f.write(await photos.read())
            logger.info(f"Saved photo: {temp_photo_path}")
        
        # Generate report
        report_text = generate_daily_report({
            "weather": weather,
            "manpower": manpower,
            "progress": progress,
            "safety": safety,
            "date": date,
            "photos": photo_description
        })
        logger.info(f"Report text generated: {report_text}")
        
        # Save report to not_needed subfolder
        timestamp = int(time.time())
        output_path = os.path.join(not_needed_dir, f"daily_report_{safe_date}_{timestamp}.docx")
        generate_daily_report_doc(report_text, output_path, date, temp_photo_path)
        logger.info(f"Report saved to {output_path}")
        
        # Verify file exists
        if not os.path.exists(output_path):
            logger.error(f"File not found after generation: {output_path}")
            raise FileNotFoundError(f"Generated file {output_path} does not exist")
        
        return FileResponse(
            path=output_path,
            filename=f"Daily_Site_Report_{safe_date}.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        logger.error(f"Report generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)