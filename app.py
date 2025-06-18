import streamlit as st
import os
from groq import Groq
from card_agent import CreditCardAgent  # this is your updated agent module

# Load Groq API key from environment or .streamlit/secrets.toml
GROQ_API_KEY = os.getenv("GROQ_API_KEY", st.secrets.get("GROQ_API_KEY", ""))

# Initialize Groq client and agent
client = Groq(api_key=GROQ_API_KEY)
agent = CreditCardAgent(model_client=client)

# UI Setup
st.set_page_config(page_title="Credit Card Advisor", layout="centered")
st.title("💳 Credit Card Recommendation Advisor")
st.markdown(
    "Enter details like your **income**, **spending categories**, and **preferences** "
    "(e.g., cashback, lounge access, etc.) to get tailored recommendations."
)

user_input = st.text_area("📝 Tell me about your income, spend habits, preferences:", height=180)

if st.button("🔍 Recommend Cards") and user_input.strip():
    with st.spinner("Analyzing your profile..."):
        result = agent.run(user_input)
        st.markdown(result)
