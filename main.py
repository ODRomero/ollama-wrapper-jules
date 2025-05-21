from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ollama import Client

# Create a FastAPI app instance
app = FastAPI()

# Define a Pydantic model for the request body
class GenerateRequest(BaseModel):
    model: str
    prompt: str | None = None
    messages: list[dict] | None = None

# Create a POST endpoint /generate
@app.post("/generate")
async def generate(request: GenerateRequest):
    if not request.prompt and (not request.messages or len(request.messages) == 0):
        raise HTTPException(
            status_code=422,
            detail="Either 'prompt' or a non-empty 'messages' list must be provided."
        )

    try:
        # Initialize an ollama.Client instance
        client = Client()

        message_list_to_send = []
        if request.messages and len(request.messages) > 0:
            message_list_to_send = request.messages
        elif request.prompt:
            message_list_to_send = [{'role': 'user', 'content': request.prompt}]
        # The case where both are empty/None is caught by the check above

        # Call client.chat()
        response = client.chat(
            model=request.model,
            messages=message_list_to_send
        )
        # Return the response dictionary directly
        return response
    except Exception as e:
        # Basic error handling
        raise HTTPException(status_code=500, detail=f"Error interacting with Ollama API: {str(e)}")
