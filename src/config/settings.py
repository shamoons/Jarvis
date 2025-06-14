from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    # LLM Settings
    LLAMA_MODEL_PATH: Path = Path("models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")
    
    # Wake Word Settings
    WAKE_WORD: str = "hey jarvis"
    
    # Model Parameters
    TEMPERATURE: float = 0.7  # More creative and varied responses
    MAX_TOKENS: int = 2048    # Allow for very long, detailed responses
    TOP_P: float = 0.9       # More diverse sampling
    
    class Config:
        env_file = ".env"

settings = Settings() 