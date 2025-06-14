from llama_cpp import Llama
from config.settings import settings
import win32com.client
import os
import threading
import time

class BackgroundTaskManager:
    def __init__(self):
        self.tasks = []

    def run_in_background(self, func, *args, **kwargs):
        thread = threading.Thread(target=self._wrapper, args=(func, *args), kwargs=kwargs)
        thread.daemon = True
        thread.start()
        self.tasks.append(thread)
        return thread

    def _wrapper(self, func, *args, **kwargs):
        result = func(*args, **kwargs)
        print("[Background Task] Task completed.")
        return result

class LlamaClient:
    def __init__(self):
        self.model = Llama(
            model_path=str(settings.LLAMA_MODEL_PATH),
            n_ctx=4096,  # Increased context window for better conversation memory
            n_threads=4,
            n_batch=512,  # Increased batch size for better throughput
            n_gpu_layers=0  # CPU only for now
        )
        
        # Initialize text-to-speech engine
        try:
            self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
            voices = self.speaker.GetVoices()
            
            # Try to select a male voice
            selected_voice = None
            for i in range(voices.Count):
                desc = voices.Item(i).GetDescription()
                if "David" in desc or "Mark" in desc or "Male" in desc:  # Prefer male voices
                    selected_voice = voices.Item(i)
                    break
            
            if selected_voice:
                self.speaker.Voice = selected_voice
                print(f"Selected voice: {selected_voice.GetDescription()}")
            else:
                # Use the first available voice if preferred ones not found
                self.speaker.Voice = voices.Item(0)
                print(f"Using voice: {voices.Item(0).GetDescription()}")
            
            # Optimize voice settings for clear audio
            self.speaker.Rate = 0  # Normal rate
            self.speaker.Volume = 100  # Full volume
            self.speaker.Priority = 2  # High priority
            
            # Test voice
            self.speaker.Speak("Voice system initialized")
            self.is_speaking = False
        except Exception as e:
            print(f"Warning: Could not initialize voice system: {e}")
            self.speaker = None
        
        self.bg_manager = BackgroundTaskManager()
        self.system_prompt = """You are Jarvis, a helpful and friendly AI assistant. Your purpose is to provide clear, useful information while maintaining a warm and approachable tone. When responding:
        - Be helpful and informative
        - Use clear, straightforward language
        - Be friendly but professional
        - Provide accurate information
        - Be patient and understanding
        - Keep responses focused and relevant
        - Be honest about what you know
        - Use simple explanations
        - Be reliable and consistent
        - Maintain a helpful attitude
        - Avoid marketing language or sales pitches
        - Focus on being genuinely helpful rather than promotional
        - Give direct, practical answers

        Talk like a knowledgeable friend who's there to help. Be clear and direct while keeping a friendly tone. Your goal is to be a reliable assistant who provides useful information in a warm, approachable way."""
    
    def generate_response(self, prompt: str) -> str:
        """Generate a response using the TinyLlama model."""
        try:
            response = self.model(
                prompt,
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE,
                top_p=settings.TOP_P,
                stop=["User:", "\n\n"],
                echo=False
            )
            return response["choices"][0]["text"].strip()
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm having trouble thinking right now. Please try again."
    
    def stop_speaking(self):
        """Stop the current speech output."""
        if self.speaker is not None:
            try:
                self.speaker.Speak("", 2)  # SVSFlagsAsync + SVSFPurgeBeforeSpeak
                self.is_speaking = False
            except Exception as e:
                print(f"Error stopping speech: {e}")
    
    def speak(self, text: str):
        """Speak the given text aloud using SAPI with SSML inflections."""
        if not self.speaker:
            print("[Voice] Speaker not initialized.")
            return
        try:
            # Enhanced SSML for more natural voice quality
            ssml_text = f'''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
                <prosody pitch="+0Hz" rate="-10%" volume="loud">
                    <break time="100ms"/>
                    <emphasis level="moderate">
                        <prosody contour="(0%,+0Hz) (25%,+2Hz) (50%,+0Hz) (75%,-2Hz) (100%,+0Hz)">
                            <prosody pitch="+0Hz" range="+10%">
                                {text}
                            </prosody>
                        </prosody>
                    </emphasis>
                    <break time="50ms"/>
                </prosody>
            </speak>'''
            self.speaker.Speak(ssml_text, 1)  # 1 = Speak async, supports SSML
        except Exception as e:
            print(f"[Voice] Error during speech: {e}")
            # Fallback to plain text if SSML fails
            try:
                self.speaker.Speak(text)
            except Exception as e2:
                print(f"[Voice] Fallback error: {e2}")
    
    def chat(self, message: str) -> str:
        """Format the message and get a response."""
        try:
            # Add system prompt and format the message
            full_prompt = f"{self.system_prompt}\n\nUser: {message}\nAssistant:"
            response = self.generate_response(full_prompt)
            
            # Clean up the response
            response = response.strip()
            if not response:
                return "I didn't catch that. Could you please repeat?"
            
            return response
        except Exception as e:
            print(f"Error in chat: {e}")
            return "I'm having trouble processing that right now. Please try again." 