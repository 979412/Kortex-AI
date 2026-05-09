import streamlit as st
from groq import Groq
import os

# 1. Ən sürətli performans üçün səhifə tənzimləmələri
st.set_page_config(page_title="Kortex AI", page_icon="🧠", layout="centered")

# 2. API Açarının avtomatik idarə olunması (Xəta verməməsi üçün)
# Əgər Secrets-də yoxdursa, kodun içinə birbaşa yaza bilərsən (Amma GitHub-a qoyanda sil!)
API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") or "SƏNİN_API_AÇARIN_BURA_YAZILA_BİLƏR"

# 3. Kortex-in Beyni və Təlimatı
kortex_instruksiya = {
    "role": "system",
    "content": "Sən Kortex-sən. Yaradıcın Abdullahdır. Çox ağıllı və sürətlisən. Qısa, dəqiq və professional cavablar ver."
}

# 4. Yaddaşın avtomatik təmizlənməsi və qurulması
if "messages" not in st.session_state:
    st.session_state.messages = []

# Başlıq
st.title("🧠 Kortex AI")
st.caption("⚡ Groq Llama 3.3 tərəfindən gücləndirildi | Yaradıcı: Abdullah")

# 5. Mesajların ekranda sürətli göstərilməsi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Sualın qəbulu və dərhal işlənməsi
sual = st.chat_input("Kortex-ə sual verin...")

if sual:
    # İstifadəçi sualını yaddaşa atırıq
    st.session_state.messages.append({"role": "user", "content": sual})
    with st.chat_message("user"):
        st.markdown(sual)

    # Cavab hazırlığı
    with st.chat_message("assistant"):
        # API açarı yoxlaması (Proqramın çökməməsi üçün)
        if not API_KEY or "SƏNİN_API_AÇARIN" in API_KEY:
            st.error("🔑 API açarı daxil edilməyib! Lütfən açarı koda və ya Secrets-ə əlavə edin.")
        else:
            try:
                # Sürətli qoşulma
                client = Groq(api_key=API_KEY)
                
                # Mesaj tarixcəsini optimallaşdırırıq (Sürət üçün)
                full_history = [kortex_instruksiya] + st.session_state.messages
                
                # API Çağırışı (Maksimum sürət modeli ilə)
                response = client.chat.completions.create(
                    messages=full_history,
                    model="llama-3.3-70b-versatile",
                    temperature=0.7, # Yaradıcılıq və sürət balansı
                    max_tokens=2048,
                    stream=True # Cavabın yazılaraq gəlməsi (istifadəçi gözləmir)
                )

                # Cavabı axın (stream) şəklində ekrana çıxarırıq
                placeholder = st.empty()
                tam_cavab = ""
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        tam_cavab += chunk.choices[0].delta.content
                        placeholder.markdown(tam_cavab + "▌")
                placeholder.markdown(tam_cavab)

                # Cavabı yaddaşa yazırıq
                st.session_state.messages.append({"role": "assistant", "content": tam_cavab})

            except Exception as e:
                # Xətanı tuturuq amma proqramı dayandırmırıq
                st.warning(f"Sistem bir anlıq durub: {str(e)}")
