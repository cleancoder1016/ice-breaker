import os
import json
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

# --- Constants ---
PROXYCURL_API_ENDPOINT = "https://nubela.co/proxycurl/api/v2/linkedin"
# *** FIX: Use the RAW URL for the mock data Gist ***
MOCK_PROFILE_URL = "https://gist.githubusercontent.com/cleancoder1016/31ba5799295d7ef2b666b4d3f35176cd/raw/840f4db208a03f33f9fa7c2eccbd4f22e9be569f/linkedin-info.json"
# Define default output file path (consider making it relative or configurable)
DEFAULT_OUTPUT_FILENAME = "/home/minimalist/langChain/ice_breaker/info.json"


def scrape_linkedin_profile(
    linkedin_profile_url: str,
    output_filename: str | None = DEFAULT_OUTPUT_FILENAME, # Allow None to skip saving
    mock: bool = False
):
    """
    Fetches LinkedIn profile data using ProxyCurl (or a mock source),
    cleans it, optionally saves it, and returns the cleaned data.

    Args:
        linkedin_profile_url: The URL of the LinkedIn profile (used if mock=False).
        output_filename: Path to save the cleaned JSON data. If None, saving is skipped.
        mock: If True, fetches data from MOCK_PROFILE_URL.

    Returns:
        A dictionary containing the cleaned profile data, or None if a critical error occurred.
    """
    response = None
    request_url = "" # For logging purposes

    # --- 1. Fetch Data ---
    try:
        if mock:
            request_url = MOCK_PROFILE_URL
            print(f"--- MOCK MODE: Fetching data from {request_url} ---")
            response = requests.get(request_url, timeout=10)
        else:
            request_url = PROXYCURL_API_ENDPOINT
            print(f"--- LIVE MODE: Fetching data for {linkedin_profile_url} from {request_url} ---")
            api_key = os.environ.get("PROXYURL_API_KEY")
            if not api_key:
                print("Error: PROXYURL_API_KEY environment variable not set.", file=sys.stderr)
                return None # Cannot proceed without API key in live mode

            headers = {"Authorization": f'Bearer {api_key}'}
            params = {"url": linkedin_profile_url}
            response = requests.get(request_url, params=params, headers=headers, timeout=10)

        # *** FIX: Check for HTTP errors immediately after the request ***
        response.raise_for_status()

    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors (e.g., 404 Not Found, 401 Unauthorized, 500 Internal Server Error)
        print(f"HTTP Error fetching {request_url}: {e.response.status_code} - {e.response.reason}", file=sys.stderr)
        # Log response body if available, it might contain useful error details from the API
        if response is not None:
            print(f"Response Body: {response.text[:500]}...", file=sys.stderr)
        return None # Cannot proceed
    except requests.exceptions.RequestException as e:
        # Handle other network/request issues (DNS failure, connection timeout, etc.)
        print(f"Error during request to {request_url}: {e}", file=sys.stderr)
        return None # Cannot proceed

    # --- 2. Parse JSON ---
    # *** FIX: Wrap response.json() in a try-except block ***
    try:
        data = response.json()
        print("Successfully parsed JSON response.")
    except requests.exceptions.JSONDecodeError as e: # Catch requests' version of the error
        print(f"Error: Failed to decode JSON response from {request_url}.", file=sys.stderr)
        print(f"Details: {e.msg}, Line: {e.lineno}, Col: {e.colno}", file=sys.stderr)
        # Print the beginning of the text that failed to parse
        print(f"Response text (first 200 chars): {response.text[:200]}...", file=sys.stderr)
        return None # Cannot proceed if JSON is invalid

    # --- 3. Clean Data ---
    try:
        # Check if data is actually a dictionary before attempting dict operations
        if not isinstance(data, dict):
            print(f"Warning: Expected dictionary data from API but got {type(data)}. Cannot clean.", file=sys.stderr)
            # Depending on requirements, you might return data as is, or return None
            # return data # Option 1: Return the non-dict data
            return None   # Option 2: Treat as failure if not a dict

        # Perform cleaning (using slightly safer .get and type checking)
        cleaned_data = {
            k: v
            for k, v in data.items()
            # Removed duplicate "" check
            if v not in ([], "", None) and k not in ["people_also_viewed", "certifications"]
        }

        # Clean groups - check if 'groups' exists and is a list
        groups = cleaned_data.get("groups")
        if isinstance(groups, list):
            for group_dict in groups:
                # Check if item in list is a dictionary before popping
                if isinstance(group_dict, dict):
                    group_dict.pop("profile_pic_url", None) # Use default for pop

        data = cleaned_data # Assign cleaned data back
        print("Data cleaning complete.")

    except Exception as e:
        # Catch potential errors during cleaning (e.g., unexpected data structure)
        print(f"Error during data cleaning phase: {e}", file=sys.stderr)
        # Decide if you want to return partially cleaned data or fail
        # For safety, returning None might be better if cleaning fails unexpectedly
        return None

    # --- 4. Save Data (Optional) ---
    if output_filename: # Check if a filename was provided
        print(f"Attempting to save cleaned data to {output_filename}")
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            print(f"Successfully saved cleaned data to {output_filename}")
        # *** FIX: Catch file-related errors here, not JSONDecodeError ***
        except IOError as e:
            print(f"Error: Could not write data to file {output_filename}. Details: {e}", file=sys.stderr)
        except TypeError as e:
            print(f"Error: Could not serialize cleaned data to JSON for {output_filename}. Details: {e}", file=sys.stderr)
    else:
        print("Skipping file saving because no output file was specified.")

    return data # Return the final cleaned data


if __name__ == "__main__":
    # Example call using Mock mode (now points to the correct RAW gist URL)
    result = scrape_linkedin_profile(
        linkedin_profile_url="https://www.linkedin.com/in/irrelevant-for-mock-mode/",
        output_filename=DEFAULT_OUTPUT_FILENAME,
        mock=True
    )

    # Example call for Live mode (uncomment to use)
    # result = scrape_linkedin_profile(
    #     linkedin_profile_url="https://www.linkedin.com/in/siva-rama-krishna-prasad-changala-a3115a253/",
    #     output_filename="siva_info.json", # Use a different file or None
    #     mock=False
    # )

    if result:
        print("\n--- Script finished successfully ---")
        # Optionally print some of the result for verification
        # print("Sample of returned data:", json.dumps(list(result.items())[:3], indent=2))
    else:
        print("\n--- Script finished with errors ---")
        sys.exit(1) # Exit with error code if function returned None