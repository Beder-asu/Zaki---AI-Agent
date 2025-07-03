import requests
import json

def summarize_rfi_api(base_url: str, file_bytes: bytes, filename: str, api_token: str):
    """
    Calls the backend API to summarize an RFI document.

    Args:
        base_url: The base URL of the backend API (e.g., "http://localhost:8000").
        file_bytes: The content of the PDF file as bytes.
        filename: The original name of the file.
        api_token: The API token for authentication (if required by backend).

    Returns:
        A dictionary containing the API response data (e.g., {"filename": ..., "summary": ...}).

    Raises:
        requests.exceptions.RequestException: For network-related errors.
        ValueError: For API-specific errors (e.g., 400, 500 responses).
    """
    
    ENDPOINT = "/summarize-rfi/"
    API_URL = f"{base_url.rstrip('/')}{ENDPOINT}" # Ensure no double slashes

    headers = {}
    # Add Authorization header if an API token is provided
    if api_token:
        headers["Authorization"] = f"Bearer {api_token}" # Assuming Bearer token authentication

    files = {
        'file': (filename, file_bytes, 'application/pdf')
    }

    try:
        response = requests.post(API_URL, files=files, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        error_detail = "Unknown error"
        try:
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
