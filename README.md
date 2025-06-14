# Jarvis - Your AI Desk Buddy

A voice-activated AI assistant that uses TinyLlama for natural language processing. Built to run efficiently on Raspberry Pi.

## Setup

1. Install dependencies:
```bash
uv pip install -r requirements.txt
```

2. Download TinyLlama model:
   - Visit [Hugging Face](https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF) to download a GGUF model
   - Place it in the `models` directory (recommended: tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf)

3. Create a `.env` file with your configuration:
```bash
LLAMA_MODEL_PATH=models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
```

## Usage

Run Jarvis:
```bash
python src/main.py
```

Say "Hey Jarvis" to activate the assistant.

## Project Structure

- `src/` - Source code
  - `main.py` - Entry point
  - `llm/` - LLM integration
  - `wake_word/` - Wake word detection
  - `config/` - Configuration management 