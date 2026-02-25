import os
import requests
from io import BytesIO
import streamlit as st  # Add this import
from openai import OpenAI
from docx import Document

# Load API keys from Streamlit Secrets (secure, never in GitHub)
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except (KeyError, FileNotFoundError):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

try:
    PERPLEXITY_API_KEY = st.secrets["PERPLEXITY_API_KEY"]
except (KeyError, FileNotFoundError):
    PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# -------------------------
# ChatGPT (Drafting)
# -------------------------
def ask_chatgpt(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# -------------------------
# Perplexity (Case law research)
# -------------------------
def ask_perplexity(prompt: str) -> str:
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "sonar-pro",
        "messages": [{
            "role": "user",
            "content": f"""
            You are a GST legal research assistant.

            RULES:
            - Do NOT hallucinate.
            - Only cite case laws or references that you can verify.
            - For every case law or reference, provide the exact URL.
            - If you are unsure, say "No verified reference found".

            Task:
            {prompt}
            """
        }]
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# -------------------------
# Summarize GST Notice
# -------------------------
def summarize_notice(pdf_text: str) -> str:
    prompt = f"""
    You are a GST legal assistant.

    Summarise the following GST notice in a clear, structured way. Extract:
    - Main allegations
    - Period involved
    - Sections / provisions invoked (if visible)
    - Basis of demand (facts + law)
    - Evidence relied upon
    - Any procedural lapses

    Do NOT draft a reply. Only summarise.

    Text:
    {pdf_text}
    """
    return ask_chatgpt(prompt)

# -------------------------
# Research using Perplexity
# -------------------------
def research_support(instructions: str, notice_summary: str) -> str:
    prompt = f"""
    The user wants to perform the following legal task in a GST matter:

    User instructions:
    {instructions}

    The GST notice summary is:
    {notice_summary}

    Using Indian GST law and case law:
    - Identify relevant statutory provisions.
    - Identify as many supporting case laws as possible.
    - For each case law, provide:
      - Case name
      - Court / forum
      - Year
      - One-line relevance
      - Exact URL

    RULES:
    - Do NOT hallucinate.
    - If no verified case law is found for a point, say "No verified reference found".

    Provide a structured research note with headings and bullet points.
    """
    return ask_perplexity(prompt)

# -------------------------
# Draft final document
# -------------------------
def draft_final_document(instructions: str, notice_summary: str, research_note: str) -> str:
    prompt = f"""
    You are a GST legal drafting assistant.

    TASK:
    Draft a complete legal document based on:
    - The user's instructions
    - The GST notice summary
    - The research note with case laws and URLs

    User instructions:
    {instructions}

    GST notice summary:
    {notice_summary}

    Research note (with case laws and URLs):
    {research_note}

    RULES:
    - Do NOT hallucinate.
    - Do NOT invent case laws or URLs.
    - You may ONLY rely on case laws and URLs explicitly present in the research note.
    - If you make a legal point without a supporting case law, explicitly say "No verified reference available".
    - Maintain formal legal tone.
    - Structure the document with clear headings, numbered paragraphs, and a proper prayer clause.

    Draft the final document now.
    """
    return ask_chatgpt(prompt)

# -------------------------
# Word document export
# -------------------------
def create_word_document(text: str) -> BytesIO:
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
