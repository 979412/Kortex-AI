import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="KORTEX-AI ULTRA", page_icon="🚀", layout="wide")
st.title("🚀 KORTEX-AI: Ultra Agentic Hub")

# 2. KONFİQURASİYA (API açarını bura yaz)
API_KEY = "SİZİN_API_AÇARINIZI_BURAYA_YAZIN"
genai.configure(api_key=API_KEY)

# 3. ALƏTLƏR (Tools)
def internetde_axtaris_et(sorgu: str) -> str:
    """İnternetdən ən son məlumatları gətirir."""
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(sorgu, max_results=3)]
            return "\n".join(results)
    except: return "Məlumat tapılmadı."

def video_ve_media_generasiyası(tesvir: str) -> str:
    return f"VEO 3.1: '{tesvir}' üçün media planı quruldu."

def ofis_ve_sened_idareetmesi(emeliyyat: str) -> str:
    return f"OFFICE: '{emeliyyat}' icra edildi."

# 4. YADDAŞ VƏ MODELİN QURULMASI
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    # SİSTEM TƏLİMATI: Hər şeyə cavab verməsini təmin edirik
    system_instruction = """
    Sən KORTEX-AI-san. Heç bir halda cavabsız qalma. 
    İstifadəçi nə yazsa (salam, necəsən, hər hansı dil və ya sual), mütləq reaksiya ver. 
    Əgər alətlərdən (tools) istifadə edirsənsə, nəticəni gözlə və insan dilində yekun cavab yaz.
    """
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        system_instruction=system_instruction,
        tools=[internetde_axtaris_et, video_ve_media_generasiyası, ofis_ve_sened_idareetmesi]
    )
    # AVTOMATİK FUNKSİYA ÇAĞIRIŞI AKTİV EDİLDİ
    st.session_state.chat = model.start_chat(history=[], enable_automatic_function_calling=True)

# 5. MESAJLARI GÖSTƏR
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. ƏSAS ÇAT MEXANİZMİ
if prompt := st.chat_input("KORTEX-ə bir şey yazın..."):
    # İstifadəçi mesajını ekrana yaz və yaddaşa al
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI Cavab bölməsi
    with st.chat_message("assistant"):
        response_placeholder = st.empty() # Cavab üçün yer ayırırıq
        with st.spinner("KORTEX düşünür və analiz edir..."):
            try:
                # Modeli çağırırıq (Avtomatik funksiya dövrü daxildə işləyir)
                response = st.session_state.chat.send_message(prompt)
                
                # Cavabı parçalardan yığırıq
                full_text = ""
                if response.candidates:
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'text'):
                            full_text += part.text
                
                # Əgər hələ də boşdursa, modelin daxili strukturu vasitəsilə mətni məcburi çıxarırıq
                if not full_text:
                    full_text = response.text if hasattr(response, 'text') else "Əməliyyat icra olundu. Növbəti sualınızı gözləyirəm."

                response_placeholder.markdown(full_text)
                st.session_state.messages.append({"role": "assistant", "content": full_text})
                
            except Exception as e:
                # Xəta olarsa, səbəbini göstər və donmağı dayandır
                error_msg = f"Sistem xətası baş verdi: {str(e)}"
                response_placeholder.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
