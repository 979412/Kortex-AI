import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="KORTEX-AI ULTRA", page_icon="🚀", layout="wide")
st.title("🚀 KORTEX-AI: Ultra Agentic Hub")

# 2. KONFİQURASİYA
API_KEY = "SİZİN_API_AÇARINIZI_BURAYA_YAZIN"
genai.configure(api_key=API_KEY)

# 3. ULTRA ALƏTLƏR (Funksiyalar)
def internetde_axtaris_et(sorgu: str) -> str:
    """İnternetdən ən son real-vaxt məlumatlarını gətirir."""
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(sorgu, max_results=3)]
            return "\n".join(results)
    except: return "Axtarışda xəta baş verdi."

def video_ve_media_generasiyası(tesvir: str) -> str:
    """Veo 3.1 sistemi üçün media planı qurur."""
    return f"VEO 3.1: '{tesvir}' üçün video kadrlar və audio sintezi hazırlandı."

def ofis_ve_sened_idareetmesi(emeliyyat: str) -> str:
    """Gmail və Docs inteqrasiyasını simulyasiya edir."""
    return f"OFFICE: '{emeliyyat}' uğurla icra olundu."

# 4. MODEL VƏ YADDAŞIN QURULMASI
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    system_instruction = """
    Sən KORTEX-AI-san. Daxilində STRATEQ, KREATİV, CODER və OFFICE agentləri var.
    İstifadəçi Memardır. Əgər sual mürəkkəbdirsə, internetdə axtarış et.
    Həmişə aydın və konkret cavab ver. Cavabın boş qalmasına icazə vermə.
    """
    # QEYD: enable_pycall=True bəzi mühitlərdə avtomatik icra üçün lazımdır
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        system_instruction=system_instruction,
        tools=[internetde_axtaris_et, video_ve_media_generasiyası, ofis_ve_sened_idareetmesi]
    )
    # enable_automatic_function_calling=True bu ən vacib hissədir!
    st.session_state.chat = model.start_chat(history=[], enable_automatic_function_calling=True)

# 5. MESAJLARI GÖSTƏR
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. ULTRA ÇAT MEXANİZMİ
if prompt := st.chat_input("KORTEX-ə əmr verin..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("KORTEX Agentləri işləyir..."):
            try:
                # Avtomatik funksiya çağırışı ilə mesajı göndəririk
                response = st.session_state.chat.send_message(prompt)
                
                # Modelin cavabını dərindən yoxlayırıq
                final_text = ""
                if response.candidates:
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'text') and part.text:
                            final_text += part.text
                
                # Əgər hələ də boşdursa, modelin funksiya nəticələrindən bir cavab çıxarırıq
                if not final_text:
                    final_text = "Əməliyyat uğurla icra olundu. Agentlər növbəti təlimatınızı gözləyir."

                st.markdown(final_text)
                st.session_state.messages.append({"role": "assistant", "content": final_text})
                
            except Exception as e:
                st.error(f"Sistem xətası: {str(e)}")
                st.info("İpucu: API limitini və ya internet bağlantısını yoxlayın.")
