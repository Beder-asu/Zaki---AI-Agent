import streamlit as st
import os
import re
from datetime import datetime
from services.summarizer import summarize_rfi_api
from services.report_generator import generate_daily_report_api

st.set_page_config(
    page_title="Zaki RFI Tools",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Sidebar Content and API Configuration ---
st.sidebar.title("🛠️ Zaki RFI Tools")

# API Configuration
st.sidebar.header("API Configuration")
if 'api_base_url' not in st.session_state:
    st.session_state.api_base_url = os.getenv("BACKEND_API_BASE_URL", "http://localhost:8000")

api_base_url = st.sidebar.text_input(
    "Backend API Base URL:",
    value=st.session_state.api_base_url,
    help="The base URL for your backend API (e.g., http://localhost:8000)"
)
st.session_state.api_base_url = api_base_url

if 'api_token' not in st.session_state:
    st.session_state.api_token = os.getenv("BACKEND_API_TOKEN", "")

api_token = st.sidebar.text_input(
    "Backend API Token (optional):",
    type="password",
    value=st.session_state.api_token,
    help="Enter your backend API token if authentication is required."
)
st.session_state.api_token = api_token

if not api_base_url:
    st.sidebar.warning("Please enter your backend API Base URL to proceed.")

st.sidebar.markdown("---") # Separator

# Manual Navigation
st.sidebar.markdown("Navigate between different tools:")
page_selection = st.sidebar.radio(
    "Go to",
    ["I am Zaki", "RFI Summarizer", "Daily Site Report Generator"],
    index=0, # Default to "I am Zaki"
    key="main_navigation"
)

# --- Main Content Area ---

if page_selection == "I am Zaki":
    st.title("I am Zaki")
    st.header("Zaki: AI Agent Manager for Real Estate and Construction")
    st.subheader("Overview")
    st.write(
        "Zaki is an intelligent, modular AI agent system designed to automate high-friction, repetitive workflows in the construction, real estate, and property management industries. "
        "Zaki combines large language models (LLMs), vision models, and system-level integrations to operate as a proactive digital employee across multiple domains—offering speed, clarity, and operational efficiency where traditional systems fall short."
    )
    st.write(
        "Zaki is not a single AI model, but a multi-agent architecture composed of microservices, each responsible for solving a specific pain point in real-world project workflows."
    )
    st.subheader("How Zaki Works")
    st.write(
        "Zaki is designed around a layered, service-oriented software architecture that consists of four main layers:"
    )
    st.markdown("""
    - **Presentation UI**: Web dashboards, CLI tools, and APIs that allow engineers, site managers, and clients to interact with Zaki.
    - **Application Orchestrator**: Routes requests, handles user authentication, logs actions, and directs data flow to the appropriate services.
    - **Intelligent Processing Layer**: Handles prompt engineering, model selection, and execution logic via LLMs (e.g., GPT-4) or custom classifiers.
    - **Task Modules**: A plug-in layer of intelligent services, each encapsulating a microservice that solves a specific business task.
    """)

elif page_selection == "RFI Summarizer":
    st.header("📝 RFI Summarizer")
    st.markdown("Upload an RFI document (PDF) to get a structured summary.")

    rfi_uploaded_file = st.file_uploader(
        "Upload an RFI Document (.pdf)",
        type=["pdf"],
        accept_multiple_files=False,
        key="rfi_uploader"
    )

    rfi_summary_placeholder = st.empty()

    if rfi_uploaded_file is not None:
        rfi_file_type = rfi_uploaded_file.type
        rfi_file_name = rfi_uploaded_file.name

        st.info(f"RFI File uploaded: **{rfi_file_name}** ({rfi_file_type})")

        if rfi_file_type == "application/pdf":
            if st.button("Summarize RFI", disabled=not api_base_url, key="summarize_button"):
                if not api_base_url:
                    st.error("Please provide the API Base URL in the sidebar to summarize.")
                else:
                    with st.spinner("Summarizing RFI... This may take a moment."):
                        try:
                            file_bytes = rfi_uploaded_file.getvalue()
                            response_data = summarize_rfi_api(api_base_url, file_bytes, rfi_file_name, api_token)
                            
                            if response_data and "summary" in response_data:
                                summary_text = response_data["summary"]
                                st.success("Summarization Complete!")
                                
                                rfi_summary_placeholder.subheader("Summary:")
                                
                                requester_question = "N/A"
                                referenced_docs = "N/A"
                                
                                rq_match = re.search(r"(?:Requester Question(?: \/ Clarification)?[:\s]*)(.*?)(?:Referenced (?:drawings or )?documents[:\s]*|$)", summary_text, re.DOTALL | re.IGNORECASE)
                                
                                if rq_match:
                                    requester_question = rq_match.group(1).strip()
                                    rd_match = re.search(r"(?:Referenced (?:drawings or )?documents[:\s]*)(.*)", summary_text, re.DOTALL | re.IGNORECASE)
                                    if rd_match:
                                        referenced_docs = rd_match.group(1).strip()
                                        if referenced_docs in requester_question:
                                            requester_question = requester_question.replace(referenced_docs, "").strip()
                                            requester_question = re.sub(r"Referenced (?:drawings or )?documents[:\s]*", "", requester_question, flags=re.IGNORECASE).strip()
                                
                                if requester_question == "N/A" and referenced_docs == "N/A":
                                    requester_question = summary_text
                                    rfi_summary_placeholder.markdown(f"**Requester Question / Clarification:** {requester_question if requester_question else 'N/A'}")
                                    rfi_summary_placeholder.markdown(f"**Referenced drawings or documents:** N/A")
                                    rfi_summary_placeholder.markdown("---")
                                    rfi_summary_placeholder.markdown(f"**Full Summary:**\n{summary_text}")
                                    st.info("Note: No specific 'Requester Question' or 'Referenced Documents' headers were found in the summary. Displaying full summary as the question.")
                                else:
                                    rfi_summary_placeholder.markdown(f"**Requester Question / Clarification:** {requester_question if requester_question else 'N/A'}")
                                    rfi_summary_placeholder.markdown(f"**Referenced drawings or documents:** {referenced_docs if referenced_docs else 'N/A'}")
                                    rfi_summary_placeholder.markdown("---")
                                    rfi_summary_placeholder.markdown(f"**Full Summary:**\n{summary_text}")

                            else:
                                st.error("Summarization failed: No summary returned from the API.")
                        except Exception as e:
                            st.error(f"An error occurred during summarization: {e}")
                            st.exception(e)
        else:
            st.error("Unsupported file type for RFI Summarizer. Please upload a PDF file.")

elif page_selection == "Daily Site Report Generator":
    st.header("📊 Daily Site Report Generator")
    st.markdown("Generate a professional daily site report from site inputs and an optional photo.")

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
        value=datetime.now().strftime("%Y-%m-%d"),
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

    if report_photo:
        st.image(report_photo, caption=report_photo.name, width=200)

    generate_button_clicked = st.button("Generate Report", disabled=not api_base_url, key="generate_report_button")

    weather_error = st.empty()
    manpower_error = st.empty()
    progress_error = st.empty()
    safety_error = st.empty()
    date_error = st.empty()
    photo_error = st.empty()
    report_generation_error = st.empty()

    if generate_button_clicked:
        weather_error.empty()
        manpower_error.empty()
        progress_error.empty()
        safety_error.empty()
        date_error.empty()
        photo_error.empty()
        report_generation_error.empty()

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
