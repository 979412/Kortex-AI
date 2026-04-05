import streamlit as st
import google.generativeai as genai
import os
from reader import KortexReader

# Səhifə Ayarları
st.set_page_config(page_title="KORTEX-AI Business Intelligence", page_icon="🧠")

st.title("🧠 KORTEX-AI: Strateji Biznes Analitiki")
st.markdown("---")

# API Açarı (Streamlit Secrets-dən oxuyacaq)
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Sol panel - Məlumat
with st.sidebar:
    st.header("Sistem Statusu")
    st.success("KORTEX-AI Onlayndır")
    st.info("Hədəf: $100,000 mənfəət analizi")

# Fayl yükləmə
uploaded_file = st.file_uploader("Biznes hesabatını yükləyin (PDF)", type="pdf")

if uploaded_file is not None:
    # Faylı müvəqqəti yaddaşa yazırıq
    with open("temp_report.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    if st.button("KORTEX-AI Analizini Başlat"):
        with st.spinner('Rəqəmlər yoxlanılır və strategiya qurulur...'):
            # Reader modulunu işlədirik
            reader = KortexReader()
            text = reader.read_pdf("temp_report.pdf")
            
            # Sİ-yə sorğu göndəririk
            prompt = f"Sən KORTEX-AI-san. Bu sənədi analiz et və biznes sahibinə $100k qazandıracaq 3 strateji addım de: {text[:4000]}"
            response = model.generate_content(prompt)
            
            st.subheader("📊 Strateji Hesabat")
            st.write(response.text)
