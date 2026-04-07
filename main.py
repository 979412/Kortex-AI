import streamlit as st
from groq import Groq
import PyPDF2

# ==========================================================
# 1. CSS VƏ VİZUAL AYARLAR (VIP KORPORATİV DİZAYN)
# ==========================================================
st.set_page_config(page_title="Zəka AI: Enterprise", page_icon="💼", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; color: #0f172a; }
    .stChatMessage { border-radius: 8px; padding: 20px; border: 1px solid #e2e8f0; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
    [data-testid="stChatMessageUser"] { background-color: #ffffff; border-left: 4px solid #3b82f6; }
    [data-testid="stChatMessageAssistant"] { background-color: #f1f5f9; border-left: 4px solid #10b981; }
    .stSidebar { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
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
# 2. RAG MODULU: SƏNƏD YÜKLƏMƏ VƏ OXUMA PANelİ
# ==========================================================
st.sidebar.title("📁 Şirkət Məlumat Bazası")
st.sidebar.markdown("Sistemə daxili sənədləri (PDF) yükləyin. Zəka AI yalnız bu məlumatlara əsaslanacaq.")

uploaded_file = st.sidebar.file_uploader("Hesabat və ya Müqavilə yükləyin", type=['pdf'])
document_text = ""

if uploaded_file is not None:
    with st.spinner("Sənəd Zəka AI-ın beyninə inteqrasiya olunur..."):
        try:
            # PDF oxuyucu
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    document_text += text + "\n"
            
            # Mətni API limitlərinə uyğun olaraq kəsirik (maksimum ~20,000 simvol)
            document_text = document_text[:20000] 
            st.sidebar.success("✅ Sənəd uğurla oxundu və analizə hazırdır!")
            
            with st.sidebar.expander("Sənədin Önizləməsi"):
                st.caption(document_text[:500] + "...")
        except Exception as e:
            st.sidebar.error(f"Sənəd oxunarkən xəta: {e}")

# ==========================================================
# 3. KORPORATİV BEYİN (RAG PROMPTU)
# ==========================================================
# Əgər sənəd yüklənibsə, sistem tamamilə o sənədə fokuslanır.
if document_text:
    SYSTEM_PROMPT = f"""
    Sən Abdullah Mikayılov tərəfindən yaradılmış Korporativ Zəka AI-san.
    DİQQƏT: İstifadəçi şirkətə aid xüsusi sənəd yükləyib. Sənədin mətni budur:
    
    --- SƏNƏDİN BAŞLANĞICI ---
    {document_text}
    --- SƏNƏDİN SONU ---
    
    QAYDALAR:
    1. Yalnız yuxarıdakı sənədə əsaslanaraq suallara cavab ver.
    2. Əgər istifadəçinin sualının cavabı sənəddə YOXDURSA, qətiyyən uydurma və "Bu məlumat yüklədiyiniz sənəddə mövcud deyil" de.
    3. Cavablarını maddələr halında, qısa və peşəkar Maliyyə Direktoru (CFO) və ya Baş Hüquqşünas tonunda ver.
    """
else:
    SYSTEM_PROMPT = """
    Sən Abdullah Mikayılov tərəfindən yaradılmış Zəka AI-san. 
    İstifadəçi hələ şirkət sənədi yükləməyib. Qlobal biznes, iqtisadiyyat və strategiya üzrə peşəkar, sərt və dəqiq analizlər ver.
    """

# ==========================================================
# 4. İNTERFEYS VƏ ÇAT
# ==========================================================
st.title("💼 Zəka AI: Enterprise RAG")
st.caption("Yaradıcı: Abdullah Mikayılov | Versiya: 8.0 (Sənəd Analizi İnteqrasiya Edilib)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Sənədlə bağlı sualınızı və ya strategiyanızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Zəka AI sənədləri təhlil edir..."):
            model = "llama-3.3-70b-versatile"
            messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages

            try:
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model=model,
                    temperature=0.1, 
                    max_tokens=2048
                )
                response = chat_completion.choices[0].message.content
            except Exception as e:
                response = f"Xəta baş verdi: {str(e)}"

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
