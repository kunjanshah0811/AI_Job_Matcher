import speech_recognition as sr
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SpeechRecognizer:
    """
    Speech recognition module that converts user's spoken interview answers to text.
    Uses Google's free speech recognition API by default.
    """
    
    def __init__(self, recognition_service="google", timeout=10, phrase_time_limit=None):
        """
        Initialize the speech recognizer.
        
        Args:
            recognition_service (str): Speech recognition service to use (default: "google")
            timeout (int): Maximum time in seconds to wait for speech input
            phrase_time_limit (int): Maximum time in seconds for a phrase, None for no limit
        """
        self.recognizer = sr.Recognizer()
        self.recognition_service = recognition_service
        self.timeout = timeout
        self.phrase_time_limit = phrase_time_limit
        
    def adjust_for_ambient_noise(self, duration=1):
        """
        Adjust for ambient noise before recording.
        
        Args:
            duration (int): Time in seconds to sample ambient noise
        """
        try:
            with sr.Microphone() as source:
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=duration)
                logger.info("Ambient noise adjustment complete")
        except Exception as e:
            logger.error(f"Error adjusting for ambient noise: {e}")
            
    def listen(self):
        """
        Listen for speech input and convert to text.
        
        Returns:
            str: Transcribed text or None if an error occurred
        """
        try:
            with sr.Microphone() as source:
                logger.info("Listening... Please speak your answer.")
                audio = self.recognizer.listen(
                    source, 
                    timeout=self.timeout,
                    phrase_time_limit=self.phrase_time_limit
                )
                
            logger.info("Processing speech...")
            
            if self.recognition_service == "google":
                text = self.recognizer.recognize_google(audio)
            elif self.recognition_service == "whisper":
                # Requires whisper installation
                text = self.recognizer.recognize_whisper(audio)
            else:
                logger.error(f"Unsupported recognition service: {self.recognition_service}")
                return None
                
            logger.info("Speech recognition successful")
            return text
            
        except sr.WaitTimeoutError:
            logger.warning("No speech detected within timeout period")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return None
        except Exception as e:
            logger.error(f"Speech recognition error: {e}")
            return None
            
    def record_interview_answer(self, question_number):
        """
        Record and transcribe a complete interview answer.
        
        Args:
            question_number (int): Current question number for logging
            
        Returns:
            str: Transcribed answer or error message
        """
        logger.info(f"Recording answer for question {question_number}")
        
        # Adjust for ambient noise before recording
        self.adjust_for_ambient_noise()
        
        # Get the spoken answer
        answer = self.listen()
        
        if answer:
            logger.info(f"Answer recorded: {answer[:50]}...")
            return answer
        else:
            error_msg = "Sorry, I couldn't capture your answer. Please try again."
            logger.warning(error_msg)
            return error_msg


# Example usage
if __name__ == "__main__":
    recognizer = SpeechRecognizer()
    print("Testing speech recognition...")
    
    # Test speech recognition
    text = recognizer.record_interview_answer(1)
    print(f"Recognized: {text}")