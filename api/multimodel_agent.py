import streamlit as st
from agno.ago import Agent
from agno.run.agent import RunOutput
from agno.models.google import GeminiModel
from agno.media import video 
from time 
from time import sleep
from pathlib import Path
import tempfile

st.set_page_config(page_title="Multimodal Gemini Agent", page_title="Multimodal Gemini Agent", page_icon="🤖", layout="wide")
st.title("🤖 Multimodal Gemini Agent")

#Get Gemini Api from user in sidebar 
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("my gemini api key:", type="password")
    model_name = st.selectbox("Select Gemini Model:", ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"])
    
    if not api_key:
        st.warning("Please enter your Gemini API key to proceed.")
        st.stop()