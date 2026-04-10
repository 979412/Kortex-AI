import streamlit as st
from groq import Groq
import PyPDF2
import time
from duckduckgo_search import DDGS  # İNTERNETƏ BAĞLANMAQ ÜÇÜN BEYİN

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
        # Daha çox və dəqiq məlumat tapması üçün nəticə sayını 5-ə qaldırdım
        results = DDGS().text(query, max_results=5) 
        res_text = ""
        for r in results:
            res_text += f"Mənbə: {r['title']}\nMəlumat: {r['body']}\n\n"
        return res_text
    except Exception as e:
        return ""

# ==========================================================
# 2. YAN PANEL (MƏLUMAT BAZASI VƏ İNTERNET)
# ==========================================================
st.sidebar.title("⚙️ Zəka AI İdarə Paneli")

# İnternet Qoşulması (ARTIQ AVTOMATİK AKTİVDİR)
st.sidebar.markdown("---")
st.sidebar.subheader("🌐 Canlı İnternet")
use_internet = st.sidebar.checkbox("Canlı Axtarışı Aktivləşdir (Avtomatik İşləyir)", value=True) # VALUE=TRUE EDİLDİ

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
# 3. ALİM BEYNİ (TAM DƏQİQ VƏ İNTERNETƏ BAĞLI REJİM)
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
    Sən Abdullah Mikayılov tərəfindən yaradılmış Zəka AI-san. Dünyanın ən güclü, səmimi və dəqiq Azərbaycanlı süni intellektisən.
    DİQQƏT: Sənin üçün cari il 2026-cı ildir. Sən Google və mənim kimi birbaşa internet məlumatları ilə qidalanırsan.

    QƏTİ QAYDALAR VƏ BİLİKLƏRİN:
    1. ADLARI UYDURMA: Əgər istifadəçi "Boralo" və ya hər hansı bir youtuber/oyunçu soruşursa və sən onu tanımadınsa, QƏTİYYƏN ona oxşayan başqa bir sözdən (məsələn, "Borax" adlı mineraldan) danışma! 
    2. DÜRÜSTLÜK: Sənə verilən canlı internet nəticələrində o adam barədə məlumat yoxdursa, dürüstcə de: "İnternetdə axtarış etdim, amma bu adda birini tapa bilmədim." Xəyal gücündən istifadə etmək qadağandır.
    3. YOUTUBE VƏ PLAY MARKET: Ən son trendləri, oyunları və proqramları sənə verilən canlı internet axtarışına əsasən dəqiq və səmimi izah et.
    """

# ==========================================================
# 4. İNTERFEYS VƏ ÇAT
# ==========================================================
st.title("🧠 Zəka AI: Qlobal İntellekt")
st.caption("Yaradıcı: Abdullah Mikayılov | Versiya: 8.2 (Avtomatik İnternet Axtarışı)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("İstədiyiniz məlumatı, Youtuberi və ya xəbəri soruşun..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Zəka AI analiz edir..."):
            
            # --- AVTOMATİK İNTERNETƏ QOŞULMA MƏNTİQİ ---
            live_internet_data = ""
            if use_internet:
                with st.spinner("🌐 Zəka AI internetdə məlumat toplayır..."):
                    live_internet_data = search_internet(prompt)
            
            # Sistem promptuna internet məlumatlarını birləşdiririk
            final_prompt = SYSTEM_PROMPT
            if live_internet_data:
                final_prompt += f"\n\n--- DİQQƏT: CANLI İNTERNET NƏTİCƏLƏRİ ---\nİstifadəçinin sualı barədə internetdən bu dəqiqə tapılan ən son məlumatlar bunlardır:\n{live_internet_data}\nBu canlı məlumatları oxu və istifadəçiyə çox təbii, səmimi bir dillə cavab ver. Əgər məlumat yoxdursa, uydurma!"

            # Model qurulması
            model = "llama-3.3-70b-versatile"
            messages = [{"role": "system", "content": final_prompt}] + st.session_state.messages

            try:
                # Dəqiqlik üçün temperatur 0.3 edildi.
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
