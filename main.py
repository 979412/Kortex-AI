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
    
    /* QİYMƏT KARTLARI ÜÇÜN DİZAYN */
    .pricing-card {
        border: 2px solid #edf2f7; 
        border-radius: 15px; 
        padding: 30px; 
        text-align: center;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.3s;
    }
    .pricing-card:hover { transform: translateY(-5px); border-color: #1a73e8; }
    .tier-name { font-size: 24px; font-weight: bold; color: #202124; margin-bottom: 10px; }
    .tier-desc { font-size: 14px; color: #5f6368; height: 60px; }
    .tier-price { font-size: 36px; font-weight: bold; color: #1a73e8; margin: 20px 0; }
    .tier-price span { font-size: 18px; color: #5f6368; font-weight: normal; }
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
# 2. SİSTEM VƏZİYYƏTİ (STATE)
# ==========================================================
# Default olaraq hamı "Basic" paketində başlayır və Çat ekranını görür
if "selected_tier" not in st.session_state:
    st.session_state.selected_tier = "Basic"

if "show_pricing" not in st.session_state:
    st.session_state.show_pricing = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================================
# 3. QİYMƏT VƏ PAKET SEÇİMİ EKRANI (AÇILANDA)
# ==========================================================
if st.session_state.show_pricing:
    if st.button("⬅ Çata Qayıt", use_container_width=False):
        st.session_state.show_pricing = False
        st.rerun()

    st.markdown("<h1 style='text-align: center; color: #202124;'>Google Sİ-nin ən yaxşı üstünlükləri (Kortex AI)</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #5f6368; margin-bottom: 40px;'>Məhsuldarlıq və yaradıcılığınızı artırmaq üçün ehtiyacınıza uyğun paketi seçin.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="pricing-card">
            <div class="tier-name">Kortex AI Basic</div>
            <div class="tier-desc">Gündəlik suallar və sadə tapşırıqlar üçün pulsuz versiya.</div>
            <div class="tier-price">$0 <span>/ay</span></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Basic əldə edin", use_container_width=True, key="btn_basic"):
            st.session_state.selected_tier = "Basic"
            st.session_state.show_pricing = False
            st.rerun()

    with col2:
        st.markdown("""
        <div class="pricing-card">
            <div class="tier-name">Kortex AI Pro</div>
            <div class="tier-desc">Daha dəqiq cavablar və orta həcmli sənəd oxuma xüsusiyyəti.</div>
            <div class="tier-price">$12 <span>/ay</span></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Pro əldə edin", use_container_width=True, key="btn_pro"):
            st.session_state.selected_tier = "Pro"
            st.session_state.show_pricing = False
            st.rerun()

    with col3:
        st.markdown("""
        <div class="pricing-card">
            <div class="tier-name">Kortex AI Ultra</div>
            <div class="tier-desc">Maksimal limitlər, canlı internet axtarışı və böyük fayl analizi.</div>
            <div class="tier-price">$95 <span>/ay</span></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ultra əldə edin", use_container_width=True, key="btn_ultra"):
            st.session_state.selected_tier = "Ultra"
            st.session_state.show_pricing = False
            st.rerun()
            
    st.stop() # Qiymət ekranındayıqsa, aşağıdakı çatı göstərmə

# ==========================================================
# 4. ƏSAS ÇAT EKRANI (BİRBAŞA BURA AÇILIR)
# ==========================================================
# Yuxarı Başlıq və "Planı Dəyiş" düyməsi (Atdığın şəkil məntiqi)
header_col1, header_col2 = st.columns([4, 1])
with header_col1:
    st.title("🧠 Kortex AI")
    st.caption(f"Yaradıcı: Abdullah Mikayılov | Lisenziya: {st.session_state.selected_tier}")
with header_col2:
    st.write("") # Boşluq
    if st.button("✨ Planı Dəyiş", use_container_width=True):
        st.session_state.show_pricing = True
        st.rerun()

# ==========================================================
# YAN PANEL VƏ MƏNTİQ
# ==========================================================
st.sidebar.title("⚙️ Kortex Paneli")
st.sidebar.success(f"Aktiv Lisenziya: {st.session_state.selected_tier}")

st.sidebar.markdown("---")
st.sidebar.subheader("🌐 İnternet Axtarışı")
if st.session_state.selected_tier in ["Pro", "Ultra"]:
    use_internet = st.sidebar.checkbox("Canlı Axtarış Aktivdir", value=True)
else:
    st.sidebar.warning("🔒 İnternet axtarışı üçün Pro və ya Ultra lazımdır.")
    use_internet = False

st.sidebar.markdown("---")
st.sidebar.subheader("📁 Sənəd Yükləmə (PDF)")
uploaded_file = st.sidebar.file_uploader("Sənəd yükləyin", type=['pdf'])
document_text = ""

if uploaded_file is not None:
    # Limit yoxlaması
    if st.session_state.selected_tier == "Basic" and uploaded_file.size > 1000000:
        st.sidebar.error("❌ Basic paketdə böyük sənəd yükləmək olmur. ✨ Planı Dəyiş!")
    else:
        with st.spinner("Sənəd oxunur..."):
            try:
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        document_text += text + "\n"
                document_text = document_text[:25000] 
                st.sidebar.success("✅ Sənəd hazır!")
            except Exception as e:
                st.sidebar.error(f"Xəta: {e}")

# ==========================================================
# ALİM BEYNİ
# ==========================================================
if document_text:
    SYSTEM_PROMPT = f"Sən Kortex AI-san. Mətn budur: {document_text}. Buna əsasən cavab ver."
else:
    SYSTEM_PROMPT = "Sən Abdullah Mikayılov tərəfindən yaradılmış Kortex AI-san. Səmimi, dəqiq və dürüst ol. Heç nə uydurma."

# ==========================================================
# MESAJLAŞMA
# ==========================================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Kortex AI-a mesaj yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        live_internet_data = ""
        
        # Əgər Pro və ya Ultradısa internetdən tap
        if use_internet and st.session_state.selected_tier in ["Pro", "Ultra"]:
            with st.spinner("🌐 Kortex AI internetdə axtarır..."):
                try:
                    kw_chat = client.chat.completions.create(
                        messages=[{"role": "system", "content": "Axtarış sözü çıxar. Məsələn: 'boralonu taniyirsan' -> 'Boralo youtuber'"}, {"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                        temperature=0.0, max_tokens=15
                    )
                    search_query = kw_chat.choices[0].message.content.replace("'", "").replace('"', '').strip()
                    live_internet_data = search_internet(search_query)
                except:
                    pass
        
        with st.spinner("Kortex AI cavab yazır..."):
            final_prompt = SYSTEM_PROMPT
            if live_internet_data:
                final_prompt += f"\n\nCANLI İNTERNET MƏLUMATI:\n{live_internet_data}\nBuna əsaslanaraq cavab ver. Səhvdirsə uydurma."

            messages = [{"role": "system", "content": final_prompt}] + st.session_state.messages

            try:
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model="llama-3.3-70b-versatile",
                    temperature=0.3, max_tokens=2048
                )
                response = chat_completion.choices[0].message.content
            except Exception as e:
                response = f"Xəta: {str(e)}"

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
