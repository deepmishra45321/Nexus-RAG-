import os
from langchain_ollama import ChatOllama, OllamaEmbeddings

# Configure parallel execution as requested
os.environ["OLLAMA_NUM_PARALLEL"] = "2"

def get_chat_model(streaming: bool = True):
    return ChatOllama(
        model="qwen2.5:1.5b",
        temperature=0.0,
        streaming=streaming,
        keep_alive=-1
    )

def get_embeddings_model():
    return OllamaEmbeddings(
        model="qwen3-embedding:0.6b",
        keep_alive=-1
    )
