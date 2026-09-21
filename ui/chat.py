import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, AIMessageChunk
from backend.graph import create_graph
from backend.memory import get_checkpointer

def render_chat_interface():
    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    # React to user input
    if prompt := st.chat_input("Ask NexusRAG..."):
        # Display user message
        st.chat_message("user").markdown(prompt)
        # Add to session state for UI purposes
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Instantiate graph
        graph = create_graph()
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            with get_checkpointer() as checkpointer:
                app = graph.compile(checkpointer=checkpointer)
                
                config = {"configurable": {"thread_id": st.session_state.thread_id}}
                inputs = {"messages": [HumanMessage(content=prompt)]}
                
                try:
                    # Token streaming using stream_mode="messages"
                    message_placeholder.markdown("NexusRAG is thinking... ⏳ (This may take a minute for the first response due to the 9B model size)")
                    
                    for chunk, metadata in app.stream(inputs, config=config, stream_mode="messages"):
                        # In LangGraph stream_mode="messages", chunk is the message object
                        if isinstance(chunk, (AIMessage, AIMessageChunk)) and isinstance(getattr(chunk, "content", ""), str):
                            if chunk.content:
                                full_response += chunk.content
                                message_placeholder.markdown(full_response + "▌")
                            
                    if full_response:
                        message_placeholder.markdown(full_response)
                    else:
                        message_placeholder.markdown("*(No response was generated)*")
                except Exception as e:
                    st.error(f"Error connecting to Ollama model: {e}")
                    st.error("Please ensure you have pulled the model by running: `ollama pull qwen2.5:1.5b` and `ollama pull qwen3-embedding:0.6b` in your terminal.")
                    import traceback
                    traceback.print_exc()
        
        # Add assistant response to UI session state
        st.session_state.messages.append({"role": "assistant", "content": full_response})
