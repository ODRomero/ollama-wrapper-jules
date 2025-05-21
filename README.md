# Ollama FastAPI Wrapper

This project provides a simple FastAPI wrapper for interacting with the Ollama API.

## Setup

1.  **Install Ollama:**
    Make sure you have Ollama installed and running. Refer to the [official Ollama documentation](https://ollama.com/download) for installation instructions.

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To run the FastAPI application, use uvicorn:

```bash
uvicorn main:app --reload
```

The application will typically be available at `http://127.0.0.1:8000`.

## Usage

You can send requests to the `/generate` endpoint to interact with an Ollama model.

**Request Body:**

*   `model` (string): The name of the Ollama model to use (e.g., "llama3").
*   `prompt` (string): The prompt to send to the model.

**Example using `curl`:**

```bash
curl -X POST "http://127.0.0.1:8000/generate" -H "Content-Type: application/json" -d '{
  "model": "llama3",
  "prompt": "Why is the sky blue?"
}'
```

**Example using Python `requests`:**

```python
import requests
import json

url = "http://127.0.0.1:8000/generate"
payload = {
    "model": "llama3", # Or any other model you have pulled with ollama
    "prompt": "Tell me a joke about programming."
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, data=json.dumps(payload), headers=headers)

if response.status_code == 200:
    print("Success:")
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```
