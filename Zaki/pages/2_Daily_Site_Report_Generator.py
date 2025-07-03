import streamlit as st
import os
import re
from datetime import datetime
from services.report_generator import generate_daily_report_api

# Access API config from session_state set in app.py
api_base_url = st.session_state.api_base_url
api_token = st.session_state.api_token

st.header("📊 Daily Site Report Generator")
st.markdown("Generate a professional daily site report from site inputs and an optional photo.")

# Input fields for report data
report_weather = st.text_input(
    "Weather Conditions",
    placeholder="e.g., Sunny, 75°F",
    help="Enter the weather conditions (e.g., temperature, precipitation).",
    key="report_weather"
)
report_manpower = st.text_input(
    "Manpower",
    placeholder="e.g., 20 workers, 2 absent",
    help="Enter manpower details (e.g., worker count, absences).",
    key="report_manpower"
)
report_progress = st.text_input(
    "Progress",
    placeholder="e.g., Completed foundation pour",
    help="Describe the day’s progress (e.g., tasks completed).",
    key="report_progress"
)
report_safety = st.text_input(
    "Safety Observations",
    placeholder="e.g., No incidents",
    help="Enter safety observations (e.g., incidents or none).",
    key="report_safety"
)
report_date = st.text_input(
    "Report Date",
    value=datetime.now().strftime("%Y-%m-%d"), # Default to current date
    placeholder="e.g., 2025-07-03 or 3 jul 25",
    help="Enter the report date (any format, e.g., 2025-07-03 or 3 jul 25).",
    key="report_date"
)

report_photo = st.file_uploader(
    "Upload Photo (Optional)",
    type=["jpg", "jpeg", "png"],
    help="Upload an optional JPEG or PNG photo of the site.",
    key="report_photo_uploader"
)

# Display photo preview if uploaded
if report_photo:
    st.image(report_photo, caption=report_photo.name, width=200)

generate_button_clicked = st.button("Generate Report", disabled=not api_base_url, key="generate_report_button")

# Error message placeholders for validation
weather_error = st.empty()
manpower_error = st.empty()
progress_error = st.empty()
safety_error = st.empty()
date_error = st.empty()
photo_error = st.empty()
report_generation_error = st.empty()

if generate_button_clicked:
    # Clear previous errors
    weather_error.empty()
    manpower_error.empty()
    progress_error.empty()
    safety_error.empty()
    date_error.empty()
    photo_error.empty()
    report_generation_error.empty()

    # Client-side validation
    is_valid = True
    if not report_weather:
        weather_error.error("Weather Conditions is required.")
        is_valid = False
    if not report_manpower:
        manpower_error.error("Manpower is required.")
        is_valid = False
    if not report_progress:
        progress_error.error("Progress is required.")
        is_valid = False
    if not report_safety:
        safety_error.error("Safety Observations is required.")
        is_valid = False
    if not report_date:
        date_error.error("Report Date is required.")
        is_valid = False
    
    if report_photo:
        if report_photo.type not in ["image/jpeg", "image/png"]:
            photo_error.error("Please upload a valid JPEG or PNG file.")
            is_valid = False

    if is_valid:
        with st.spinner("Generating Daily Site Report... This may take a moment."):
            try:
                report_data = {
                    "weather": report_weather,
                    "manpower": report_manpower,
                    "progress": report_progress,
                    "safety": report_safety,
                    "date": report_date,
                }
                
                photo_file_for_api = None
                if report_photo:
                    photo_file_for_api = (report_photo.name, report_photo.getvalue(), report_photo.type)

                docx_content = generate_daily_report_api(api_base_url, report_data, photo_file_for_api, api_token)
                
                if docx_content:
                    clean_date = re.sub(r'[^a-zA-Z0-9]', '_', report_date)
                    download_filename = f"Daily_Site_Report_{clean_date}.docx"

                    st.success(f"Report generated successfully! Downloading {download_filename}.")
                    st.download_button(
                        label="Download Report",
                        data=docx_content,
                        file_name=download_filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key="download_report_button"
                    )
                    st.markdown(
                        """
                        <div style="background-color: #e0f7fa; padding: 10px; border-radius: 5px; margin-top: 15px;">
                            <strong>Note:</strong> The generated .docx file and any uploaded photo are also saved in the 
                            <code>C:\\Users\\mobed\\Desktop\\Zaki\\not_needed</code> subfolder on your backend server.
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    report_generation_error.error("Failed to generate report: No content received.")
            except ValueError as ve:
                report_generation_error.error(f"Failed to generate report: {ve}. Please try again or contact support.")
            except Exception as e:
                report_generation_error.error(f"An unexpected error occurred: {e}. Please try again or contact support.")
                st.exception(e)
    else:
        report_generation_error.error("Please correct the errors in the form.")
