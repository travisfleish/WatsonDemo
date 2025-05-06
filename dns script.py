import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def discover_correct_endpoint():
    """Test various IBM Watson endpoints to find the correct one"""
    print("Attempting to discover the correct IBM Watson ML endpoint...")

    # Get your IAM token first
    iam_url = "https://iam.cloud.ibm.com/identity/token"
    apikey = os.getenv("WATSONX_APIKEY")

    # Get IAM token
    response = requests.post(
        iam_url,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": apikey},
        timeout=10
    )

    if response.status_code != 200:
        print(f"❌ Failed to get IAM token: {response.status_code}")
        return

    token = response.json().get("access_token")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # List of potential endpoints to try
    potential_endpoints = [
        "https://us-south.ml.cloud.ibm.com",  # US South region
        "https://eu-de.ml.cloud.ibm.com",  # Frankfurt region
        "https://eu-gb.ml.cloud.ibm.com",  # London region
        "https://jp-tok.ml.cloud.ibm.com",  # Tokyo region
        "https://au-syd.ml.cloud.ibm.com",  # Sydney region
        "https://jp-osa.ml.cloud.ibm.com",  # Osaka region
        "https://ca-tor.ml.cloud.ibm.com",  # Toronto region
        "https://br-sao.ml.cloud.ibm.com",  # Sao Paulo region
        "https://us.ml.cloud.ibm.com",  # Generic US endpoint
        "https://api.ml.cloud.ibm.com",  # Generic API endpoint
        "https://ml.cloud.ibm.com",  # Root endpoint
    ]

    # Test each endpoint
    for endpoint in potential_endpoints:
        try:
            print(f"Testing endpoint: {endpoint}")
            test_url = f"{endpoint}/ml/v1/models?version=2024-03-13"
            response = requests.get(test_url, headers=headers, timeout=10)

            if response.status_code == 200:
                print(f"✅ SUCCESS! Found working endpoint: {endpoint}")
                print("Update your .env file with this endpoint.")
                return endpoint
            else:
                print(f"❌ Failed with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed: {e}")

    print("❌ Could not find a working endpoint.")
    return None


if __name__ == "__main__":
    discover_correct_endpoint()