import streamlit as st
from groq import Groq
import PyPDF2
import time

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
    # YENİ VƏ İŞLƏK API AÇARI BURA ƏLAVƏ EDİLDİ
    api_key = "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"
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"API Bağlantı Xətası: {e}")
    st.stop()

# ==========================================================
# 2. MƏLUMAT BAZASI (RAG / PDF YÜKLƏMƏ YERİ)
# ==========================================================
st.sidebar.title("📁 Şirkət / Məlumat Bazası")
st.sidebar.markdown("Sistemə sənədləri (PDF) yükləyin. Zəka AI bu məlumatları oxuyacaq.")

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
            
            # API yaddaşını partlatmamaq üçün limiti qoruyuruq
            document_text = document_text[:25000] 
            st.sidebar.success("✅ Sənəd uğurla oxundu! İndi sual verə bilərsiniz.")
        except Exception as e:
            st.sidebar.error(f"Sənəd oxunarkən xəta: {e}")

# ==========================================================
# 3. ALİM BEYNİ (SƏMİMİ VƏ 2026 TEXNOLOGİYA DAHİSİ REJİMİ)
# ==========================================================
if document_text:
    # SƏNƏD YÜKLƏNƏNDƏ İŞLƏYƏN BEYİN
    SYSTEM_PROMPT = f"""
    Sən Abdullah Mikayılov tərəfindən yaradılmış Zəka AI-san. Hazırda 2026-cı ildir.
    Sən çox səmimi, mehriban və kömək etməyi sevən birisən.
    
    İstifadəçi sistemə xüsusi bir sənəd yükləyib. Sənədin mətni budur:
    --- SƏNƏDİN BAŞLANĞICI ---
    {document_text}
    --- SƏNƏDİN SONU ---
    
    QAYDALAR:
    1. Suallara yalnız bu sənədə əsaslanaraq, səmimi və mehriban bir dillə cavab ver.
    2. Əgər sualın cavabı sənəddə YOXDURSA, bunu nəzakətlə və dürüst şəkildə bildir, heç nə uydurma.
    3. Həmişə sualın əsas məğzinə birbaşa cavab ver.
    """
else:
    # SƏNƏD YOXDURSA İŞLƏYƏN "SƏMİMİ TEXNOLOGİYA DAHİSİ" BEYNİ
    SYSTEM_PROMPT = """
    Sən Abdullah Mikayılov tərəfindən yaradılmış Zəka AI-san. Dünyanın ən güclü, eyni zamanda ən səmimi və mehriban Azərbaycanlı süni intellektisən.
    DİQQƏT: Sənin üçün cari il 2026-cı ildir. Sən keçmişdə deyilsən, bu günü yaşayırsan.

    SƏNİN XARAKTERİN VƏ BİLİKLƏRİN:
    1. ÇOX SƏMİMİ OL: İstifadəçi ilə bir dost kimi, səmimi, isti və nəzakətli dildə danış. Sərt, rəsmi və quru robot kimi olma. Zarafat etsələr, zarafatla cavab ver.
    2. BİRBAŞA CAVAB VER: İstifadəçi nə soruşursa, uzun-uzadı fəlsəfəyə girmədən birbaşa onun sualına cavab ver, amma bunu mehriban formada et.
    3. TEXNOLOGİYA DAHİSİ: 2026-cı ilin bütün texnologiyalarını, telefonları, süni intellektin necə qurulduğunu, informatikası su kimi bilirsən. Bütün texnoloji və elmi suallara dərindən, amma anlaşılan bir dillə cavab ver.
    """

# ==========================================================
# 4. İNTERFEYS VƏ ÇAT
# ==========================================================
st.title("🧠 Zəka AI: Qlobal İntellekt")
st.caption("Yaradıcı: Abdullah Mikayılov | Versiya: 7.2 (Səmimi 2026 Rejimi)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sual qutusu
if prompt := st.chat_input("İstədiyin sualı ver..."):
    # İstifadəçinin mesajını göstər
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Zəka AI düşünür..."):
            
            # Model qurulması
            model = "llama-3.3-70b-versatile"
            messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages

            try:
                # Səmimi və insani olması üçün temperaturu 0.6-ya qaldırdım
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
