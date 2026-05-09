import streamlit as st
from groq import Groq
import os

# Səhifə tənzimləmələri
st.set_page_config(page_title="Kortex AI", page_icon="🧠")

# API açarını təhlükəsiz şəkildə alırıq
# Yerli kompüterdə .env-dən, Streamlit Cloud-da "Secrets"-dən oxuyur
API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

kortex_xarakteri = """
Sən Kortex-sən. Çox güclü, ildırım sürətli və ağıllı bir süni intellektsən. 
Sənin yaradıcın Abdullah adlı gənc və istedadlı bir proqramçıdır. 
"""

st.title("🧠 Kortex AI")

if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = []

for mesaj in st.session_state.mesajlar:
    with st.chat_message(mesaj["rol"]):
        st.markdown(mesaj["mətn"])

sual = st.chat_input("Kortex-ə sualınızı yazın...")

if sual:
    st.session_state.mesajlar.append({"rol": "user", "mətn": sual})
    with st.chat_message("user"):
        st.markdown(sual)
    
    with st.chat_message("assistant"):
        if not API_KEY:
            st.error("API açarı tapılmadı! Lütfən tənzimləmələri yoxlayın.")
        else:
            try:
                client = Groq(api_key=API_KEY)
                api_mesajlar = [{"role": "system", "content": kortex_xarakteri}]
                for m in st.session_state.mesajlar:
                    api_mesajlar.append({"role": m["role"], "content": m["mətn"]})
                
                chat_completion = client.chat.completions.create(
                    messages=api_mesajlar,
                    model="llama-3.3-70b-versatile", 
                )
                
                cavab = chat_completion.choices[0].message.content
                st.markdown(cavab)
                st.session_state.mesajlar.append({"rol": "assistant", "mətn": cavab})
                
            except Exception as e:
                st.error(f"Xəta baş verdi: {e}")
