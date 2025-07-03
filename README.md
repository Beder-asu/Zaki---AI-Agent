1- from search bar open cmd (Command Prompt)

2- paste: pip install requests python-docx pillow fastapi uvicorn pdfplumber streamlit python-multipart

3- go to submission folder --> zaki folder --> copy the path from the path bar = copied_path

4- in cmd write -> cd copied_path
	then write -> uvicorn main:app --reload
 
5- open new cmd window (DO NOT CLOSE THE EXISTING)
	write -> cd copied_path	
	   then write -> streamlit run ui_app.py
    
6- to try the RFI summarizer, upload the RFI file from copied_path

7- to try the report generator insert any dummy data and upload 
   any image into the form then witness the output

NOTE: if you are using a certain conda env or similar packages you will need to 
	activate it at steps 4 and 5
 
PS: If not working try to copy the main host url(Beside running on statement at step 4)
	then paste it in the side panel
 
PS: For simplicity I will include my own HF token url

Design: The UI leverages Streamlit for a simple, interactive web interface, 
	enabling rapid development and deployment. Input fields for weather, manpower,
	progress, safety, and date are designed for user-friendly data entry, with a default
	 date set to today. Optional photo uploads support JPEG/PNG formats with previews for 
	validation. Client-side validation ensures non-empty inputs, while FastAPI handles backend 
	processing, generating downloadable Word reports. Logging is integrated for debugging, and 
	files are saved in a dedicated not_needed directory.

Limitations: The system relies on a stable internet connection for API calls,
	 which may fail if the backend is down. Only PDF files are supported for RFI summarization,
	 and photo uploads are limited to JPEG/PNG. The date format is flexible but not strictly validated
	, risking filename issues. Error handling is robust but may not cover all edge cases, and large file 
	uploads could strain memory. Streamlit's UI lacks advanced customization options.

283 words 1,814 characters.
