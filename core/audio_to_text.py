import speech_recognition as sr

def listen_for_speech():
    """
    Captures speech input from the microphone and converts it to text .
    Returns the transcribed text or handles error message.
    """
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Please speak your answer :")
        audio=r.listen(source)

    try:
        text=r.recognize_google(audio)
        print("You said : "+ text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I did not understand you.")
    except sr.RequestError as e :
        print(f"Could not request results ; {e}")

if __name__=="__main__":
    listen_for_speech()