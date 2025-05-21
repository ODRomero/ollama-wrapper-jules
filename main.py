from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ollama import Client

# Create a FastAPI app instance
app = FastAPI()

# Define a Pydantic model for the request body
class GenerateRequest(BaseModel):
    model: str
    prompt: str

# Create a POST endpoint /generate
@app.post("/generate")
async def generate(request: GenerateRequest):
    try:
        # Initialize an ollama.Client instance
        client = Client()

        # Call client.chat()
        response = client.chat(
            model=request.model,
            messages=[
                {
                    'role': 'user',
                    'content': request.prompt,
                }
            ]
        )
        # Return the response dictionary directly
        return response
    except Exception as e:
        # Basic error handling
        raise HTTPException(status_code=500, detail=f"Error interacting with Ollama API: {str(e)}")
