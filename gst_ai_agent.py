import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = "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"
PERPLEXITY_API_KEY = "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"

client = OpenAI(api_key=OPENAI_API_KEY)

# ---------------------------
# 1. Function: Ask ChatGPT
# ---------------------------
def ask_chatgpt(prompt):
    response = client.chat.completions.create(
        model="gpt-5-2025-08-07",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]


# ---------------------------
# 2. Function: Ask Perplexity
# ---------------------------
def ask_perplexity(prompt):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "sonar-pro",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]


# ---------------------------
# 3. AI Agent Logic
# ---------------------------
def gst_ai_agent(task_type, details):
    """
    task_type: 'adjournment', 'retraction', 'scn_reply', 'scn_summary'
    details: user-provided facts
    """

    if task_type == "adjournment":
        prompt = f"""
        Draft a GST adjournment application. Facts: {details}.
        Include legal tone, reasons, and request for next date.
        """
        return ask_chatgpt(prompt)

    elif task_type == "retraction":
        prompt = f"""
        Draft a GST retraction of statement. Facts: {details}.
        Include coercion, duress, late-night detention, and legal grounds.
        """
        return ask_chatgpt(prompt)

    elif task_type == "scn_summary":
        research = ask_perplexity(f"Summarise this GST Show Cause Notice: {details}")
        drafting = ask_chatgpt(f"Rewrite this SCN summary in legal format: {research}")
        return drafting

    elif task_type == "scn_reply":
        research = ask_perplexity(f"""
        Provide case laws and legal grounds to defend against this GST SCN:
        {details}
        """)
        drafting = ask_chatgpt(f"""
        Draft a detailed reply to the GST SCN using these legal points:
        {research}
        Facts: {details}
        """)
        return drafting

    else:
        return "Invalid task type."


# ---------------------------
# 4. Command-line Interface
# ---------------------------
if __name__ == "__main__":
    print("\nGST AI Assistant")
    print("1. Adjournment Application")
    print("2. Retraction of Statement")
    print("3. SCN Summary")
    print("4. SCN Reply\n")

    choice = input("Enter choice (1-4): ")

    details = input("\nEnter case details: ")

    mapping = {
        "1": "adjournment",
        "2": "retraction",
        "3": "scn_summary",
        "4": "scn_reply"
    }

    task = mapping.get(choice)

    output = gst_ai_agent(task, details)

    print("\n\n--- Generated Draft ---\n")
    print(output)
