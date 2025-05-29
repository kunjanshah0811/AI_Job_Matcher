import os
from dotenv import load_dotenv
from openai import OpenAI
from groq import Groq
import streamlit as st

load_dotenv()

def generate_response(system_prompt: str, user_prompt: str, temp: float = 0.7):
    """
    Generate a response using Gemini or Groq LLM.
    
    Args:
        system_prompt (str): The system prompt to set the context for the model
        user_prompt (str): The user's input/question
    
    Returns:
        str: The model's response
    """
    try:
        # Try Gemini first
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Initialize the OpenAI client with Gemini API
        client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        st.info("🤖 Using Gemini model")  # Debug message
        # Create chat completion request
        response = client.chat.completions.create(
            model="gemini-2.0-flash-lite",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temp
        )
        
        # Return the generated response
        return response.choices[0].message.content
    
    except Exception as e:
        # Fallback to Groq if Gemini fails
        try:
            groq_key = os.getenv("GROQ_API_KEY")
            if not groq_key:
                raise ValueError("GROQ_API_KEY not found in environment variables")
            
            groq_client = Groq(api_key=groq_key)
            st.warning("⚠️ Gemini failed, using Groq model")  # Debug message

            response = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=temp
            )
            
            return response.choices[0].message.content
            
        except Exception as groq_error:
            st.error(f"Both models failed. Gemini error: {e}, Groq error: {groq_error}")
            raise

# Example usage
if __name__ == "__main__":
    system_prompt = "You are a helpful assistant."
    user_prompt = "Explain to me how AI works"
    
    result = generate_response(system_prompt, user_prompt)
    print(result)
