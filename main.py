import streamlit as st
import google.generativeai as genai

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="KORTEX-AI", page_icon="🧠")
st.title("🧠 KORTEX-AI: Ultra Beyin")

# 2. API AÇARI (Sənin verdiyin açar bura yerləşdirilib)
API_KEY = "AIzaSyAvgUNZUco4-KxQxtFOcKnoh4oUOyjIxmk"
genai.configure(api_key=API_KEY)

# 3. YADDAŞ SİSTEMİ (Müvəqqəti olaraq sadə saxlayırıq)
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
        with st.spinner("KORTEX əlaqə qurur..."):
            try:
                # XƏTANIN HƏLLİ: Modeli 'gemini-1.5-flash' olaraq dəyişdik
                # Bu model 404 xətası vermədən dərhal açılmalıdır
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                # Mesajı birbaşa göndəririk (ən sadə və sürətli yol)
                response = model.generate_content(prompt)
                
                # Cavabı ekrana çıxarırıq
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.warning("Model cavab qaytarmadı.")
            
            except Exception as e:
                st.error(f"Sistem xətası: {str(e)}")
                st.info("İpucu: Əgər yenə 404 xətası versə, 'gemini-pro' yazıb yoxlayın.")
