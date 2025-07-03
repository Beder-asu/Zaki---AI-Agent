import requests
import json

def generate_daily_report_api(base_url: str, report_data: dict, photo_file: tuple = None, api_token: str = None):
    """
    Calls the backend API to generate a daily site report.

    Args:
        base_url: The base URL of the backend API (e.g., "http://localhost:8000").
        report_data: A dictionary containing text inputs (weather, manpower, progress, safety, date).
        photo_file: An optional tuple (filename, file_bytes, mime_type) for the photo.
        api_token: An optional API token for authentication.

    Returns:
        The content of the generated .docx file as bytes if successful.

    Raises:W
        requests.exceptions.RequestException: For network-related errors.
        ValueError: For API-specific errors (e.g., 400, 500 responses).
    """
    
    ENDPOINT = "/generate-daily-report/"
    API_URL = f"{base_url.rstrip('/')}{ENDPOINT}"

    headers = {}
    if api_token:
        headers["Authorization"] = f"Bearer {api_token}"

    files = {}
    if photo_file:
        # photo_file is (filename, file_bytes, mime_type)
        files['photos'] = photo_file

    try:
        # requests.post handles multipart/form-data automatically when 'files' is used
        # and 'data' contains other form fields.
        response = requests.post(API_URL, files=files, data=report_data, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        # For a file download, we return the raw content
        return response.content
    except requests.exceptions.HTTPError as http_err:
        error_detail = "Unknown error"
        try:
            # Attempt to parse JSON error detail if available
            error_json = response.json()
            if "detail" in error_json:
                error_detail = error_json["detail"]
        except json.JSONDecodeError:
            error_detail = response.text # Fallback to raw text if not JSON
        raise ValueError(f"API Error {response.status_code}: {error_detail}") from http_err
    except requests.exceptions.ConnectionError as conn_err:
        raise requests.exceptions.ConnectionError(f"Could not connect to the backend API at {API_URL}. Please ensure the backend is running.") from conn_err
    except requests.exceptions.Timeout as timeout_err:
        raise requests.exceptions.Timeout("The request to the backend API timed out.") from timeout_err
    except requests.exceptions.RequestException as req_err:
        raise requests.exceptions.RequestException(f"An unexpected error occurred during the API request: {req_err}") from req_err
