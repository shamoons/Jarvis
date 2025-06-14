from llama_cpp import Llama
from ..config.settings import settings

class LlamaClient:
    def __init__(self):
        self.model = Llama(
            model_path=str(settings.LLAMA_MODEL_PATH),
            n_ctx=1024,  # Reduced context window for faster processing
            n_threads=4,
            n_batch=512,  # Increased batch size for better throughput
            n_gpu_layers=0  # CPU only for now
        )
    
    def generate_response(self, prompt: str) -> str:
        """Generate a response using the TinyLlama model."""
        response = self.model(
            prompt,
            max_tokens=settings.MAX_TOKENS,
            temperature=settings.TEMPERATURE,
            top_p=settings.TOP_P,
            stop=["User:", "\n\n"],
            echo=False  # Don't include prompt in response
        )
        return response["choices"][0]["text"].strip()
    
    def chat(self, message: str) -> str:
        """Format the message and get a response."""
        prompt = f"""User: {message}
Assistant:"""
        return self.generate_response(prompt) 