import streamlit as st
import google.generativeai as genai

# Səhifənin dizaynını və adını tənzimləyirik
st.set_page_config(page_title="Kortex AI", page_icon="🧠")

# DİQQƏT: Aşağıdakı dırnaq içərisinə öz API açarını yazmalısan!
API_KEY = "SƏNİN_API_AÇARIN_BURADA_OLACAQ" 

genai.configure(api_key=API_KEY)

# Kortex-ə xüsusi bir xarakter və güc veririk
kortex_xarakteri = """
Sən Kortex-sən. Çox güclü, sürətli və ağıllı bir süni intellektsən. 
Sənin yaradıcın Abdullah adlı gənc və istedadlı bir proqramçıdır. 
İstifadəçilərin suallarına ən dəqiq, anlaşıqlı və peşəkar şəkildə cavab verirsən.
"""

# Modeli yükləyirik və xarakteri ona təyin edirik
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=kortex_xarakteri
)

# Vebsaytın başlığı
st.title("🧠 Kortex AI")
st.write("Salam! Mən Kortex. Sizin şəxsi və çox güclü süni intellekt köməkçinizəm. Mənə istədiyiniz sualı verə bilərsiniz.")

# Yaddaş sistemini qururuq
if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = []

# Köhnə mesajları ekranda göstəririk
for mesaj in st.session_state.mesajlar:
    with st.chat_message(mesaj["rol"]):
        st.markdown(mesaj["mətn"])

# XƏTANIN DÜZƏLDİLDİYİ YER: Sualı ayrı qəbul edib, sonra if ilə yoxlayırıq
sual = st.chat_input("Kortex-ə sualınızı yazın...")

if sual:
    # 1. İstifadəçinin sualını ekrana və yaddaşa əlavə edirik
    st.session_state.mesajlar.append({"rol": "user", "mətn": sual})
    with st.chat_message("user"):
        st.markdown(sual)
    
    # 2. Kortex-in cavab vermə prosesi
    with st.chat_message("model"):
        try:
            # API açarı yazılmayıbsa, xəbərdarlıq edirik
            if API_KEY == "SƏNİN_API_AÇARIN_BURADA_OLACAQ":
                st.error("Kortexin oyanması üçün main.py faylında API açarınızı qeyd etməlisiniz!")
            else:
                # Kortex düşünür və bütün keçmiş mesajları nəzərə alaraq cavab verir
                söhbet = model.start_chat(history=[])
                
                # Söhbət tarixçəsini API-yə uyğunlaşdırırıq
                for m in st.session_state.mesajlar[:-1]:
                    rol = "user" if m["rol"] == "user" else "model"
                    söhbet.history.append({"role": rol, "parts": [m["mətn"]]})
                
                # Yeni sualı göndərib cavabı alırıq
                cavab = söhbet.send_message(sual)
                st.markdown(cavab.text)
                
                # Kortex-in cavabını yaddaşa əlavə edirik
                st.session_state.mesajlar.append({"rol": "model", "mətn": cavab.text})
                
        except Exception as e:
            st.error(f"Bağışlayın, sistemdə xəta baş verdi: {e}")
