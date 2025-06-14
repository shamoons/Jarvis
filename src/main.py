from llm.llama_client import LlamaClient
import speech_recognition as sr
import time
import sys
from config.settings import settings

def check_microphone():
    """Check if microphone is available and working."""
    try:
        # List available microphones
        print("\nAvailable microphones:")
        mics = sr.Microphone.list_microphone_names()
        for index, name in enumerate(mics):
            print(f"Microphone {index}: {name}")
        
        # Try to initialize with default microphone
        mic = sr.Microphone()
        print("\nTesting microphone...")
        with mic as source:
            recognizer = sr.Recognizer()
            # Set proper timing parameters
            recognizer.pause_threshold = 0.8
            recognizer.non_speaking_duration = 0.5
            recognizer.dynamic_energy_threshold = True
            recognizer.energy_threshold = 50  # Much more sensitive
            print("Microphone is working!")
            return True, mic
    except Exception as e:
        print(f"Error: Could not access microphone. {e}")
        print("Please make sure your microphone is connected and working.")
        return False, None

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
    if not mic:
        print("No microphone available")
        return False
        
    try:
        with mic as source:
            print(f"\nListening for wake word '{wake_word}'...")
            try:
                # Set proper timing parameters before adjusting for ambient noise
                recognizer.pause_threshold = 0.8
                recognizer.non_speaking_duration = 0.5
                recognizer.energy_threshold = 50  # Much more sensitive
                recognizer.adjust_for_ambient_noise(source, duration=1.0)  # Longer calibration
                
                print("Ready to hear you...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
                text = recognizer.recognize_google(audio).lower().strip()
                print(f"Heard: {text}")
                
                if wake_word.lower() in text:
                    print(f"[Wake word '{wake_word}' detected!]")
                    return True
                return False
            except sr.WaitTimeoutError:
                print("No speech detected")
                return False
            except sr.UnknownValueError:
                print("Could not understand audio")
                return False
            except sr.RequestError as e:
                print(f"Error with speech recognition service: {e}")
                return False
    except Exception as e:
        print(f"Error in wake word detection: {e}")
        import traceback
        traceback.print_exc()
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
            recognizer.energy_threshold = 50  # Much more sensitive
            recognizer.pause_threshold = 0.8
            recognizer.non_speaking_duration = 0.5
            
            print("Ready to hear your command...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
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
    success, mic = check_microphone()
    if not success:
        return

    # Initialize components
    recognizer = sr.Recognizer()
    client = LlamaClient()
    
    print("\n=== Jarvis Voice Assistant ===")
    print("Initializing...")
    print(f"Wake word is set to: '{settings.WAKE_WORD}'")
    print("Make sure your microphone is working and you're in a quiet environment")
    print("Speak clearly and at a normal volume")
    print("Press Ctrl+C to exit the program")
    
    # Initial greeting
    client.speak(f"Jarvis is ready. Say '{settings.WAKE_WORD}' to wake me up!")
    
    try:
        while True:
            try:
                # Wait for wake word with timeout
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
                
                # Add a small delay to prevent CPU overuse
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\nExiting program...")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(1)
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    finally:
        print("\nShutting down Jarvis...")

if __name__ == "__main__":
    main() 