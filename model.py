import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

def generate_response(system_prompt, user_prompt):
    """
    Generate a response using Gemini LLM.
    
    Args:
        system_prompt (str): The system prompt to set the context for the model
        user_prompt (str): The user's input/question
    
    Returns:
        str: The model's response
    """
    # Get API key from environment variables
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    # Initialize the OpenAI client with Gemini API
    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    
    # Create chat completion request
    response = client.chat.completions.create(
        model="gemini-2.0-flash-lite",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    # Return the generated response
    return response.choices[0].message.content

# Example usage
if __name__ == "__main__":
    system_prompt = "You are a helpful assistant."
    user_prompt = "Explain to me how AI works"
    
    result = generate_response(system_prompt, user_prompt)
    print(result)
