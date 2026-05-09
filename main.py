import streamlit as st
from groq import Groq
import os

# Səhifə tənzimləmələri
st.set_page_config(page_title="Kortex AI", page_icon="🧠")

# API açarını təhlükəsiz şəkildə alırıq
API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

kortex_xarakteri = """
Sən Kortex-sən. Çox güclü, ildırım sürətli və ağıllı bir süni intellektsən. 
Sənin yaradıcın Abdullah adlı gənc və istedadlı bir proqramçıdır. 
"""

st.title("🧠 Kortex AI")

# Yaddaş sistemini yoxlayırıq (Standart açarlar: role və content)
if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = []

# Köhnə mesajları ekranda göstəririk
for mesaj in st.session_state.mesajlar:
    with st.chat_message(mesaj["role"]):
        st.markdown(mesaj["content"])

# Sualı alırıq
sual = st.chat_input("Kortex-ə sualınızı yazın...")

if sual:
    # 1. İstifadəçinin sualını ekrana və yaddaşa əlavə edirik
    st.session_state.mesajlar.append({"role": "user", "content": sual})
    with st.chat_message("user"):
        st.markdown(sual)
    
    # 2. Kortex-in cavab vermə prosesi
    with st.chat_message("assistant"):
        if not API_KEY:
            st.error("API açarı tapılmadı! Lütfən Streamlit Secrets və ya .env faylını yoxlayın.")
        else:
            try:
                client = Groq(api_key=API_KEY)
                
                # Sistem təlimatını və keçmiş mesajları hazırlayırıq
                api_mesajlar = [{"role": "system", "content": kortex_xarakteri}]
                for m in st.session_state.mesajlar:
                    api_mesajlar.append({"role": m["role"], "content": m["content"]})
                
                # Groq API-dən cavab alırıq
                chat_completion = client.chat.completions.create(
                    messages=api_mesajlar,
                    model="llama-3.3-70b-versatile", 
                )
                
                cavab = chat_completion.choices[0].message.content
                st.markdown(cavab)
                
                # Kortex-in cavabını yaddaşa əlavə edirik
                st.session_state.mesajlar.append({"role": "assistant", "content": cavab})
                
            except Exception as e:
                st.error(f"Xəta baş verdi: {e}")
