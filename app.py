import streamlit as st
from pypdf import PdfReader
import requests
import os
import re

# --------------------------------------------------
# Config
# --------------------------------------------------
st.set_page_config(page_title="PDF Summarizer (LLM)", layout="wide")
st.title("📄 PDF Summarizer (LLM-powered)")
st.write("Upload a PDF and get a bullet-point summary using an LLM.")

OPENROUTER_API_KEY = 'sk-or-v1-437e2'

if not OPENROUTER_API_KEY:
    st.error("❌ OPENROUTER_API_KEY not found in environment variables.")
    st.stop()

# --------------------------------------------------
# Read PDF
# --------------------------------------------------
def read_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            page_text = re.sub(r"\s+", " ", page_text)
            text += page_text + " "

    return text.strip()

# --------------------------------------------------
# Chunk text (LLM-safe)
# --------------------------------------------------
def chunk_text(text, max_length=3000):
    chunks = []
    current = ""

    for sentence in text.split(". "):
        if len(current) + len(sentence) <= max_length:
            current += sentence + ". "
        else:
            chunks.append(current.strip())
            current = sentence + ". "

    if current:
        chunks.append(current.strip())

    return chunks

# --------------------------------------------------
# Call OpenRouter LLM
# --------------------------------------------------
def summarize_with_llm(text):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "PDF Summarizer"
    }

    payload = {
        "model": "openai/gpt-4o-mini",  # fast + cheap
        "messages": [
            {
                "role": "system",
                "content": "You summarize documents clearly and concisely."
            },
            {
                "role": "user",
                "content": (
                    "Summarize the following text into clear bullet points. "
                    "No introduction, no conclusion, only bullet points:\n\n"
                    f"{text}"
                )
            }
        ],
        "temperature": 0.2
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]

# --------------------------------------------------
# Upload PDF
# --------------------------------------------------
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("📖 Reading PDF..."):
        pdf_text = read_pdf(uploaded_file)

    if not pdf_text:
        st.error("❌ Could not extract text from this PDF.")
        st.stop()

    with st.spinner("🤖 Summarizing with LLM..."):
        chunks = chunk_text(pdf_text)
        summaries = [summarize_with_llm(chunk) for chunk in chunks]

    st.subheader("📝 PDF Summary (Key Points)")
    for s in summaries:
        st.markdown(s)
