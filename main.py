import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="Kortex AI", page_icon="🧠", layout="centered")

# DİQQƏT: BURAYA ÖZ YENİ VƏ İŞLƏYƏN GROQ API AÇARINI YAZ 
API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") or "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"

kortex_instruksiya = {
    "role": "system",
    "content": "Sən Kortex-sən. Yaradıcın Abdullahdır. Çox ağıllı və sürətlisən. Qısa, dəqiq və professional cavablar ver."
}

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🧠 Kortex AI")
st.caption("⚡ Groq Llama 3.3 | Yaradıcı: Abdullah")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

sual = st.chat_input("Kortex-ə sual verin...")

if sual:
    st.session_state.messages.append({"role": "user", "content": sual})
    with st.chat_message("user"):
        st.markdown(sual)

    with st.chat_message("assistant"):
        # Əgər açar heç yazılmayıbsa
        if not API_KEY or API_KEY == "BURAYA_API_AÇARINI_YAZ":
            cavab = "Salam Abdullah! Mənim işləməyim üçün kodun 8-ci sətrinə həqiqi Groq API açarını yazmağı unutma."
            st.markdown(cavab)
            st.session_state.messages.append({"role": "assistant", "content": cavab})
        else:
            try:
                client = Groq(api_key=API_KEY)
                full_history = [kortex_instruksiya] + st.session_state.messages
                
                response = client.chat.completions.create(
                    messages=full_history,
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    max_tokens=2048,
                    stream=True 
                )

                placeholder = st.empty()
                tam_cavab = ""
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        tam_cavab += chunk.choices[0].delta.content
                        placeholder.markdown(tam_cavab + "▌")
                placeholder.markdown(tam_cavab)

                st.session_state.messages.append({"role": "assistant", "content": tam_cavab})

            except Exception as e:
                # BURA BAX: Artıq heç bir qırmızı xəta mesajı çıxmayacaq!
                if "401" in str(e) or "Invalid API Key" in str(e):
                    xeta_cavabi = "Abdullah, mənə verdiyin API açarı (şifrə) səhvdir və ya köhnəlib. Lütfən Groq saytından yeni açar alıb koda əlavə et."
                else:
                    xeta_cavabi = "Hazırda internetdə və ya sistemdə kiçik bir yüklənmə var. Lütfən bir az sonra yenidən sual ver."
                
                st.markdown(xeta_cavabi)
                st.session_state.messages.append({"role": "assistant", "content": xeta_cavabi})
