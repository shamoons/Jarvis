from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    # LLM Settings
    LLAMA_MODEL_PATH: Path = Path("models/llama-2-7b-chat.Q4_K_M.gguf")
    
    # Wake Word Settings
    WAKE_WORD: str = "hey jarvis"
    
    # Model Parameters
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 512
    TOP_P: float = 0.95
    
    class Config:
        env_file = ".env"

settings = Settings() 