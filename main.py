import streamlit as st
from groq import Groq
import os
import time

st.set_page_config(page_title="Kortex AI", page_icon="🧠", layout="centered")

# Açar buraya yazılır
API_KEY = st.secrets.get("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") or os.getenv("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") or "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"

st.title("🧠 Kortex AI")
st.caption("Yaradıcı: Abdullah | ⚡ Avtomatik Rejim Aktivdir")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

sual = st.chat_input("Kortex-ə sual verin...")

if sual:
    # Sənin sualın ekrana çıxır
    st.session_state.messages.append({"role": "user", "content": sual})
    with st.chat_message("user"):
        st.markdown(sual)

    with st.chat_message("assistant"):
        try:
            # 1. Kortex əsl beyninə (Groq-a) qoşulmağa cəhd edir
            client = Groq(api_key=API_KEY)
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": "Sən Kortexsən."}] + st.session_state.messages,
                model="llama-3.3-70b-versatile"
            )
            cavab = response.choices[0].message.content
            st.markdown(cavab)
            st.session_state.messages.append({"role": "assistant", "content": cavab})
            
        except Exception:
            # 2. ƏGƏR AÇAR SƏHVDİRSƏ VƏ YA YOXDURSA - AVTOMATİK YEDƏK REJİM İŞƏ DÜŞÜR (XƏTA VERMİR!)
            offline_cavab = f"Sən məndən soruşdun: **'{sual}'**\n\n🤖 Salam Abdullah! Mən hazırda 'Avtomatik Yedək Rejimdəyəm' və səni eşidirəm. Amma sənə tam ağıllı və həqiqi cavablar verə bilməyim üçün maşınıma 'benzin' lazımdır. Zəhmət olmasa kodun 9-cu sətrinə işləyən bir Groq API açarı qoy ki, əsl gücümü sənə göstərim!"
            
            # Kortexin sözləri yazaraq gəlməsi effekti (Gözəl görünüş üçün)
            placeholder = st.empty()
            tam_metn = ""
            for herf in offline_cavab:
                tam_metn += herf
                placeholder.markdown(tam_metn + "▌")
                time.sleep(0.01) # Yazılma sürəti
            placeholder.markdown(tam_metn)
            
            st.session_state.messages.append({"role": "assistant", "content": offline_cavab})
