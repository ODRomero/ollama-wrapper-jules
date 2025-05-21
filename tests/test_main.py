import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Adjust the import path if your main.py is in a subdirectory (e.g., app.main)
from main import app 

client = TestClient(app)

@patch('ollama.Client')
def test_generate_success(MockOllamaClient):
    # Configure the mock
    mock_ollama_instance = MockOllamaClient.return_value
    mock_response = {
        "model": "llama3",
        "created_at": "2023-10-26T12:00:00Z",
        "message": {
            "role": "assistant",
            "content": "The sky is blue due to Rayleigh scattering."
        },
        "done": True
    }
    mock_ollama_instance.chat.return_value = mock_response

    # Make the request
    response = client.post("/generate", json={"model": "llama3", "prompt": "Why is the sky blue?"})

    # Assertions
    assert response.status_code == 200
    assert response.json() == mock_response
    mock_ollama_instance.chat.assert_called_once_with(
        model="llama3",
        messages=[{'role': 'user', 'content': "Why is the sky blue?"}]
    )

@patch('ollama.Client')
def test_generate_ollama_error(MockOllamaClient):
    # Configure the mock to raise an exception
    mock_ollama_instance = MockOllamaClient.return_value
    mock_ollama_instance.chat.side_effect = Exception("Ollama connection error")

    # Make the request
    response = client.post("/generate", json={"model": "llama3", "prompt": "What happens on error?"})

    # Assertions
    assert response.status_code == 500
    assert response.json() == {"detail": "Error interacting with Ollama API: Ollama connection error"}
    mock_ollama_instance.chat.assert_called_once_with(
        model="llama3",
        messages=[{'role': 'user', 'content': "What happens on error?"}]
    )

def test_generate_invalid_request_body():
    # Missing 'prompt'
    response = client.post("/generate", json={"model": "llama3"})
    assert response.status_code == 422 # Unprocessable Entity for Pydantic validation errors

    # Missing 'model'
    response = client.post("/generate", json={"prompt": "test"})
    assert response.status_code == 422
