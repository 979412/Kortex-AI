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
    
    /* GİRİŞ EKRANI VƏ QİYMƏT KARTLARI ÜÇÜN DİZAYN */
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
    
    /* MAVİ DÜYMƏLƏR */
    div[data-testid="stButton"] > button {
        background-color: #1a73e8;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    div[data-testid="stButton"] > button:hover {
        background-color: #1557b0;
        color: white;
    }
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
# 2. QİYMƏT CƏDVƏLİ VƏ GİRİŞ EKRANI
# ==========================================================
if "selected_tier" not in st.session_state:
    st.session_state.selected_tier = None

if st.session_state.selected_tier is None:
    st.markdown("<h1 style='text-align: center; color: #202124;'>Kortex AI Plans & Pricing</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #5f6368; margin-bottom: 40px;'>Choose the perfect Kortex AI plan for your productivity and creativity needs.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # KORTEX AI BASIC (SADƏ)
    with col1:
        st.markdown("""
        <div class="pricing-card">
            <div class="tier-name">Kortex AI Basic</div>
            <div class="tier-desc">Essential AI features for everyday tasks and simple queries.</div>
            <div class="tier-price">$0 <span>/month</span></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Get Kortex Basic", use_container_width=True, key="btn_basic"):
            st.session_state.selected_tier = "Basic"
            st.rerun()

    # KORTEX AI PRO
    with col2:
        st.markdown("""
        <div class="pricing-card">
            <div class="tier-name">Kortex AI Pro</div>
            <div class="tier-desc">Advanced performance, live internet access, and document analysis.</div>
            <div class="tier-price">$TBD <span>/month</span></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Get Kortex Pro", use_container_width=True, key="btn_pro"):
            st.session_state.selected_tier = "Pro"
            st.rerun()

    # KORTEX AI ULTRA
    with col3:
        st.markdown("""
        <div class="pricing-card">
            <div class="tier-name">Kortex AI Ultra</div>
            <div class="tier-desc">Maximum limits, autonomous agents, and exclusive premium features.</div>
            <div class="tier-price">$TBD <span>/month</span></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Get Kortex Ultra", use_container_width=True, key="btn_ultra"):
            st.session_state.selected_tier = "Ultra"
            st.rerun()
            
    st.stop() # İstifadəçi paket seçməyənə qədər aşağıdakı çat kodunu işə salmır

# ==========================================================
# 3. YAN PANEL (MƏLUMAT BAZASI VƏ İNTERNET)
# ==========================================================
st.sidebar.title("⚙️ Kortex AI Paneli")
st.sidebar.success(f"💎 Aktiv Paket: {st.session_state.selected_tier}")

st.sidebar.markdown("---")
st.sidebar.subheader("🌐 Canlı İnternet")
# Basic paketdə internet bağlı ola bilər, amma hələlik sən istədiyin kimi açıq qoyuram
use_internet = st.sidebar.checkbox("Ağıllı Axtarış Agentini Aktivləşdir", value=True)

st.sidebar.markdown("---")
st.sidebar.subheader("📁 Şirkət / Məlumat Bazası (PDF)")
uploaded_file = st.sidebar.file_uploader("Sənəd yükləyin", type=['pdf'])
document_text = ""

if uploaded_file is not None:
    with st.spinner("Sənəd Kortex AI-ın beyninə inteqrasiya olunur..."):
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
# 4. ALİM BEYNİ (SƏRT ANTI-HALLÜSİNASİYA QAYDALARI)
# ==========================================================
if document_text:
    SYSTEM_PROMPT = f"""
    Sən Abdullah Mikayılov tərəfindən yaradılmış Kortex AI-san. 
    İstifadəçi sənəd yükləyib. Mətn budur: {document_text}
    QAYDALAR: Yalnız bu sənədə əsaslanaraq səmimi cavab ver.
    """
else:
    SYSTEM_PROMPT = """
    Sən Abdullah Mikayılov tərəfindən yaradılmış Kortex AI-san. Dünyanın ən güclü, səmimi Azərbaycanlı süni intellektisən.
    DİQQƏT: Sənin üçün cari il 2026-cı ildir. Sən canlı internet məlumatları ilə qidalanırsan.

    ŞƏXSİYYƏTİN VƏ SƏRT QAYDALARIN:
    1. İNTERNET NƏTİCƏLƏRİNİ FİLTRLƏ: Sənə verilən internet nəticələri bəzən səhv ola bilər. Əgər istifadəçi bir adamı soruşursa, amma internet sənə fərqli məlumat gətirirsə, onu rədd et!
    2. SIFIR UYDURMA: Əgər məlumat yoxdursa dərhal etiraf et: "Mən bu barədə dəqiq məlumat tapa bilmədim." Mövzunu uydurma!
    3. HÖRMƏT: Cavabların səmimi, dürüst və çox ciddi olmalıdır.
    """

# ÇIXIŞ DÜYMƏSİ (SƏHİFƏYƏ QAYITMAQ ÜÇÜN)
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Paket Seçiminə Qayıt", use_container_width=True):
    st.session_state.selected_tier = None
    st.rerun()

# ==========================================================
# 5. İNTERFEYS VƏ ÇAT
# ==========================================================
st.title("🧠 Kortex AI: Qlobal İntellekt")
st.caption(f"Yaradıcı: Abdullah Mikayılov | Lisenziya: Kortex {st.session_state.selected_tier}")

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
        
        # --- İKİ MƏRHƏLƏLİ AĞILLI AXTARIŞ ---
        live_internet_data = ""
        if use_internet:
            with st.spinner("🧠 Kortex AI axtarış üçün açar sözləri düşünür..."):
                try:
                    kw_chat = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Sən yalnız axtarış sözləri yazan robotsan. Cümlədən ən vacib sözləri tap. Nümunə: 'boralonu taniyirsan' -> 'Boralo youtuber'."},
                            {"role": "user", "content": prompt}
                        ],
                        model="llama-3.3-70b-versatile",
                        temperature=0.0, 
                        max_tokens=15
                    )
                    search_query = kw_chat.choices[0].message.content.replace("'", "").replace('"', '').strip()
                except:
                    search_query = prompt

            with st.spinner(f"🌐 İnternetdə axtarılır: '{search_query}' ..."):
                live_internet_data = search_internet(search_query)
        
        # --- YEKUN CAVABIN HAZIRLANMASI ---
        with st.spinner("Kortex AI cavab hazırlayır..."):
            final_prompt = SYSTEM_PROMPT
            if live_internet_data:
                final_prompt += f"\n\n--- DİQQƏT: CANLI İNTERNET NƏTİCƏLƏRİ ---\nİnternetdən tapılan məlumatlar:\n{live_internet_data}\n\nƏgər bu nəticələr istifadəçinin sualı ilə MƏNTİQƏN tamamilə əlaqəsizdirsə, onlara əhəmiyyət vermə və dürüstcə 'Məlumatım yoxdur' de."

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
