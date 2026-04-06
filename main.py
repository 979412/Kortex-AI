import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="KORTEX-AI ULTRA", page_icon="🚀", layout="wide")
st.title("🚀 KORTEX-AI: Ultra Agentic Hub")

# 2. KONFİQURASİYA
API_KEY = "SİZİN_API_AÇARINIZI_BURAYA_YAZIN"
genai.configure(api_key=API_KEY)

# 3. ALƏTLƏRİN TƏRİFİ
def internetde_axtaris_et(sorgu: str):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(sorgu, max_results=3)]
            return "\n".join(results)
    except: return "Məlumat tapılmadı."

def video_ve_media_generasiyası(tesvir: str):
    return f"VEO 3.1: '{tesvir}' üçün media planı quruldu."

def ofis_ve_sened_idareetmesi(emeliyyat: str):
    return f"OFFICE: '{emeliyyat}' icra edildi."

# Funksiya xəritəsi (Modelin tanıması üçün)
tools_map = {
    "internetde_axtaris_et": internetde_axtaris_et,
    "video_ve_media_generasiyası": video_ve_media_generasiyası,
    "ofis_ve_sened_idareetmesi": ofis_ve_sened_idareetmesi
}

# 4. MODEL VƏ YADDAŞ
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        tools=[internetde_axtaris_et, video_ve_media_generasiyası, ofis_ve_sened_idareetmesi]
    )
    st.session_state.chat = model.start_chat(history=[])

# 5. MESAJLARI GÖSTƏR
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. ƏSAS ÇAT MEXANİZMİ (XƏTASIZ VERSİYA)
if prompt := st.chat_input("KORTEX-ə əmr verin..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Agentlər müzakirə edir..."):
            try:
                # 1. İlk mesajı göndəririk
                response = st.session_state.chat.send_message(prompt)
                
                # 2. Əgər model funksiya çağırmaq istəyirsə (Loop başlayır)
                while response.candidates[0].content.parts[0].function_call:
                    fc = response.candidates[0].content.parts[0].function_call
                    fn_name = fc.name
                    fn_args = fc.args
                    
                    # Funksiyanı işlədirik
                    if fn_name in tools_map:
                        arg_val = list(fn_args.values())[0] if fn_args else ""
                        fn_result = tools_map[fn_name](arg_val)
                        
                        # Nəticəni modelə geri göndəririk ki, bizə insan dilində cavab versin
                        response = st.session_state.chat.send_message(
                            genai.types.Content(
                                parts=[genai.types.Part.from_function_response(
                                    name=fn_name,
                                    response={'result': fn_result}
                                )]
                            )
                        )
                    else:
                        break

                # 3. Yekun mətni çıxarırıq
                final_text = response.text
                st.markdown(final_text)
                st.session_state.messages.append({"role": "assistant", "content": final_text})
                
            except Exception as e:
                # Əgər model birbaşa mətn qaytarırsa və .text xətası verirsə, alternativ yol:
                try:
                    alt_text = response.candidates[0].content.parts[0].text
                    st.markdown(alt_text)
                    st.session_state.messages.append({"role": "assistant", "content": alt_text})
                except:
                    st.error(f"Sistem xətası: {str(e)}")
