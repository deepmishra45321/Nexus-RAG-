from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from .state import AgentState
from .llm import get_chat_model
from .rag import get_retriever
from .memory import get_facts, save_fact

# Initialize models
llm = get_chat_model(streaming=True)
extractor_llm = get_chat_model(streaming=False)

def retrieve_node(state: AgentState):
    """Retrieve documents if necessary, or just extract latest message."""
    messages = state["messages"]
    latest_message = messages[-1].content
    
    # OPTIMIZATION: Skip RAG for simple greetings to prevent slow model-swapping in Ollama
    generic_greetings = ["hi", "hello", "hey", "how are you", "what's up", "who are you", "hi there"]
    cleaned_msg = latest_message.strip().lower().replace("?", "").replace("!", "")
    if cleaned_msg in generic_greetings or len(cleaned_msg) < 3:
        return {"context": ""}
    
    # Simple RAG: Always retrieve context for the latest message
    retriever = get_retriever()
    docs = retriever.invoke(latest_message)
    context = "\n".join([doc.page_content for doc in docs])
    
    return {"context": context}

def generate_node(state: AgentState):
    """Generate response using context and long-term memory."""
    messages = state["messages"]
    context = state.get("context", "")
    
    # Fetch long term memory facts
    facts = get_facts("default_user")
    facts_str = "\n".join(facts) if facts else "No long term facts known."
    
    system_prompt = f"""You are NexusRAG, a helpful AI assistant.
Use the following retrieved context to answer the user's question if relevant:
<context>
{context}
</context>

Known facts about the user from long-term memory:
<facts>
{facts_str}
</facts>

If the user tells you a new fact about themselves, acknowledge it and incorporate it.
"""
    
    invoke_messages = [SystemMessage(content=system_prompt)] + list(messages)
    
    response = llm.invoke(invoke_messages)
    
    return {"messages": [response]}

def update_memory_node(state: AgentState):
    """Extract facts and update long-term memory."""
    messages = state["messages"]
    
    human_messages = [m for m in messages if isinstance(m, HumanMessage)]
    if not human_messages:
        return {}
        
    latest_human = human_messages[-1].content
    
    # OPTIMIZATION: Only run the heavy 9B extraction LLM if it looks like a fact
    lower_msg = latest_human.lower()
    if not any(kw in lower_msg for kw in ["i am", "my", "i like", "i live", "i work"]):
        return {}
    
    extraction_prompt = f"""Extract any new explicit facts the user stated about themselves in this message.
If none, output exactly 'NONE'. Message: "{latest_human}" """
    
    fact = extractor_llm.invoke([HumanMessage(content=extraction_prompt)]).content
    
    if "NONE" not in fact.upper() and fact.strip() != "":
        save_fact("default_user", fact.strip())
        
    return {}

# Build graph
def create_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_node)
    workflow.add_node("update_memory", update_memory_node)

    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", "update_memory")
    workflow.add_edge("update_memory", END)
    
    return workflow
