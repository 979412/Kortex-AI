import streamlit as st
from groq import Groq
import PyPDF2
import time
from duckduckgo_search import DDGS  

# ==========================================================
# 1. CSS VƏ VİZUAL AYARLAR
# ==========================================================
st.set_page_config(page_title="Kortex AI: Ultra", page_icon="🧠", layout="wide")

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
st.sidebar.title("⚙️ Kortex AI İdarə Paneli")

st.sidebar.markdown("---")
st.sidebar.subheader("🌐 Canlı İnternet")
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
# 3. ALİM BEYNİ (SƏRT ANTI-HALLÜSİNASİYA QAYDALARI)
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
    1. İNTERNET NƏTİCƏLƏRİNİ FİLTRLƏ: Sənə verilən internet nəticələri bəzən səhv ola bilər. Əgər istifadəçi bir adamı (məsələn, youtuberi, oyunçunu) soruşursa, amma internet sənə "mineral, bitki, maddə, xəstəlik" kimi aidiyyatı olmayan məlumat gətirirsə, o məlumatı rədd et!
    2. SIFIR UYDURMA: Əgər sən bir şeyi (və ya birini) tanımadınsa və ya internet səhv məlumat gətirdisə, dərhal etiraf et: "Mən bu barədə dəqiq məlumat tapa bilmədim." Heç vaxt, heç bir halda mövzunu başqa şeylərə bənzədib uydurma!
    3. HÖRMƏT: Cavabların səmimi, dürüst və çox ciddi (səviyyəli) olmalıdır. Heç kimə gülməli, uydurma, əlaqəsiz cavablar verib məni pis vəziyyətdə qoyma.
    """

# ==========================================================
# 4. İNTERFEYS VƏ ÇAT
# ==========================================================
st.title("🧠 Kortex AI: Qlobal İntellekt")
st.caption("Yaradıcı: Abdullah Mikayılov | Versiya: 9.1 (Kortex Rebrandinq + İki Mərhələli Agent)")

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
                            {"role": "system", "content": "Sən yalnız axtarış sözləri yazan robotsan. Cümlədən ən vacib sözləri və əsas kateqoriyanı tap. Məsələn: 'boralonu taniyirsan' -> 'Boralo youtuber'. 'nuraneni taniyirsan' -> 'Nurane adinda sexs'"},
                            {"role": "user", "content": prompt}
                        ],
                        model="llama-3.3-70b-versatile",
                        temperature=0.0, # SIFIR YARADICILIQ - Dəqiq olsun
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
                # Temperatur aşağı salındı ki, məntiqsiz hekayələr uydurmasın.
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
