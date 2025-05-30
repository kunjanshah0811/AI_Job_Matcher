import speech_recognition as sr
import sounddevice as sd
import wavio as wv
import os
import time
import pyttsx3

def audio_to_text(audio_file_path=None):
    """
    Converts audio file to text using speech recognition.
    If audio_file_path is provided, uses that file. Otherwise captures from microphone.
    Returns the transcribed text or None if error.
    """
    r = sr.Recognizer()
    text = None
    
    try:
        if audio_file_path:
            # Use provided audio file
            with sr.AudioFile(audio_file_path) as source:
                audio = r.record(source)
        else:
            # Original microphone capture logic
            freq = 44100
            duration = 180
            channels = 1
            recording_file = "recording.wav"
            
            print("🎤 You can answer now")
            print(f"Recording will automatically stop after {duration} seconds")
                     
            recording = sd.rec(int(duration*freq), samplerate=freq, channels=channels)
             
            for i in range(duration):
                time.sleep(1)
                seconds_left = duration - i - 1
                print(f"⏱️ {seconds_left} seconds remaining...", end="\r")
                 
            print("Thank you for your answer")
            sd.wait()
            wv.write(recording_file, recording, freq, sampwidth=2)
            
            with sr.AudioFile(recording_file) as source:
                audio = r.record(source)
            
            # Clean up recording file
            if os.path.exists(recording_file):
                os.remove(recording_file)
                     
        text = r.recognize_google(audio)
        return text
        
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said. Please try again.")
        return None
    except sr.RequestError as e:
        print(f"Speech recognition service error: {e}")
        return None
    except Exception as e:
        print(f"Audio processing error: {e}")
        return None

def text_to_audio(text):
    engine=pyttsx3.init()
    voices=engine.getProperty("voices")
    engine.setProperty("rate",125)
    engine.setProperty("voice",voices[1].id)
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    audio_to_text()
    text_to_audio("""The key to effective software development lies in balancing technical excellence with practical solutions.
                     In my experience at TechSolutions, 
                     I implemented this philosophy by optimizing database queries which reduced load times by 40%. 
                     I'm passionate about clean code and proper documentation, which has helped my teams maintain 
                    systems efficiently over time. I'm excited to bring these skills to your cloud-based applications.""")