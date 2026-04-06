import streamlit as st
import google.generativeai as genai

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="KORTEX-AI", page_icon="🧠")
st.title("🧠 KORTEX-AI: Ultra Beyin")

# 2. API AÇARINI QEYD EDİRİK (Sənin verdiyin açarı bura yerləşdirdim)
API_KEY = "AIzaSyAvgUNZUco4-KxQxtFOcKnoh4oUOyjIxmk"
genai.configure(api_key=API_KEY)

# 3. YADDAŞ SİSTEMİ
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. KÖHNƏ MESAJLARI EKRANDA GÖSTƏRMƏK
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. ÇAT MEXANİZMİ
if prompt := st.chat_input("Bura 'Salam' yazaraq yoxla..."):
    # İstifadəçinin mesajı
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # KORTEX-in cavabı
    with st.chat_message("assistant"):
        with st.spinner("KORTEX düşünür..."):
            try:
                # Modeli ən sadə variantda çağırırıq (Xəta çıxmaması üçün)
                model = genai.GenerativeModel("gemini-1.5-pro")
                
                # Yaddaş tarixçəsini hazırlayırıq
                history = [{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages[:-1]]
                chat = model.start_chat(history=history)
                
                # Mesajı göndəririk
                response = chat.send_message(prompt)
                
                # Cavabı ekrana çıxarırıq
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.warning("Model cavab qaytarmadı.")
            
            except Exception as e:
                st.error(f"Xəta baş verdi: {str(e)}")
                if "API_KEY_INVALID" in str(e):
                    st.info("İpucu: API açarını Google AI Studio-dan yenidən yoxlayın.")
