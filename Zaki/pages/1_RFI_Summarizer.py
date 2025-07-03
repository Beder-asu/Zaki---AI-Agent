import streamlit as st
import os
import re
from services.summarizer import summarize_rfi_api

# Access API config from session_state set in app.py
api_base_url = st.session_state.api_base_url
api_token = st.session_state.api_token

st.header("📝 RFI Summarizer")
st.markdown("Upload an RFI document (PDF) to get a structured summary.")

rfi_uploaded_file = st.file_uploader(
    "Upload an RFI Document (.pdf)",
    type=["pdf"], # Only PDF for summarization as per backend spec
    accept_multiple_files=False,
    key="rfi_uploader" # Unique key for this uploader
)

rfi_summary_placeholder = st.empty() # Placeholder for RFI summary display

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
                        # Ensure all 4 arguments are passed here
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
