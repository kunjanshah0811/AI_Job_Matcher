import whisper
import streamlit as st
import pyttsx3


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

def text_to_audio(text, filepath):
    """Converts text to speech using pyttsx3"""
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("rate", 125) 
    engine.setProperty("voice", voices[0].id)
    # engine.say(text)
    engine.save_to_file(text, filepath)
    engine.runAndWait()

# def text_to_audio(text=None, filepath=None):
#     client = InferenceClient(
#         provider="fal-ai",
#         api_key=os.getenv("TEXT_TO_AUDIO"),
#     )
#     # audio is returned as bytes
#     audio_bytes=client.text_to_speech(
#         text,
#         model="hexgrad/Kokoro-82M",
#     )

#     with open(filepath, "wb") as f:
#         f.write(audio_bytes)



if __name__ == "__main__":
    text_to_audio("Test speech conversion")