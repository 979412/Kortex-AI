import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="KORTEX-AI", page_icon="🧠")
st.title("🧠 KORTEX-AI: Ultra Beyin")

# YENİ AÇARINI YALNIZ BURA YAZ (Dırnaq işarələrinin içinə)
API_KEY = "YENİ_AÇARINI_BURA_YAPIŞDIR"
genai.configure(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Bura 'Salam' yazaraq yoxla..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("KORTEX əlaqə qurur..."):
            try:
                # Ən stabil modeli istifadə edirik
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.warning("Model cavab qaytarmadı.")
            
            except Exception as e:
                st.error(f"Sistem xətası: {str(e)}")
