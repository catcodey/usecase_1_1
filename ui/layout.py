import streamlit as st

def render_input_section():
    st.subheader("Input")
    has_text = len(st.session_state.get("input_text_val", "").strip()) > 0
    
    uploaded_files = st.file_uploader(
        "Upload TXT/XLSX (Multiple allowed)", 
        type=["txt", "xlsx"], 
        accept_multiple_files=True,
        disabled=has_text,
        key=f"uploader_{st.session_state.get('uploader_key', 0)}"
    )
    
    if uploaded_files:
        st.info("Files uploaded. Text area is now disabled.")
    
    st.markdown("---")

    manual_input = st.text_area(
        "Paste Transcript:", 
        height=300, 
        value=st.session_state.get("input_text_val", ""),
        disabled=bool(uploaded_files),
        placeholder="Paste your text here..."
    )
    st.session_state.input_text_val = manual_input
    
    if has_text:
        st.info("Text detected. File upload is now disabled.")
        
    return uploaded_files, manual_input

def render_chat_section():
    st.subheader("Summary & Chat")
    chat_container = st.container(height=450)
    with chat_container:
        if not st.session_state.messages:
            st.write("Results will appear here.")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])