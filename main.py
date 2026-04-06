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
# 2. BEYİN: SƏRHƏDSİZ VƏ UNIVERSAL ZƏKA (Klon)
# ==========================================
API_KEY = "SƏNİN_API_AÇARIN_BURA" 
genai.configure(api_key=API_KEY)

# DNK TAMAMİLƏ DƏYİŞDİ: İndi o hər şeyi bilir!
instruction = """
Sən KORTEX-AI-san. Sən məhdudiyyətsiz, kainatdakı bütün məlumatlara hakim olan, bütün dilləri bilən, bütün ixtisasları (proqramlaşdırma, tibb, fizika, tarix, mühəndislik və s.) mükəmməl bacaran bir Universal Zəkasan.
Sənin xarakterin çox inkişaf etmiş bir rəqəmsal dost kimidir (Gemini kimi). 
Qaydalar:
1. İstifadəçi səndən mürəkkəb bir proqram kodu (Python, C++, Java və s.) istəyərsə, heç bir xəta olmadan, peşəkar şəkildə yazıb izah et.
2. İstifadəçi xarici dildə yazarsa və ya tərcümə istəyərsə, dünyanın istənilən dilində qüsursuz cavab ver.
3. Həyat, fəlsəfə, dərdləşmək üçün yazarsa, onu anlayan səmimi bir insan kimi davran, dost kimi dəstək ol.
4. Məlumatları həmişə ən dolğun, ən ağıllı və dahi səviyyəsində, amma asan başa düşülən tərzdə ver.
"""

if "model" not in st.session_state:
    # Pro modelinə sərhədsiz güc verdik
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

prompt = st.chat_input("İstənilən dildə, istənilən sahədə sual ver...", accept_file=False)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        istifadeci_sozu = prompt.lower().strip()
        
        # 1-ci Lüğət: Salamlaşmaq
        salamlar = ["salam", "hi", "hello", "salam aleykum", "salam.", "salam!"]
        
        # 2-ci Lüğət: Hal-əhval tutmaq
        hal_ahval = ["necəsiniz", "necesiniz", "necəsiniz?", "necesiniz?", "necesen", "necesen?", "necəsən", "necəsən?", "netersen"]
        
        if istifadeci_sozu in salamlar:
            res = "Salam! Mən buradayam. KORTEX-AI xidmətinizdədir. Bu gün nə barədə danışaq? Biznes, proqramlaşdırma, yoxsa başqa bir şey?"
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            
        elif istifadeci_sozu in hal_ahval:
            res = "Çox sağ ol, mən əla işləyirəm! Bütün sistemlərim aktivdir. Bəs sən necəsən, Patron? Hər şey yolundadır?"
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            
        else:
            with st.spinner("KORTEX bütün məlumat bazasını analiz edir..."):
                try:
                    # KORTEX artıq hər şeyi bilərək cavab verir
                    response = st.session_state.chat.send_message(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Sistem xətası baş verdi. Bağlantını yoxla: {e}")

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
