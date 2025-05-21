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
    # Missing 'model' - Pydantic validation
    response = client.post("/generate", json={"prompt": "test"}) # 'model' is required by Pydantic
    assert response.status_code == 422
    # Ensure the error is about 'model' being missing if possible, or just check 422
    # For example, Pydantic v2 might return:
    # {'detail': [{'type': 'missing', 'loc': ['body', 'model'], 'msg': 'Field required', 'input': {'prompt': 'test'}}]}
    # For simplicity, just checking status 422 is often sufficient for this test's scope.

    # Test with 'model' but no prompt or messages (covered by specific tests below, but good for Pydantic check)
    response = client.post("/generate", json={"model": "llama3"})
    assert response.status_code == 422 
    assert response.json() == {"detail": "Either 'prompt' or a non-empty 'messages' list must be provided."}


@patch('ollama.Client')
def test_generate_with_conversation_history(MockOllamaClient):
    mock_ollama_instance = MockOllamaClient.return_value
    messages_payload = [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi there!"},
        {"role": "user", "content": "How are you?"}
    ]
    mock_response_content = "I'm doing well, thank you for asking!"
    mock_ollama_response = {
        "model": "llama3",
        "created_at": "2023-10-27T10:00:00Z",
        "message": {"role": "assistant", "content": mock_response_content},
        "done": True
    }
    mock_ollama_instance.chat.return_value = mock_ollama_response

    response = client.post("/generate", json={"model": "llama3", "messages": messages_payload})

    assert response.status_code == 200
    assert response.json() == mock_ollama_response
    mock_ollama_instance.chat.assert_called_once_with(
        model="llama3",
        messages=messages_payload
    )

@patch('ollama.Client')
def test_generate_messages_takes_precedence_over_prompt(MockOllamaClient):
    mock_ollama_instance = MockOllamaClient.return_value
    messages_payload = [{"role": "user", "content": "From messages"}]
    mock_response_content = "Response based on messages"
    mock_ollama_response = {
        "model": "llama3",
        "message": {"role": "assistant", "content": mock_response_content},
        "done": True
    }
    mock_ollama_instance.chat.return_value = mock_ollama_response

    response = client.post(
        "/generate",
        json={"model": "llama3", "prompt": "This should be ignored", "messages": messages_payload}
    )

    assert response.status_code == 200
    assert response.json()["message"]["content"] == mock_response_content
    mock_ollama_instance.chat.assert_called_once_with(
        model="llama3",
        messages=messages_payload
    )

@patch('ollama.Client')
def test_generate_empty_messages_list_with_prompt(MockOllamaClient):
    mock_ollama_instance = MockOllamaClient.return_value
    prompt_payload = "Use this prompt"
    expected_messages_to_ollama = [{"role": "user", "content": prompt_payload}]
    mock_response_content = "Response based on prompt"
    mock_ollama_response = {
        "model": "llama3",
        "message": {"role": "assistant", "content": mock_response_content},
        "done": True
    }
    mock_ollama_instance.chat.return_value = mock_ollama_response

    response = client.post(
        "/generate",
        json={"model": "llama3", "prompt": prompt_payload, "messages": []} # Empty messages list
    )

    assert response.status_code == 200
    assert response.json()["message"]["content"] == mock_response_content
    mock_ollama_instance.chat.assert_called_once_with(
        model="llama3",
        messages=expected_messages_to_ollama
    )

def test_generate_missing_prompt_and_messages():
    response = client.post("/generate", json={"model": "llama3"}) # Neither prompt nor messages
    assert response.status_code == 422
    assert response.json() == {"detail": "Either 'prompt' or a non-empty 'messages' list must be provided."}

def test_generate_empty_messages_list_and_no_prompt():
    response = client.post("/generate", json={"model": "llama3", "messages": []}) # Empty messages, no prompt
    assert response.status_code == 422
    assert response.json() == {"detail": "Either 'prompt' or a non-empty 'messages' list must be provided."}

@patch('ollama.Client')
def test_generate_ollama_error_with_messages(MockOllamaClient):
    mock_ollama_instance = MockOllamaClient.return_value
    mock_ollama_instance.chat.side_effect = Exception("Ollama connection error with messages")
    messages_payload = [{"role": "user", "content": "Test with messages"}]

    response = client.post("/generate", json={"model": "llama3", "messages": messages_payload})

    assert response.status_code == 500
    assert response.json() == {"detail": "Error interacting with Ollama API: Ollama connection error with messages"}
    mock_ollama_instance.chat.assert_called_once_with(
        model="llama3",
        messages=messages_payload
    )
