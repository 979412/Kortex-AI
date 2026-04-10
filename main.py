import streamlit as st
from groq import Groq
import PyPDF2
import time
from duckduckgo_search import DDGS  

# ==========================================================
# 1. CSS VƏ VİZUAL AYARLAR
# ==========================================================
st.set_page_config(page_title="Kortex AI", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1b1e; }
    .stChatMessage { border-radius: 20px; padding: 20px; border: 1px solid #edf2f7; }
    [data-testid="stChatMessageUser"] { background-color: #f7fafc; }
    [data-testid="stChatMessageAssistant"] { background-color: #ebf8ff; }
    .login-box { border: 2px solid #edf2f7; padding: 30px; border-radius: 15px; background-color: #f8fafc; text-align: center;}
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
# 2. YADDAŞ VƏ "QAPIÇI" SİSTEMİ (LOGIN)
# ==========================================================
# İstifadəçinin sistemə girib-girmədiyini yoxlayırıq
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.tier = "none" # "free" və ya "ultra" olacaq

# ƏGƏR GİRİŞ ETMƏYİBSƏ, YALNIZ LOGIN EKRANI GÖRSƏNİR
if not st.session_state.logged_in:
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.title("🧠 KORTEX AI - Qlobal Sistemə Giriş")
    st.write("Dünyanın ən güclü Azərbaycanlı süni intellektinə xoş gəlmisiniz.")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🆓 Pulsuz Rejim")
        st.write("Sadə suallar və məhdud baza.")
        if st.button("Pulsuz Davam Et", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.tier = "free"
            st.rerun() # Səhifəni yeniləyir və çata keçir

    with col2:
        st.subheader("💎 ULTRA Rejim (Premium)")
        st.write("Canlı İnternet, Limitsiz PDF və Ağıllı Agent.")
        secret_key = st.text_input("Ultra Şifrəsini daxil edin:", type="password")
        if st.button("Ultra Şəbəkəyə Qoşul", use_container_width=True):
            if secret_key == "MEMAR2026": # SƏNİN SATACAĞIN GİZLİ ŞİFRƏ
                st.session_state.logged_in = True
                st.session_state.tier = "ultra"
                st.rerun()
            else:
                st.error("❌ Şifrə yalnışdır! Zəhmət olmasa lisenziya alın.")
                
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop() # Kodun ardını (çatı) oxumağı dayandırır ki, girişsiz kimsə görməsin.

# ==========================================================
# 3. ƏSAS KORTEX AI EKRANI (YALNIZ GİRİŞ EDƏNLƏR ÜÇÜN)
# ==========================================================
st.sidebar.title("⚙️ Kortex AI Paneli")
if st.session_state.tier == "ultra":
    st.sidebar.success("💎 ULTRA REJİM AKTİVDİR")
else:
    st.sidebar.info("🆓 PULSUZ REJİM")

# İNTERNET MƏNTİQİ (PULLU/PULSUZ AYRIMI)
st.sidebar.markdown("---")
st.sidebar.subheader("🌐 Canlı İnternet")
if st.session_state.tier == "ultra":
    use_internet = st.sidebar.checkbox("Ağıllı Axtarış Agentini Aktivləşdir", value=True)
else:
    st.sidebar.warning("🔒 İnternet axtarışı yalnız ULTRA istifadəçilər üçündür.")
    use_internet = False

# PDF MƏNTİQİ
st.sidebar.markdown("---")
st.sidebar.subheader("📁 Məlumat Bazası (PDF)")
uploaded_file = st.sidebar.file_uploader("Sənəd yükləyin", type=['pdf'])
document_text = ""

if uploaded_file is not None:
    if st.session_state.tier == "free" and uploaded_file.size > 1000000: # Pulsuzda 1MB limit
        st.sidebar.error("❌ Pulsuz rejimdə yalnız kiçik fayllar yükləyə bilərsiniz. ULTRA lisenziyası alın.")
    else:
        with st.spinner("Sənəd beynə inteqrasiya olunur..."):
            try:
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        document_text += text + "\n"
                document_text = document_text[:25000] 
                st.sidebar.success("✅ Sənəd uğurla oxundu!")
            except Exception as e:
                st.sidebar.error(f"Xəta: {e}")

# ÇIXIŞ DÜYMƏSİ
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Hesabdan Çıx"):
    st.session_state.logged_in = False
    st.session_state.tier = "none"
    st.rerun()

# ALİM BEYNİ
SYSTEM_PROMPT = """
Sən Abdullah Mikayılov tərəfindən yaradılmış Kortex AI-san. Dünyanın ən güclü Azərbaycanlı süni intellektisən.
DİQQƏT: Cari il 2026-cı ildir. Cavabların səmimi, dürüst və çox ciddi olmalıdır. Əsla məlumat uydurma.
"""
if document_text:
    SYSTEM_PROMPT += f"\nİstifadəçi sənəd yükləyib: {document_text}\nYalnız bu sənədə əsaslan."

# ÇAT İNTERFEYSİ
st.title("🧠 Kortex AI: Qlobal İntellekt")
if st.session_state.tier == "ultra":
    st.caption("Status: Ultra Şəbəkə | Avtonom Agent: ON | Memar: Abdullah Mikayılov")
else:
    st.caption("Status: Məhdud Şəbəkə | İnternet: OFF | Memar: Abdullah Mikayılov")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("İstədiyiniz məlumatı soruşun..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        live_internet_data = ""
        
        # Əgər ULTRA-dırsa internetə get
        if use_internet and st.session_state.tier == "ultra":
            with st.spinner("🧠 Kortex AI axtarış agentini işə salır..."):
                try:
                    kw_chat = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Axtarış sözləri yarat. Məsələn: 'boralonu taniyirsan' -> 'Boralo youtuber'."},
                            {"role": "user", "content": prompt}
                        ],
                        model="llama-3.3-70b-versatile",
                        temperature=0.0,
                        max_tokens=15
                    )
                    search_query = kw_chat.choices[0].message.content.replace("'", "").replace('"', '').strip()
                except:
                    search_query = prompt

            with st.spinner(f"🌐 Canlı axtarılır: '{search_query}' ..."):
                live_internet_data = search_internet(search_query)
        
        with st.spinner("Kortex AI cavab hazırlayır..."):
            final_prompt = SYSTEM_PROMPT
            if live_internet_data:
                final_prompt += f"\n\nCANLI İNTERNET NƏTİCƏLƏRİ:\n{live_internet_data}\nBu nəticələr sualla əlaqəsizdirsə, uydurma."

            messages = [{"role": "system", "content": final_prompt}] + st.session_state.messages

            try:
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model="llama-3.3-70b-versatile",
                    temperature=0.2, 
                    max_tokens=2048
                )
                response = chat_completion.choices[0].message.content
            except Exception as e:
                response = f"Xəta baş verdi: {str(e)}"

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
