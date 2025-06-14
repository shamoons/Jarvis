# Jarvis - Your AI Desk Buddy

A voice-activated AI assistant that uses Llama for natural language processing. Built to run efficiently on Raspberry Pi.

## Setup

1. Install dependencies:
```bash
uv pip install -r requirements.txt
```

2. Download Llama model:
   - Visit [Hugging Face](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF) to download a GGUF model
   - Place it in the `models` directory

3. Create a `.env` file with your configuration:
```bash
LLAMA_MODEL_PATH=models/llama-2-7b-chat.Q4_K_M.gguf
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