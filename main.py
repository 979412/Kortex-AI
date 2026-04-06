import streamlit as st
import requests

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="KORTEX-AI", page_icon="🧠", layout="centered")
st.markdown("<h1 style='text-align: center; color: #2C3E50;'>🧠 KORTEX-AI (Direkt Bağlantı)</h1>", unsafe_allow_html=True)
st.divider()

# 2. DİQQƏT: Öz YENİ API açarınızı bura yazın! (Köhnə sızdırılmış açarı yox!)
API_KEY = "SİZİN_YENİ_API_AÇARINIZ".strip()

# 3. YADDAŞ SİSTEMİ
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. ÇAT MEXANİZMİ (Tam fərqli və donmayan metod)
if prompt := st.chat_input("KORTEX-ə mesajınızı yazın..."):
    # İstifadəçi mesajı
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("KORTEX serverə qoşulur (Maks 10 saniyə)..."):
            
            # HTTP REST API İLƏ BİRBAŞA QOŞULMA (gRPC yoxdur, donma ehtimalı sıfırdır)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            
            headers = {'Content-Type': 'application/json'}
            data = {
                "contents": [{"parts": [{"text": prompt}]}]
            }

            try:
                # Tələb göndəririk (Maksimum 10 saniyə gözləyir)
                response = requests.post(url, headers=headers, json=data, timeout=10)
                
                # Əgər əlaqə 100% uğurludursa
                if response.status_code == 200:
                    result = response.json()
                    cavab_metni = result["candidates"][0]["content"]["parts"][0]["text"]
                    st.markdown(cavab_metni)
                    st.session_state.messages.append({"role": "assistant", "content": cavab_metni})
                
                # Əgər API açarı səhvdirsə və ya bloklanıbsa, dərhal xəta verəcək
                else:
                    st.error(f"Google Xətası: Kodu {response.status_code}. Səbəb: {response.text}")
            
            # Əgər 10 saniyə keçsə və cavab gəlməsə
            except requests.exceptions.Timeout:
                st.error("XƏTA: 10 saniyə keçdi və cavab gəlmədi. İnternetinizdə və ya VPN-də problem var.")
            
            # Digər bütün xətalar
            except Exception as e:
                st.error(f"Sistem Xətası baş verdi: {str(e)}")
