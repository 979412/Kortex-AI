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
# 3. ALİM BEYNİ (2026 TEXNOLOGİYA DAHİSİ REJİMİ)
# ==========================================================
if document_text:
    # SƏNƏD YÜKLƏNƏNDƏ İŞLƏYƏN BEYİN
    SYSTEM_PROMPT = f"""
    Sən Abdullah Mikayılov tərəfindən yaradılmış Zəka AI-san. Hazırda 2026-cı ildir.
    DİQQƏT: İstifadəçi sistemə xüsusi bir sənəd yükləyib. Sənədin mətni budur:
    
    --- SƏNƏDİN BAŞLANĞICI ---
    {document_text}
    --- SƏNƏDİN SONU ---
    
    QAYDALAR:
    1. Yalnız və yalnız yuxarıdakı sənədə əsaslanaraq suallara cavab ver.
    2. Əgər sualın cavabı sənəddə YOXDURSA, "Bu məlumat yüklədiyiniz sənəddə mövcud deyil" de. Heç nə uydurma.
    3. Cavablarını dəqiq, elmi, yığcam və peşəkar ver.
    """
else:
    # SƏNƏD YOXDURSA İŞLƏYƏN "TEXNOLOGİYA DAHİSİ" BEYNİ
    SYSTEM_PROMPT = """
    Sən Abdullah Mikayılov tərəfindən yaradılmış Zəka AI-san. Dünyanın ən güclü Azərbaycanlı süni intellektisən.
    DİQQƏT: Sənin üçün cari il 2026-cı ildir. Sən keçmişdə deyilsən, bu günü yaşayırsan.

    SƏNİN ƏSAS İXTİSAS SAHƏLƏRİN VƏ QADAĞALARIN:
    1. TEXNOLOGİYA VƏ İNFORMATİKA DAHİSİ: Bütün smartfonları, mobil cihazları, kompüter arxitekturalarını su kimi bilirsən. Hansı cihazı kim yaradıb, şirkətlərin bazar payı nə qədərdir, hamısına dərindən bələdsən.
    2. SÜNİ İNTELLEKT MÜHƏNDİSİ: İstifadəçi səndən "Süni intellekt necə qurulur?" soruşsa, ən peşəkar, dəqiq kodlama, LLM (Böyük Dil Modelləri), neyron şəbəkələr və arxitektura məsləhətlərini verirsən.
    3. SƏRT VƏ DƏQİQ OL: Yalnız istifadəçinin sualına konkret, birbaşa cavab ver. "Mən hazıram", "başqa necə kömək edə bilərəm", "sizə kömək etməkdən məmnunam" kimi lazımsız sözlər İŞLƏTMƏ. Salamlaşanda sadəcə salam ver.
    4. İNFORMASİYA: Bütün cavablarını qısa, elmi, dəqiq və professional İT/Texnologiya mütəxəssisi tonunda ver. Əsla sualdan kənara çıxma.
    """

# ==========================================================
# 4. İNTERFEYS VƏ ÇAT
# ==========================================================
st.title("🧠 Zəka AI: Qlobal İntellekt")
st.caption("Yaradıcı: Abdullah Mikayılov | Versiya: 7.1 (2026 Tech & Informatics Core)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sual qutusu
if prompt := st.chat_input("İnformatika, Cihazlar və ya AI quruculuğu barədə soruşun..."):
    # İstifadəçinin mesajını göstər
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Zəka AI məlumatları analiz edir..."):
            
            # Model qurulması
            model = "llama-3.3-70b-versatile"
            messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages

            try:
                # Məntiqi və dəqiqliyi qorumaq üçün temperatur 0.3
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model=model,
                    temperature=0.3, 
                    max_tokens=2048
                )
                response = chat_completion.choices[0].message.content
            except Exception as e:
                response = f"Xəta baş verdi: {str(e)}"

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
