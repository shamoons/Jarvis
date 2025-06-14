from llm.llama_client import LlamaClient
import speech_recognition as sr
import time
import sys
from config.settings import settings

def check_microphone():
    """Check if microphone is available and working."""
    try:
        with sr.Microphone() as source:
            print("Testing microphone...")
            recognizer = sr.Recognizer()
            # Increase sensitivity for testing
            recognizer.dynamic_energy_threshold = True
            recognizer.energy_threshold = 100  # Much lower threshold
            recognizer.pause_threshold = 0.3   # Shorter pause
            recognizer.adjust_for_ambient_noise(source, duration=2)  # Longer calibration
            print("Microphone is working!")
            return True
    except Exception as e:
        print(f"Error: Could not access microphone. {e}")
        print("Please make sure your microphone is connected and working.")
        return False

def listen_for_speech(timeout=5, phrase_time_limit=5):
    """Listen for voice input and return the recognized text."""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("\nListening... (speak now)")
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            # Set timeout and phrase time limit
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print("Processing speech...")
            try:
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text.lower()  # Convert to lowercase for easier matching
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return None
    except sr.WaitTimeoutError:
        print("No speech detected within timeout")
        return None
    except Exception as e:
        print(f"Error during speech recognition: {e}")
        return None

def listen_for_wake_word(recognizer, mic, wake_word=settings.WAKE_WORD):
    """Listen for the wake word."""
    try:
        with mic as source:
            print(f"\nListening for wake word '{wake_word}'...")
            # Adjust for ambient noise each time
            recognizer.adjust_for_ambient_noise(source, duration=1)
            # Increase sensitivity
            recognizer.dynamic_energy_threshold = True
            recognizer.energy_threshold = 100  # Much lower threshold to catch quieter speech
            recognizer.pause_threshold = 0.3   # Shorter pause threshold
            recognizer.phrase_threshold = 0.1  # More sensitive to phrases
            
            print("Ready to hear you...")
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)  # Longer phrase time
            try:
                text = recognizer.recognize_google(audio).lower().strip()
                print(f"Heard: {text}")
                # More flexible wake word matching
                if wake_word.lower() in text or text in wake_word.lower():
                    print(f"[Wake word '{wake_word}' detected!]")
                    return True
                else:
                    print(f"Wake word not found in: {text}")
            except sr.UnknownValueError:
                print("Could not understand audio - please speak clearly and a bit louder")
            except sr.RequestError as e:
                print(f"Error with speech recognition service: {e}")
    except Exception as e:
        print(f"Error in wake word detection: {e}")
    return False

def listen_for_command(recognizer, mic, timeout=10):
    """Listen for a command after wake word."""
    try:
        with mic as source:
            print("\nListening for command...")
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            # Use same sensitive settings
            recognizer.dynamic_energy_threshold = True
            recognizer.energy_threshold = 100
            recognizer.pause_threshold = 0.3
            recognizer.phrase_threshold = 0.1
            
            print("Ready to hear your command...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=10)  # Longer phrase time
            try:
                text = recognizer.recognize_google(audio).strip()
                print(f"Command received: {text}")
                return text
            except sr.UnknownValueError:
                print("Could not understand command - please speak clearly and a bit louder")
                return None
            except sr.RequestError as e:
                print(f"Error with speech recognition service: {e}")
                return None
    except sr.WaitTimeoutError:
        print("No speech detected within timeout")
        return None
    except Exception as e:
        print(f"Error in command detection: {e}")
        return None

def main():
    # First check if microphone is working
    if not check_microphone():
        return

    # Initialize components
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    client = LlamaClient()
    
    print("\n=== Jarvis Voice Assistant ===")
    print("Initializing...")
    print(f"Wake word is set to: '{settings.WAKE_WORD}'")
    print("Make sure your microphone is working and you're in a quiet environment")
    print("Speak clearly and at a normal volume")
    
    # Initial greeting
    client.speak(f"Jarvis is ready. Say '{settings.WAKE_WORD}' to wake me up!")
    
    while True:
        try:
            # Wait for wake word
            if listen_for_wake_word(recognizer, mic):
                client.speak("Yes, I'm listening")
                
                # Listen for command
                command = listen_for_command(recognizer, mic)
                if command:
                    print(f"\nYou: {command}")
                    response = client.chat(command)
                    print(f"Jarvis: {response}")
                    client.speak(response)
                else:
                    client.speak("I didn't catch that. Please try again.")
        except Exception as e:
            print(f"Error in main loop: {e}")
            client.speak("I encountered an error. Please try again.")
            time.sleep(1)  # Brief pause before continuing

if __name__ == "__main__":
    main() 