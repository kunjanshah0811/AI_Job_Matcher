import speech_recognition as sr
import sounddevice as sd
import wavio as wv
import os
import time

def audio_to_text():
    """
    Captures speech input from the microphone and converts it to text.
    Returns the transcribed text or handles error message.
    """
    freq = 44100
    duration = 180
    channels = 1
    recording_file = "recording.wav"

    print("🎤 You can answer now")
    print(f"Recording will automatically stop after {duration} seconds")
        
    recording = sd.rec(int(duration*freq), samplerate=freq, channels=channels)
    
    # Show progress during recording
    for i in range(duration):
        time.sleep(1)
        seconds_left = duration - i - 1
        print(f"⏱️ {seconds_left} seconds remaining...", end="\r")
    
    print("Thank you for your answer")
    sd.wait()
    wv.write(recording_file, recording, freq, sampwidth=2)

    r = sr.Recognizer()
    text = None

    try:
        with sr.AudioFile(recording_file) as source:
            audio = r.record(source)
            
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said. Please try again.")
        return None
    except sr.RequestError as e:
        print(f"Speech recognition service error: {e}")
        return None
    finally:
        if os.path.exists(recording_file):
            os.remove(recording_file)

if __name__ == "__main__":
    audio_to_text()