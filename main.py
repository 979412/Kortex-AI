import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

st.set_page_config(page_title="KORTEX-AI", page_icon="🧠")

st.title("🧠 KORTEX-AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Mesaj yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Düşünürəm..."):
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

            data = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": prompt}]
                    }
                ]
            }

            try:
                response = requests.post(url, json=data, timeout=10)

                if response.status_code == 200:
                    result = response.json()

                    cavab = result["candidates"][0]["content"]["parts"][0]["text"]

                    st.markdown(cavab)
                    st.session_state.messages.append({"role": "assistant", "content": cavab})

                else:
                    st.error("API xətası: " + response.text)

            except Exception as e:
                st.error("Xəta: " + str(e))
