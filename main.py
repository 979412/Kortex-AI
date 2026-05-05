import streamlit as st
import google.generativeai as genai

# Kortex-in oyanması üçün lazım olan sehrli açar (API Key) bura yazılacaq
# "SƏNİN_API_AÇARIN_BURADA_OLACAQ" yazısını öz açarınla əvəz etməyi unutma!
genai.configure(api_key="SƏNİN_API_AÇARIN_BURADA_OLACAQ")

model = genai.GenerativeModel('gemini-1.5-flash')

# Vebsaytın başlığı və dizaynı
st.title("🧠 Kortex AI")
st.write("Salam! Mən Kortex. Sizin şəxsi və çox güclü süni intellekt köməkçinizəm. Mənə istədiyiniz sualı verə bilərsiniz.")

# İstifadəçinin sual yazması üçün qəşəng bir chat qutusu
sual = st.chat_input("Kortex-ə sualınızı yazın...")

# Əgər istifadəçi sual yazsa, bu hissə işə düşür
if sual:
    # İstifadəçinin sualını ekranda göstəririk
    with st.chat_message("user"):
        st.write(sual)
    
    # Kortex-in cavabını ekranda göstəririk
    with st.chat_message("assistant"):
        try:
            # Kortex düşünür və cavab verir
            cavab = model.generate_content(sual)
            st.write(cavab.text)
        except Exception as e:
            st.error("Bağışlayın, sistemdə xəta baş verdi. API açarınızı düzgün qoyduğunuzdan əmin olun.")
