import os
import pytest
import requests
import socket
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Watson credentials
WATSONX_APIKEY = os.getenv("WATSONX_APIKEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
WATSONX_URL = os.getenv("WATSONX_URL")


@pytest.fixture(scope="module")
def hostname():
    """Extract hostname from URL"""
    return WATSONX_URL.replace("https://", "").replace("http://", "").split("/")[0]


@pytest.fixture(scope="module")
def token():
    """Get IBM Cloud IAM token using API key"""
    print("\nGetting IAM token...")
    iam_url = "https://iam.cloud.ibm.com/identity/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }

    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": WATSONX_APIKEY
    }

    try:
        response = requests.post(iam_url, headers=headers, data=data, timeout=10)
        if response.status_code == 200:
            token = response.json().get("access_token")
            print("✅ Successfully obtained IAM token")
            return token
        else:
            print(f"❌ Failed to get IAM token. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request to IAM endpoint failed: {e}")
        return None


def test_credentials_exist():
    """Test that required credentials exist"""
    assert WATSONX_URL, "WATSONX_URL environment variable is missing"
    assert WATSONX_APIKEY, "WATSONX_APIKEY environment variable is missing"
    assert WATSONX_PROJECT_ID, "WATSONX_PROJECT_ID environment variable is missing"


def test_dns_resolution(hostname):
    """Test if hostname can be resolved"""
    try:
        ip_address = socket.gethostbyname(hostname)
        print(f"✅ Resolved {hostname} to {ip_address}")
        assert ip_address, "No IP address returned"
    except socket.gaierror as e:
        pytest.fail(f"Failed to resolve hostname: {e}")


def test_connection():
    """Test if we can connect to the URL"""
    try:
        response = requests.get(WATSONX_URL, timeout=5)
        print(f"✅ Connection successful. Status code: {response.status_code}")
        # Note: It's possible to get non-200 codes but still have connectivity
        assert response.status_code < 500, "Server error"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Connection failed: {e}")


def test_watsonx_endpoint(token):
    """Test WatsonX ML API endpoint"""
    if not token:
        pytest.skip("No token available, skipping API test")

    ml_url = f"{WATSONX_URL}/ml/v1/models?version=2024-03-13"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(ml_url, headers=headers, timeout=10)
        print(f"Response status: {response.status_code}")
        assert response.status_code == 200, f"API request failed: {response.text}"
        data = response.json()
        assert "resources" in data, "Expected 'resources' in response"
        print(f"✅ Found {len(data['resources'])} models")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to ML API failed: {e}")


def test_simple_generation(token):
    """Test a simple text generation request"""
    if not token:
        pytest.skip("No token available, skipping generation test")

    generation_url = f"{WATSONX_URL}/ml/v1/text/generation?version=2024-03-13"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "model_id": "mistralai/mistral-large",
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 50,
            "min_new_tokens": 1,
            "stop_sequences": [],
            "repetition_penalty": 1
        },
        "input": "Hello, how are you?",
        "project_id": WATSONX_PROJECT_ID
    }

    try:
        response = requests.post(generation_url, headers=headers, json=data, timeout=30)
        assert response.status_code == 200, f"Generation failed: {response.text}"
        result = response.json()
        assert "results" in result, "Expected 'results' in response"
        assert len(result["results"]) > 0, "No results returned"
        assert "generated_text" in result["results"][0], "No generated text found"
        print(f"✅ Generated text: {result['results'][0]['generated_text'][:50]}...")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to generation API failed: {e}")


def test_litellm_integration(token):
    """Test if litellm can connect to WatsonX"""
    if not token:
        pytest.skip("No token available, skipping LiteLLM test")

    try:
        import litellm

        # Configure LiteLLM
        os.environ["WATSONX_APIKEY"] = WATSONX_APIKEY
        os.environ["WATSONX_PROJECT_ID"] = WATSONX_PROJECT_ID
        os.environ["WATSONX_URL"] = WATSONX_URL

        # Create completion parameters
        params = {
            "model": "mistralai/mistral-large",
            "provider": "watsonx",
            "messages": [{"role": "user", "content": "Say hello in one sentence."}],
            "max_tokens": 25,
        }

        response = litellm.completion(**params)

        assert response, "No response from LiteLLM"
        assert hasattr(response, 'choices'), "No choices in response"
        assert len(response.choices) > 0, "Empty choices in response"
        assert hasattr(response.choices[0], 'message'), "No message in first choice"
        assert hasattr(response.choices[0].message, 'content'), "No content in message"

        print(f"✅ LiteLLM response: {response.choices[0].message.content}")
    except ImportError:
        pytest.skip("LiteLLM is not installed")
    except Exception as e:
        pytest.fail(f"LiteLLM integration test failed: {e}")