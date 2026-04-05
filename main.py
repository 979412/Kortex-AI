import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. ULTRA MİNİMALİST DİZAYN (TAM AĞ)
# ==========================================
st.set_page_config(page_title="ZƏKA ULTRA", layout="centered")

st.markdown("""
    <style>
    /* Tamamilə ağ və diqqət yayındırmayan interfeys */
    .stApp { background-color: #ffffff; color: #000000; font-family: 'Helvetica Neue', sans-serif; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Çat panellərinin xətlərini və rənglərini silirik */
    [data-testid="stChatMessage"] { background-color: #ffffff; border: none; padding: 20px 0; border-bottom: 1px solid #f0f0f0; }
    
    /* Giriş qutusunun dizaynı */
    .stChatInput { border-radius: 0px !important; border-top: 1px solid #dddddd !important; background-color: #ffffff !important;}
    
    /* Yükləmə (Düşünür...) yazısının rəngi */
    .stSpinner > div > div { border-color: #000000 transparent transparent transparent !important; }
    </style>
""", unsafe_allow_html=True)

# Başlıq (Minimal)
st.markdown("<h3 style='text-align:center; font-weight: 300; letter-spacing: 5px; margin-bottom: 50px; color: #333333;'>ZƏKA ULTRA</h3>", unsafe_allow_html=True)

# ==========================================
# 2. BEYİN: GEMINI PRO (Ən güclü versiya)
# ==========================================
# DİQQƏT: Streamlit Secrets-dən API açarını alır
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "SƏNİN_API_AÇARIN" # Öz açarını bura yaz (lokalda test edirsənsə)

genai.configure(api_key=API_KEY)

# Sistemin DNK-sı (Şəxsiyyət)
instruction = """
Sən ZƏKA ULTRA-san. Qlobal biznes sahibləri üçün elit, minimalist və dahi bir strateqsən.
Duyğulara yer yoxdur, yalnız sərt rəqəmlər, dərin analizlər və reallıq.
1. Əgər istifadəçi sadəcə "salam" (və ya bənzəri) yazarsa, ona belə cavab ver: "Salam, Memar. Sizi dinləyirəm. Hansı strateji məsələ üzərində işləyək?"
2. Digər bütün sorğularda lazımsız giriş sözləri olmadan, birbaşa və ən yüksək intellektual səviyyədə cavab ver.
3. Biznes qərarlarında həmişə rəqibləri, büdcə risklərini və ROI (İnvestisiya gəlirini) nəzərə alaraq analiz et.
"""

# Yaddaş və Modelin qurulması
if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest", # Ən güclü Pro model
        system_instruction=instruction
    )
    st.session_state.chat = st.session_state.model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# 3. İNTERFEYS VƏ MƏNTİQ
# ==========================================
# Söhbət tarixçəsini ekrana çap edirik
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image" in msg:
            st.image(msg["image"], width=400)

# Əmr gözləyirik (Mətn və ya Şəkil qəbul edir)
prompt = st.chat_input("Əmr et, Memar...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu məlumatı analiz et."
    
    # Sənin mesajın
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)
        
        # Əgər fayl/şəkil yükləmisənsə
        img_obj = None
        if prompt.files:
            img_obj = Image.open(prompt.files[0])
            st.image(img_obj, width=400)
            st.session_state.messages[-1]["image"] = img_obj

    # ZƏKA ULTRA CAVABI
    with st.chat_message("assistant"):
        with st.spinner("ZƏKA ULTRA DÜŞÜNÜR..."): # İstədiyin düşünmə effekti
            try:
                if img_obj:
                    # Şəkil və mətn analizi (Multimodal)
                    response = st.session_state.model.generate_content([user_text, img_obj])
                else:
                    # Təmiz mətn analizi (Yaddaşlı)
                    response = st.session_state.chat.send_message(user_text)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
            except Exception as e:
                st.error("Gözlənilməz dalğalanma. Zəhmət olmasa yenidən cəhd edin.")

# Səhifəni həmişə ən aşağıya sürüşdür
st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
