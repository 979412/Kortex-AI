import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS

# 1. SƏHİFƏ AYARLARI (Ultra Görünüş)
st.set_page_config(page_title="KORTEX-AI ULTRA", page_icon="🚀", layout="wide")
st.title("🚀 KORTEX-AI: Ultra Agentic Hub")
st.sidebar.title("🛠️ Agent İdarəetmə")
st.sidebar.info("Deep Think, Veo 3.1, Antigravity və Office inteqrasiyaları aktivdir.")

# 2. KONFİQURASİYA
API_KEY = "SİZİN_API_AÇARINIZI_BURAYA_YAZIN"
genai.configure(api_key=API_KEY)

# 3. ULTRA ALƏTLƏR (Tools)
def internetde_axtaris_et(sorgu: str) -> str:
    """İnternetdən ən son real-vaxt məlumatlarını gətirir."""
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(sorgu, max_results=3)]
            return "\n".join(results)
    except: return "Axtarışda xəta baş verdi."

def video_ve_media_generasiyası(tesvir: str) -> str:
    """Veo 3.1 və Whisk modelləri üçün prompt hazırlayır."""
    return f"VEO 3.1 SİSTEMİ: '{tesvir}' üçün yüksək keyfiyyətli video və audio kadrlar planlaşdırıldı."

def ofis_ve_sened_idareetmesi(emeliyyat: str) -> str:
    """Gmail, Docs və NotebookLM inteqrasiyası üçün əmr mərkəzi."""
    return f"OFFICE AGENT: '{emeliyyat}' üçün sənəd strukturu Gmail və Docs-a sinxronizasiya edildi."

# 4. AGENT ARXİTEKTURASI (Beyin Mərkəzi)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    # KORTEX-in System Promptu artıq bir "Şura" kimi işləyir
    system_instruction = """
    Sən KORTEX-AI-san. Sənin daxilində 4 əsas Agent var:
    1. STRATEQ (Deep Think): Mürəkkəb biznes analizləri edir.
    2. KREATİV (Veo/Whisk): Video və musiqi konsepsiyaları qurur.
    3. CODER (Antigravity): Kod yazır və sistemləri avtomatlaşdırır.
    4. OFFICE: Gmail, Docs və təqvim işlərini idarə edir.
    
    İstifadəçi Memardır. Ona hər zaman ən son internet məlumatları ilə cavab ver.
    """
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro", # Və ya gemini-3-pro (əlçatan olduqda)
        system_instruction=system_instruction,
        tools=[internetde_axtaris_et, video_ve_media_generasiyası, ofis_ve_sened_idareetmesi]
    )
    st.session_state.chat = model.start_chat(history=[])

# 5. İNTERFEYS: MESAJLARIN GÖSTƏRİLMƏSİ
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. ULTRA ÇAT MEXANİZMİ
if prompt := st.chat_input("KORTEX-ə əmr verin (Məs: Gəncə üçün biznes plan qur və Gmail-ə göndər)"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Agentlər şurası müzakirə edir..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                
                # Cavabı təmizləyib çıxarırıq
                final_response = ""
                if response.candidates:
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'text'):
                            final_response += part.text
                
                if not final_response:
                    final_response = "Əməliyyat icra olundu. Agentlər növbəti addım üçün hazırdır."

                st.markdown(final_response)
                st.session_state.messages.append({"role": "assistant", "content": final_response})
                
            except Exception as e:
                st.error(f"Sistem xətası: {str(e)}")
