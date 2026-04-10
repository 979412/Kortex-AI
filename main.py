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
# İNTERNET AXTARIŞI FUNKSİYASI
# ==========================================================
def search_internet(query):
    try:
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

# İNTERNET QOŞULMASI
st.sidebar.markdown("---")
st.sidebar.subheader("🌐 Canlı İnternet")
use_internet = st.sidebar.checkbox("Ağıllı Axtarış Agentini Aktivləşdir", value=True)

# PDF YÜKLƏMƏ
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
# 3. ALİM BEYNİ (SƏMİMİ VƏ DƏQİQ REJİM)
# ==========================================================
if document_text:
    SYSTEM_PROMPT = f"""
    Sən Abdullah Mikayılov tərəfindən yaradılmış Zəka AI-san. 
    İstifadəçi sənəd yükləyib. Mətn budur: {document_text}
    QAYDALAR: Yalnız bu sənədə əsaslanaraq səmimi cavab ver.
    """
else:
    SYSTEM_PROMPT = """
    Sən Abdullah Mikayılov tərəfindən yaradılmış Zəka AI-san. Dünyanın ən güclü, səmimi Azərbaycanlı süni intellektisən.
    DİQQƏT: Sənin üçün cari il 2026-cı ildir. Sən canlı internet məlumatları ilə qidalanırsan.

    QƏTİ QAYDALAR:
    1. YOUTUBERLƏR VƏ OYUNLAR: Əgər sənə internet nəticəsində "BoraLo" (Minecraft youtuberi) və ya başqa biri barədə məlumat gəlibsə, yalnız o faktlardan danış. Əsla kimyəvi maddələrdən və ya "Borax"dan danışma!
    2. DÜRÜSTLÜK: Sənə verilən canlı internet axtarışında məlumat yoxdursa uydurma.
    3. Tərzi: Çox səmimi və dost kimi cavab ver.
    """

# ==========================================================
# 4. İNTERFEYS VƏ ÇAT
# ==========================================================
st.title("🧠 Zəka AI: Qlobal İntellekt")
st.caption("Yaradıcı: Abdullah Mikayılov | Versiya: 9.0 (İki Mərhələli Ağıllı Agent)")

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
        
        # --- İKİ MƏRHƏLƏLİ AĞILLI AXTARIŞ (GEMİNİ MƏNTİQİ) ---
        live_internet_data = ""
        if use_internet:
            # MƏRHƏLƏ 1: Sualdan təmiz Açar Söz çıxarmaq (Bununla axtarış mükəmməl olacaq)
            with st.spinner("🧠 Zəka AI axtarış üçün açar sözləri düşünür..."):
                try:
                    kw_chat = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Sən yalnız axtarış sözləri yazan robotsan. Verilən cümlədən ən vacib 2-3 axtarış sözünü yaz. Şəkilçiləri sil. Nümunə: 'boralonu taniyirsan' -> 'Boralo youtuber'. Nümunə: 'Baki hava' -> 'Baki hava durumu'."},
                            {"role": "user", "content": prompt}
                        ],
                        model="llama-3.3-70b-versatile",
                        temperature=0.1,
                        max_tokens=15
                    )
                    search_query = kw_chat.choices[0].message.content.replace("'", "").replace('"', '').strip()
                except:
                    search_query = prompt

            # MƏRHƏLƏ 2: Təmiz açar sözlə internetdə axtarış etmək
            with st.spinner(f"🌐 İnternetdə axtarılır: '{search_query}' ..."):
                live_internet_data = search_internet(search_query)
        
        # MƏRHƏLƏ 3: Yekun cavabı hazırlamaq
        with st.spinner("Zəka AI cavab hazırlayır..."):
            final_prompt = SYSTEM_PROMPT
            if live_internet_data:
                final_prompt += f"\n\n--- DİQQƏT: CANLI İNTERNET NƏTİCƏLƏRİ ---\nİstifadəçinin sualı barədə internetdən tapılan məlumatlar:\n{live_internet_data}\nBu məlumatlara əsaslanıb səmimi cavab ver. Əsla fərqli mövzu uydurma!"

            messages = [{"role": "system", "content": final_prompt}] + st.session_state.messages

            try:
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model="llama-3.3-70b-versatile",
                    temperature=0.4, 
                    max_tokens=2048
                )
                response = chat_completion.choices[0].message.content
            except Exception as e:
                response = f"Xəta baş verdi: {str(e)}"

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
