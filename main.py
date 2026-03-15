import sys
import pathlib
import streamlit as st
from src.generate import TranscriptAI
from src.extractor import extract_data
from src.clean import clean_text
from src.chunking import get_overlapping_chunks
from ui.layout import render_input_section, render_chat_section
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# --- CONFIGURATION ---
PROJECT_ID = "transcript-summarizer-490013"
LOCATION = "asia-southeast1"

st.set_page_config(page_title="AI Transcript Analyser", layout="wide")

# Initialize State
if "ai_engine" not in st.session_state:
    st.session_state.ai_engine = TranscriptAI(PROJECT_ID, LOCATION)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = st.session_state.ai_engine.start_new_chat()
if "messages" not in st.session_state: st.session_state.messages = []
if "summary_text" not in st.session_state: st.session_state.summary_text = ""
if "input_text_val" not in st.session_state: st.session_state.input_text_val = ""
if "uploader_key" not in st.session_state: st.session_state.uploader_key = 0

st.title("Transcript Analysis Dashboard")
col1, col2 = st.columns(2, gap="large")

with col1:
    uploaded_files, manual_input = render_input_section()
    
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("🚀 Generate", use_container_width=True):
            raw_data = extract_data(uploaded_files) if uploaded_files else manual_input
            if raw_data:
                cleaned = clean_text(raw_data)
                chunks = get_overlapping_chunks(cleaned)
                
                try:
                    if len(chunks) > 1:
                        st.write(f"Processing {len(chunks)} chunks...")
                        summaries = [st.session_state.ai_engine.model.generate_content(f"Summarize briefly: {c}").text for c in chunks]
                        final_prompt = f"Combine these into 5 points:\n\n{' '.join(summaries)}"
                    else:
                        final_prompt = f"Summarize in 5 short points:\n\n{cleaned}"
                    
                    st.session_state.chat_session = st.session_state.ai_engine.start_new_chat()
                    response = st.session_state.chat_session.send_message(final_prompt)
                    st.session_state.summary_text = response.text
                    st.session_state.messages = [{"role": "assistant", "content": response.text}]
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    with btn_col2:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.update({"input_text_val": "", "summary_text": "", "messages": []})
            st.session_state.uploader_key += 1
            st.rerun()

with col2:
    render_chat_section()
    if prompt := st.chat_input("Follow-up..."):
        if st.session_state.summary_text:
            st.session_state.messages.append({"role": "user", "content": prompt})
            response = st.session_state.chat_session.send_message(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()

    if st.session_state.summary_text:
        st.download_button("💾 Download Summary", st.session_state.summary_text, "summary.txt")
