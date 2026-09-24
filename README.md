# NexusRAG

NexusRAG is a Streamlit-based AI assistant that leverages a Retrieval-Augmented Generation (RAG) pipeline to provide intelligent, context-aware responses. It utilizes local models via Ollama, LangChain, and LangGraph for orchestration, and features both short-term session memory and long-term factual memory.

## Features

- **Local AI Models**: Uses Ollama for fully local and private AI execution.
  - Chat Model: `qwen2.5:1.5b`
  - Embedding Model: `qwen3-embedding:0.6b`
- **RAG Capabilities**: Upload PDF documents directly through the UI, which are ingested, chunked, and stored in a local ChromaDB instance for quick retrieval during conversations.
- **Advanced Memory Management**: 
  - **Short-term Memory**: Uses LangGraph's `SqliteSaver` to maintain context within individual chat sessions.
  - **Long-term Memory**: Extracts user-specific facts during conversations and persists them in a local SQLite database (`nexus_memory.db`), allowing the assistant to remember details about the user across multiple sessions.
- **Optimized Workflow**: Skips heavy retrieval or extraction steps on simple generic greetings to improve response times.
- **Clean UI**: A modern and user-friendly web interface built with Streamlit, including a chat interface, sidebar controls, and developer information.

## Architecture

The project is structured into backend logic and UI components:

- `app.py`: The main entry point of the Streamlit application.
- `backend/`
  - `graph.py`: Defines the AI workflow using `langgraph`. It orchestrates retrieval, generation, and memory update nodes.
  - `llm.py`: Configures the connection to the local Ollama chat and embedding models.
  - `memory.py`: Manages the SQLite database for session check-pointing and long-term factual memory.
  - `rag.py`: Handles PDF ingestion using `PyPDFLoader`, text splitting, and ChromaDB vector storage.
  - `state.py`: Defines the state structure (`AgentState`) passed through the LangGraph workflow.
- `ui/`
  - `chat.py`: Handles the main chat interface, token streaming, and interaction with the backend graph.
  - `sidebar.py`: Manages the sidebar UI for creating new chats, uploading PDFs, and displaying project/developer details.
  - `styles.py`: Contains custom CSS for styling the application.

## Installation and Setup

### Prerequisites

1. **Python 3.8+**
2. **Ollama**: You must have [Ollama](https://ollama.com/) installed and running on your system.

### 1. Clone the repository

Navigate to your desired directory and ensure you have the project files.

### 2. Setup Virtual Environment and Install Dependencies

We use a virtual environment named `rag1` to manage dependencies. Create the environment and install the required packages:

```bash
python -m venv rag1
# For Windows (PowerShell)
.\rag1\Scripts\Activate.ps1
# For macOS/Linux
source rag1/bin/activate

pip install -r requirements.txt
```

### 3. Pull required Ollama models

Ensure Ollama is running, then open a terminal and pull the necessary models:

```bash
ollama pull qwen2.5:1.5b
ollama pull qwen3-embedding:0.6b
```

### 4. Run the application

Ensure your `rag1` virtual environment is activated, then start the Streamlit server:

```bash
streamlit run app.py
```

The application will be available in your browser at `http://localhost:8501`.

## Usage

1. **Chat**: Use the chat input box at the bottom to talk to NexusRAG. It will remember facts about you automatically.
2. **Ingest Documents**: Open the sidebar on the left and use the "Upload a PDF for RAG" section to ingest documents. Once ingested, the assistant can answer questions based on the document's content.
3. **Manage Sessions**: Use the "Create New Chat" button in the sidebar to start a fresh conversation with a new short-term memory thread. (Long-term memory will still persist).

## Developer

Built by **Deepak Mishra**
- Email: deep.mishra45321@gmail.com
- Mobile: 7876776987
