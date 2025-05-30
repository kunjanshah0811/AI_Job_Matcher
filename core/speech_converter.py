import whisper
import streamlit as st
import pyttsx3
import os
import torch

# Set PyTorch settings to avoid thread/loop errors
torch.set_num_threads(1)
torch.set_num_interop_threads(1)

@st.cache_resource(show_spinner="Loading speech recognition model...")
def load_model():
    """Load Whisper model with optimized settings"""
    try:
        # Use CPU device and weights_only to avoid torch serialization issues
        return whisper.load_model(
            "base",
            device="cpu",
            download_root="models",
            in_memory=True
        )
    except Exception as e:
        print(f"Model loading error: {e}")
        return None

def audio_to_text(audio_file_path=None):
    """Converts audio file to text using Whisper"""
    model = load_model()
    if model is None:
        return None
    
    try:
        if audio_file_path:
            result = model.transcribe(audio_file_path, fp16=False)
            return result["text"]
        return None
        
    except Exception as e:
        print(f"Audio processing error: {e}")
        return None

def text_to_audio(text):
    """Converts text to speech using pyttsx3"""
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("rate", 125)
    engine.setProperty("voice", voices[1].id)
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    text_to_audio("Test speech conversion")