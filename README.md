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

*   `model` (string, required): The name of the Ollama model to use (e.g., "llama3").
*   `prompt` (string, optional): The prompt to send to the model for a single-turn interaction.
*   `messages` (list of objects, optional): A list of message objects for conversational context. Each object should have:
    *   `role` (string): The role of the sender (e.g., "user", "assistant").
    *   `content` (string): The content of the message.

**Important:** Either 'prompt' or a non-empty 'messages' list must be provided.
*   If `messages` is provided and is not empty, it will be used for conversational context, and `prompt` will be ignored.
*   If `messages` is not provided or is empty, `prompt` must be provided and will be used to initiate a new conversation with a single user message.

---

**Examples for Single-Turn Interaction (using `prompt`):**

**`curl`:**
```bash
curl -X POST "http://127.0.0.1:8000/generate" -H "Content-Type: application/json" -d '{
  "model": "llama3",
  "prompt": "Why is the sky blue?"
}'
```
*This example uses the `prompt` field for a single-turn interaction.*

**Python `requests`:**
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
*This example uses the `prompt` field for a single-turn interaction.*

---

**Examples for Conversational Interaction (using `messages`):**

**`curl`:**
```bash
curl -X POST "http://127.0.0.1:8000/generate" -H "Content-Type: application/json" -d '{
  "model": "llama3",
  "messages": [
    {"role": "user", "content": "Hello! Can you tell me about the history of large language models?"},
    {"role": "assistant", "content": "Certainly! The history of large language models dates back to the mid-20th century... (summary of response A)"},
    {"role": "user", "content": "That''s interesting. What were some of the key breakthroughs?"}
  ]
}'
```

**Python `requests`:**
```python
import requests
import json

url = "http://127.0.0.1:8000/generate"
payload = {
    "model": "llama3",
    "messages": [
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "The capital of France is Paris."},
        {"role": "user", "content": "What is a famous landmark there?"}
    ]
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
