import streamlit as st
from groq import Groq

# Səhifənin dizaynını və adını tənzimləyirik
st.set_page_config(page_title="Kortex AI", page_icon="🧠")

# DİQQƏT: Bura Groq-dan aldığın YENİ API açarını yazmalısan!
API_KEY = "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" 

# Kortex-ə xüsusi bir xarakter və güc veririk
kortex_xarakteri = """
Sən Kortex-sən. Çox güclü, ildırım sürətli və ağıllı bir süni intellektsən. 
Sənin yaradıcın Abdullah adlı gənc və istedadlı bir proqramçıdır. 
İstifadəçilərin suallarına ən dəqiq, anlaşıqlı və peşəkar şəkildə cavab verirsən.
"""

# Vebsaytın başlığı
st.title("🧠 Kortex AI (Groq Gücü ilə ⚡)")
st.write("Salam! Mən Kortex. Sizin şəxsi və çox sürətli süni intellekt köməkçinizəm. Mənə istədiyiniz sualı verə bilərsiniz.")

# Yaddaş sistemini qururuq
if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = []

# Köhnə mesajları ekranda göstəririk
for mesaj in st.session_state.mesajlar:
    with st.chat_message(mesaj["rol"]):
        st.markdown(mesaj["mətn"])

# Sualı alırıq
sual = st.chat_input("Kortex-ə sualınızı yazın...")

if sual:
    # 1. İstifadəçinin sualını ekrana və yaddaşa əlavə edirik
    st.session_state.mesajlar.append({"rol": "user", "mətn": sual})
    with st.chat_message("user"):
        st.markdown(sual)
    
    # 2. Kortex-in cavab vermə prosesi
    with st.chat_message("assistant"):
        try:
            if API_KEY == "SƏNİN_GROQ_API_AÇARIN":
                st.error("Kortexin oyanması üçün main.py faylında Groq API açarınızı qeyd etməlisiniz!")
            else:
                # Groq sisteminə qoşuluruq
                client = Groq(api_key=API_KEY)
                
                # Bütün yazışmaları Groq-un anladığı formata salırıq
                api_mesajlar = [{"role": "system", "content": kortex_xarakteri}]
                for m in st.session_state.mesajlar:
                    api_mesajlar.append({"role": m["rol"], "content": m["mətn"]})
                
                # LLaMA 3 (70B) kimi nəhəng və sürətli modeldən istifadə edirik
                chat_completion = client.chat.completions.create(
                    messages=api_mesajlar,
                    model="llama3-70b-8192", 
                )
                
                # Cavabı ekrana çıxarırıq
                cavab = chat_completion.choices[0].message.content
                st.markdown(cavab)
                
                # Kortex-in cavabını yaddaşa əlavə edirik
                st.session_state.mesajlar.append({"rol": "assistant", "mətn": cavab})
                
        except Exception as e:
            st.error(f"Bağışlayın, sistemdə xəta baş verdi: {e}")
