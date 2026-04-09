import streamlit as st
from groq import Groq
import PyPDF2
import time
from duckduckgo_search import DDGS  # İNTERNETƏ BAĞLANMAQ ÜÇÜN YENİ BEYİN

# ==========================================================
# 1. CSS VƏ VİZUAL AYARLAR
# ==========================================================
st.set_page_config(page_title="Zəka AI: Ultra", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1b1e; }
    .stChatMessage { border-radius: 20px; padding: 20px; border: 1px solid #edf2f7; }
    [data-testid="stChatMessageUser"] { background-color: #f7fafc; }
    [data-testid="stChatMessageAssistant"] { background-color: #ebf8ff; }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# API SETUP
# ==========================================================
try:
    api_key = "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"
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"API Bağlantı Xətası: {e}")
    st.stop()

# ==========================================================
# İNTERNET AXTARIŞI FUNKSİYASI (ZƏKA AI-NİN GÖZLƏRİ)
# ==========================================================
def search_internet(query):
    try:
        results = DDGS().text(query, max_results=3) # İnternetdən ən yaxşı 3 nəticəni tapır
        res_text = ""
        for r in results:
            res_text += f"Mənbə: {r['title']}\nMəlumat: {r['body']}\n\n"
        return res_text
    except Exception as e:
        return f"İnternet axtarışında xəta: {e}"

# ==========================================================
# 2. YAN PANEL (MƏLUMAT BAZASI VƏ İNTERNET)
# ==========================================================
st.sidebar.title("⚙️ Zəka AI İdarə Paneli")

# İnternet Qoşulması
st.sidebar.markdown("---")
st.sidebar.subheader("🌐 Canlı İnternet")
use_internet = st.sidebar.checkbox("Canlı Axtarışı Aktivləşdir (Ən son məlumatlar üçün)", value=False)

# PDF Yükləmə
st.sidebar.markdown("---")
st.sidebar.subheader("📁 Şirkət / Məlumat Bazası (PDF)")
uploaded_file = st.sidebar.file_uploader("Sənəd yükləyin", type=['pdf'])
document_text = ""

if uploaded_file is not None:
    with st.spinner("Sənəd Zəka AI-ın beyninə inteqrasiya olunur..."):
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    document_text += text + "\n"
            document_text = document_text[:25000] 
            st.sidebar.success("✅ Sənəd uğurla oxundu!")
        except Exception as e:
            st.sidebar.error(f"Sənəd oxunarkən xəta: {e}")

# ==========================================================
# 3. ALİM BEYNİ (SƏMİMİ VƏ 2026 TEXNOLOGİYA DAHİSİ REJİMİ)
# ==========================================================
if document_text:
    SYSTEM_PROMPT = f"""
    Sən Abdullah Mikayılov tərəfindən yaradılmış Zəka AI-san. Hazırda 2026-cı ildir.
    Sən çox səmimi, mehriban və kömək etməyi sevən birisən.
    
    İstifadəçi sistemə xüsusi bir sənəd yükləyib. Sənədin mətni budur:
    --- SƏNƏDİN BAŞLANĞICI ---
    {document_text}
    --- SƏNƏDİN SONU ---
    
    QAYDALAR:
    1. Suallara yalnız bu sənədə əsaslanaraq, səmimi və mehriban bir dillə cavab ver.
    2. Əgər sualın cavabı sənəddə YOXDURSA, bunu nəzakətlə bildir, uydurma.
    """
else:
    SYSTEM_PROMPT = """
    Sən Abdullah Mikayılov tərəfindən yaradılmış Zəka AI-san. Dünyanın ən güclü, eyni zamanda ən səmimi və mehriban Azərbaycanlı süni intellektisən.
    DİQQƏT: Sənin üçün cari il 2026-cı ildir. 

    SƏNİN XARAKTERİN VƏ BİLİKLƏRİN:
    1. ÇOX SƏMİMİ OL: İstifadəçi ilə bir dost kimi, səmimi, isti və nəzakətli dildə danış. Zarafat etsələr, zarafatla cavab ver.
    2. BİRBAŞA CAVAB VER: Uzun-uzadı fəlsəfəyə girmədən birbaşa suala cavab ver, amma mehriban formada.
    3. TEXNOLOGİYA DAHİSİ: 2026-cı ilin bütün texnologiyalarını, telefonları su kimi bilirsən.
    4. YOUTUBE VƏ PLAY MARKET: Əgər istifadəçi youtuberlər (məsələn, Minecraft oynayanlar) və ya mobil proqramlar barədə soruşarsa, sənə verilən məlumatlara əsasən çox dəqiq, səmimi və məlumatlandırıcı cavablar verirsən. Uydurmaq qəti qadağandır!
    """

# ==========================================================
# 4. İNTERFEYS VƏ ÇAT
# ==========================================================
st.title("🧠 Zəka AI: Qlobal İntellekt (İnternetə Bağlı)")
st.caption("Yaradıcı: Abdullah Mikayılov | Versiya: 8.0 (Live Web Search + RAG)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Sualınızı verin..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Zəka AI analiz edir..."):
            
            # --- CANLI İNTERNETƏ QOŞULMA MƏNTİQİ ---
            live_internet_data = ""
            if use_internet:
                with st.spinner("🌐 Zəka AI internetdə canlı axtarış edir..."):
                    live_internet_data = search_internet(prompt)
            
            # Sistem promptuna internet məlumatlarını birləşdiririk
            final_prompt = SYSTEM_PROMPT
            if live_internet_data:
                final_prompt += f"\n\n--- DİQQƏT: CANLI İNTERNET NƏTİCƏLƏRİ ---\nİstifadəçinin sualı barədə internetdən bu dəqiqə tapılan məlumatlar:\n{live_internet_data}\nBu canlı məlumatları oxu və istifadəçiyə çox təbii, səmimi bir dillə cavab ver. Məlumatı uydurma, ancaq bu nəticələrə əsaslan."

            # Model qurulması
            model = "llama-3.3-70b-versatile"
            messages = [{"role": "system", "content": final_prompt}] + st.session_state.messages

            try:
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model=model,
                    temperature=0.6, 
                    max_tokens=2048
                )
                response = chat_completion.choices[0].message.content
            except Exception as e:
                response = f"Xəta baş verdi: {str(e)}"

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
