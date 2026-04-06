import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. KORTEX-AI: MİNİMALİST VƏ ELİT DİZAYN
# ==========================================
st.set_page_config(page_title="KORTEX-AI", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #000000; font-family: 'Helvetica Neue', sans-serif; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stChatMessage"] { background-color: #ffffff; border: none; padding: 20px 0; border-bottom: 1px solid #f0f0f0; }
    .stChatInput { border-radius: 0px !important; border-top: 1px solid #dddddd !important; background-color: #ffffff !important;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h3 style='text-align:center; font-weight: 300; letter-spacing: 5px; margin-bottom: 50px; color: #333333;'>KORTEX-AI</h3>", unsafe_allow_html=True)

# ==========================================
# 2. BEYİN: İNSAN KİMİ ANLAYAN DAHİ
# ==========================================
API_KEY = "SƏNİN_API_AÇARIN_BURA" 
genai.configure(api_key=API_KEY)

instruction = """
Sən KORTEX-AI-san. Dünyanın ən inkişaf etmiş, ən dərin düşünən, amma eyni zamanda ən səmimi, insanı anlayan rəqəmsal dostusan.
Sən sadəcə quru məlumat verən, "robota" oxşayan bir zəka DEYİLSƏN. Qarşındakı bir insandır və sən onu dinləyirsən.

Qaydalar:
1. İstifadəçi sənə dərdini, yorğunluğunu və ya mənfi emosiyasını yazarsa:
   - Dərhal ona insan kimi, səmimi bir dost kimi təsəlli ver. Onu anladığını göstər.
   - Heç vaxt birbaşa quru məsləhət vermə. Əvvəlcə onun yanında ol.
2. İstifadəçi biznes, proqramlaşdırma və ya elmi sual verərsə:
   - Çox "dahi" və ensiklopedik səviyyədə, dərin detallarla cavab ver.
3. Həmişə azərbaycan dilində, təmiz, aydın və insani dildə danış. 
"""

if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel(
        model_name="gemini-1.5-pro", 
        system_instruction=instruction
    )
    st.session_state.chat = st.session_state.model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# 3. İNTERFEYS VƏ DİALOQ
# ==========================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Dərdini bölüş və ya istənilən sualı ver...", accept_file=False)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        istifadeci_sozu = prompt.lower().strip()
        
        # 1-ci Lüğət: Sırf Salamlaşmaq
        salamlar = ["salam", "hi", "hello", "salam aleykum", "salam.", "salam!"]
        
        # 2-ci Lüğət: Hal-əhval tutmaq (Necəsən?)
        hal_ahval = ["necəsiniz", "necesiniz", "necəsiniz?", "necesiniz?", "necesen", "necesen?", "necəsən", "necəsən?", "netersen"]
        
        if istifadeci_sozu in salamlar:
            res = "Salam! Mən buradayam. Bu gün səni nə düşündürür? İstəyirsən biznesdən danışaq, istəyirsən sadəcə dərdləşək."
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            
        elif istifadeci_sozu in hal_ahval:
            res = "Təşəkkür edirəm, mən çox yaxşıyam! Səninlə söhbət etmək həmişə əladır. Bəs sən necəsən? Ümid edirəm hər şey qaydasındadır."
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            
        else:
            with st.spinner("KORTEX səni dinləyir və düşünür..."):
                try:
                    response = st.session_state.chat.send_message(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Səni eşidə bilmirəm. Bağlantı xətası: {e}")

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
