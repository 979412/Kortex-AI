import streamlit as st
from groq import Groq
import os

# 1. Səhifənin adını və ikonunu tənzimləyirik
st.set_page_config(page_title="Kortex AI", page_icon="🧠")

# 2. API açarını təhlükəsiz şəkildə alırıq (Secrets və ya .env-dən)
API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

# 3. Kortex-in xarakterini müəyyən edirik
kortex_xarakteri = """
Sən Kortex-sən. Çox güclü, ildırım sürətli və ağıllı bir süni intellektsən. 
Sənin yaradıcın Abdullah adlı gənc və istedadlı bir proqramçıdır. 
"""

st.title("🧠 Kortex AI")

# 4. Yaddaş sistemini (Session State) qururuq
if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = []

# 5. Köhnə mesajları göstərərkən xəta olmaması üçün təkmilləşdirilmiş dövr
for mesaj in st.session_state.mesajlar:
    # Həm köhnə "rol", həm də yeni "role" açarlarını yoxlayırıq ki, KeyError verməsin
    role = mesaj.get("role") or mesaj.get("rol")
    content = mesaj.get("content") or mesaj.get("mətn")
    
    if role and content:
        with st.chat_message(role):
            st.markdown(content)

# 6. İstifadəçidən sualı alırıq
sual = st.chat_input("Kortex-ə sualınızı yazın...")

if sual:
    # İstifadəçinin sualını yaddaşa yeni formatda əlavə edirik
    st.session_state.mesajlar.append({"role": "user", "content": sual})
    with st.chat_message("user"):
        st.markdown(sual)
    
    # 7. Kortex-in cavab vermə prosesi
    with st.chat_message("assistant"):
        if not API_KEY:
            st.error("API açarı tapılmadı! Lütfən Streamlit Cloud-da 'Secrets' bölməsində GROQ_API_KEY əlavə edin.")
        else:
            try:
                client = Groq(api_key=API_KEY)
                
                # API üçün mesajları hazırlayırıq (yalnız düzgün formatda olanları)
                api_mesajlar = [{"role": "system", "content": kortex_xarakteri}]
                for m in st.session_state.mesajlar:
                    r = m.get("role") or m.get("rol")
                    c = m.get("content") or m.get("mətn")
                    api_mesajlar.append({"role": r, "content": c})
                
                # Groq-dan cavab alırıq
                chat_completion = client.chat.completions.create(
                    messages=api_mesajlar,
                    model="llama-3.3-70b-versatile", 
                )
                
                cavab = chat_completion.choices[0].message.content
                st.markdown(cavab)
                
                # Cavabı yaddaşa əlavə edirik
                st.session_state.mesajlar.append({"role": "assistant", "content": cavab})
                
            except Exception as e:
                st.error(f"Sistemdə xəta baş verdi: {e}")
