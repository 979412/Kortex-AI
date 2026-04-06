import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS # İnternet axtarışı kitabxanası əlavə olundu

# 1. SƏHİFƏNİN DİZAYNI VƏ BAŞLIĞI
st.set_page_config(page_title="KORTEX-AI", page_icon="🧠", layout="centered")
st.title("🧠 KORTEX-AI: Strateji Mərkəz")
st.caption("Memar üçün xüsusi olaraq yaradılmış biznes intellekti")

# 2. API AÇARI (Öz açarını bura dırnaqların içinə yaz)
API_KEY = "SİZİN_API_AÇARINIZI_BURAYA_YAZIN"
genai.configure(api_key=API_KEY)

# 3. KORTEX ÜÇÜN HESABLAMA VƏ AXTARIŞ ALƏTLƏRİ
def biznes_budce_hesabla(gelir: float, xerc: float, vergi_faizi: float) -> str:
    """Biznesin büdcəsini və vergisini dəqiq hesablayır."""
    vergi_meblegi = (gelir - xerc) * (vergi_faizi / 100)
    xalis_qazanc = (gelir - xerc) - vergi_meblegi
    if xalis_qazanc < 0:
        return f"DİQQƏT: Ziyan: {abs(xalis_qazanc)} AZN. Vergi: {vergi_meblegi} AZN"
    else:
        return f"UĞURLU: Xalis qazanc {xalis_qazanc} AZN. Vergi: {vergi_meblegi} AZN"

def internetde_axtaris_et(sorgu: str) -> str:
    """KORTEX-AI bu alətdən istifadə edərək internetdə ən son məlumatları və xəbərləri axtarır."""
    try:
        with DDGS() as ddgs:
            # İnternetdən ən uyğun 3 nəticəni tapıb gətirir
            neticeler = list(ddgs.text(sorgu, max_results=3))
            return str(neticeler)
    except Exception as e:
        return f"Axtarış xətası: {e}"

# 4. YADDAŞIN VƏ MODELİN QURULMASI (Streamlit Session State istifadə edərək)
if "chat" not in st.session_state:
    # Model yalnız səhifə ilk dəfə açılanda yüklənir
    system_instruction = """
    Sən KORTEX-AI-san. Qlobal bazarları analiz edən, riskləri hesablayan və 
    yüksək gəlirli layihələr üçün addım-addım biznes planları hazırlayan strateqsən.
    Sənə sual veriləndə köhnə məlumatlarla kifayətlənmə, mütləq internetdə axtarış edib ən son məlumatları tap.
    """
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        system_instruction=system_instruction,
        tools=[biznes_budce_hesabla, internetde_axtaris_et] # HƏR İKİ ALƏT BURA ƏLAVƏ OLUNDU
    )
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []

# 5. KÖHNƏ MESAJLARI EKRANDA GÖSTƏRMƏK
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. YENİ SÖHBƏT PƏNCƏRƏSİ
if prompt := st.chat_input("Sualınızı bura yazın..."):
    # Sənin yazdığını ekrana çıxarırıq və yaddaşa salırıq
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # KORTEX-AI-dan cavab alırıq
    with st.chat_message("assistant"):
        with st.spinner("KORTEX analiz edir... (İnternetdə axtarış edə bilər)"): 
            try:
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
                # KORTEX-in cavabını da yaddaşa salırıq
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Xəta baş verdi: {e}")
