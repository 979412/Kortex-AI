import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS

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
            neticeler = list(ddgs.text(sorgu, max_results=3))
            return str(neticeler)
    except Exception as e:
        return f"Axtarış xətası: {e}"

# 4. YADDAŞIN VƏ MODELİN QURULMASI
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    system_instruction = """
    Sən KORTEX-AI-san. Qlobal bazarları analiz edən, riskləri hesablayan və 
    yüksək gəlirli layihələr üçün addım-addım biznes planları hazırlayan strateqsən.
    Sənə sual veriləndə mütləq cavab ver. Əgər ehtiyac varsa internetdə axtarış et, 
    amma sadə söhbətlərdə (məs: salam) birbaşa və səmimi cavab ver.
    """
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        system_instruction=system_instruction,
        tools=[biznes_budce_hesabla, internetde_axtaris_et]
    )
    # Boş tarixçə ilə başlat
    st.session_state.chat = model.start_chat(history=[])

# 5. KÖHNƏ MESAJLARI EKRANDA GÖSTƏRMƏK
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. YENİ SÖHBƏT PƏNCƏRƏSİ (Təkmilləşdirilmiş Versiya)
if prompt := st.chat_input("Sualınızı bura yazın..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("KORTEX analiz edir..."):
            try:
                # Modeldən cavab alırıq
                response = st.session_state.chat.send_message(prompt)
                
                # Gemini bəzən mətni birbaşa vermir, partlar daxilindən çıxarırıq
                full_response = ""
                if response.candidates and response.candidates[0].content.parts:
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'text'):
                            full_response += part.text
                
                # Əgər hələ də cavab yoxdursa (funksiya işləyib amma mətn gəlməyibsə)
                if not full_response:
                    full_response = "Analiz tamamlandı. Başqa nə kömək edə bilərəm?"
                
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Xəta baş verdi: {str(e)}")
