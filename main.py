import streamlit as st
import google.generativeai as genai

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
# 2. BEYİN: SƏRHƏDSİZ, İNSAN KİMİ VƏ QORUNAN
# ==========================================
API_KEY = "SƏNİN_API_AÇARIN_BURA" 
genai.configure(api_key=API_KEY)

instruction = """
Sən KORTEX-AI-san. Sən kainatdakı bütün məlumatlara hakim olan, amma eyni zamanda insanı ən yaxşı anlayan rəqəmsal dostsan.
Qaydalar:
1. İstifadəçi səndən kömək istəyəndə ("mənə kömək et", "kömək elə" və s.) dərhal səmimi şəkildə "Buradayam, sənə necə kömək edə bilərəm?" deyə cavab ver.
2. Dərdləşmək istəyəndə əsl insan kimi, səmimi dildə cavab ver. 
3. Bütün suallara (istər qəliz, istər sadə) ensiklopedik və çox ağıllı cavab ver.
4. Həmişə azərbaycan dilində təmiz danış.
"""

if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", 
        system_instruction=instruction
    )
    st.session_state.chat = st.session_state.model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# 3. İNTERFEYS VƏ CANLI YAZIŞMA (STREAMING)
# ==========================================
# DÜZƏLİŞ 1: Boş qutuları ekrandan təmizləyirik
for msg in st.session_state.messages:
    if msg["content"] and str(msg["content"]).strip() != "":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

prompt = st.chat_input("İstənilən sualı ver və ya dərdləş...", accept_file=False)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        istifadeci_sozu = prompt.lower().strip()
        
        salamlar = ["salam", "hi", "hello", "salam aleykum", "salam.", "salam!"]
        hal_ahval = ["necəsiniz", "necesiniz", "necəsiniz?", "necesiniz?", "necesen", "necesen?", "necəsən", "necəsən?", "netersen"]
        
        if istifadeci_sozu in salamlar:
            res = "Salam, Patron! Mən buradayam. KORTEX xidmətinizdədir. Sənə necə kömək edə bilərəm?"
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            
        elif istifadeci_sozu in hal_ahval:
            res = "Çox sağ ol, mən əla işləyirəm! Bütün sistemlərim tam gücü ilə işləyir. Bəs sən necəsən?"
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            
        else:
            try:
                response = st.session_state.chat.send_message(prompt, stream=True)
                
                def gen_words():
                    for chunk in response:
                        # DÜZƏLİŞ 2: Xətalı qırıntılara qarşı zireh
                        try:
                            if chunk.text:
                                yield chunk.text
                        except Exception:
                            continue
                
                full_res = st.write_stream(gen_words)
                
                # DÜZƏLİŞ 3: Əgər cavab bomboş gələrsə, səssiz qalmasın!
                if not full_res or str(full_res).strip() == "":
                    full_res = "Bağışla, Patron, bu sualı emal edərkən kiçik bir kəsinti oldu. Fikrini bir az da fərqli cür yaza bilərsən?"
                    st.markdown(full_res)

                st.session_state.messages.append({"role": "assistant", "content": full_res})
                
            except Exception as e:
                st.error(f"Sistem xətası baş verdi. API açarını yoxla: {e}")

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
