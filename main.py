import streamlit as st
from groq import Groq
import time
import base64
from duckduckgo_search import DDGS
import urllib.parse
import requests

# ==========================================================
# 1. CSS VƏ VİZUAL AYARLAR (TAM TƏMİZ)
# ==========================================================
st.set_page_config(page_title="Kortex AI", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1b1e; }
    .stChatMessage { border-radius: 20px; padding: 20px; border: 1px solid #edf2f7; }
    [data-testid="stChatMessageUser"] { background-color: #f7fafc; }
    [data-testid="stChatMessageAssistant"] { background-color: #ebf8ff; }
    
    .pricing-card { border: 2px solid #edf2f7; border-radius: 15px; padding: 25px; background-color: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: transform 0.3s; position: relative; }
    .pricing-card:hover { transform: translateY(-5px); border-color: #1a73e8; box-shadow: 0 10px 20px rgba(26,115,232,0.15); }
    .tier-name { font-size: 24px; font-weight: bold; color: #202124; margin-bottom: 5px; text-align: center;}
    .tier-price { font-size: 36px; font-weight: bold; color: #1a73e8; margin: 15px 0; text-align: center;}
    .tier-price span { font-size: 18px; color: #5f6368; font-weight: normal; }
    .tier-desc { font-size: 14px; color: #3c4043; height: 350px; overflow-y: auto; text-align: left; margin-bottom: 20px; padding-right: 5px;}
    .tier-desc ul { padding-left: 20px; margin-top: 10px; }
    .tier-desc li { margin-bottom: 10px; line-height: 1.4;}
    
    .tier-desc::-webkit-scrollbar { width: 5px; }
    .tier-desc::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 5px; }
    
    .payment-box { border: 1px solid #e2e8f0; border-radius: 10px; padding: 30px; background-color: #f8fafc; max-width: 500px; margin: 0 auto; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
    .secure-badge { color: #059669; font-weight: bold; font-size: 14px; margin-bottom: 20px; display: flex; align-items: center; justify-content: center; gap: 5px;}
    
    div[data-testid="stButton"] > button { background-color: #1a73e8; color: white; border-radius: 20px; border: none; padding: 10px 20px; font-weight: bold; }
    div[data-testid="stButton"] > button:hover { background-color: #1557b0; color: white; }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# SİSTEM VƏ MƏKAN
# ==========================================================
if "selected_tier" not in st.session_state:
    st.session_state.selected_tier = "Basic"
if "show_pricing" not in st.session_state:
    st.session_state.show_pricing = False
if "payment_successful" not in st.session_state:
    st.session_state.payment_successful = False
if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    loc_response = requests.get("https://ipapi.co/json/", timeout=5).json()
    st.session_state.user_location = f"{loc_response.get('city', 'Baku')}, {loc_response.get('country_name', 'Azerbaijan')}"
except:
    st.session_state.user_location = "Baku, Azerbaijan"

# ==========================================================
# BİRBAŞA ŞİFRƏ YERLƏŞDİRMƏ (QÜSURSUZ MƏNTİQ)
# ==========================================================
# Təzə aldığın şifrələri bura dırnaqların içinə yaz. Kod heç bir xəta verməyəcək.

KORTEX_GROQ_API_KEY = "BURA_TEZE_GROQ_SIFRESINI_YAZ"
KORTEX_HF_API_KEY = "BURA_TEZE_HUGGINGFACE_SIFRESINI_YAZ"

# ==========================================================
# YAN PANEL (YALNIZ MƏLUMAT)
# ==========================================================
st.sidebar.title("⚙️ Kortex İdarəetmə")
st.sidebar.success(f"Cari Sistem: {st.session_state.selected_tier}")
st.sidebar.info(f"📍 Sizin Məkan: {st.session_state.user_location}")
st.sidebar.markdown("---")
st.sidebar.caption("Kortex AI rəsmi versiyası. Bütün sistemlər aktivdir.")

# ==========================================================
# API SETUP
# ==========================================================
try:
    client = Groq(api_key=KORTEX_GROQ_API_KEY)
except:
    client = None

def search_internet(query):
    try:
        results = DDGS().text(query, max_results=3) 
        return "".join([f"Mənbə: {r['title']}\nMəlumat: {r['body']}\n\n" for r in results])
    except: return ""

def generate_image_hf(prompt, token):
    if not token or token == "BURA_TEZE_HUGGINGFACE_SIFRESINI_YAZ": return None
    try:
        res = requests.post("https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev", 
                            headers={"Authorization": f"Bearer {token}"}, json={"inputs": prompt}, timeout=40)
        if res.status_code == 200:
            return f"data:image/png;base64,{base64.b64encode(res.content).decode('utf-8')}"
    except: pass
    return None

def generate_image_pro_engine(prompt):
    return f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1280&height=720&nologo=true&model=flux"

# ==========================================================
# ƏSAS ÇAT EKRANI 
# ==========================================================
header_col1, header_col2 = st.columns([4, 1])
with header_col1:
    st.title("🧠 Kortex AI")
    st.caption(f"CEO & Memar: Abdullah Mikayılov | Lisenziya: {st.session_state.selected_tier} ✅")
with header_col2:
    st.write("") 
    if st.button("✨ Planı Dəyiş", use_container_width=True):
        st.session_state.show_pricing = True
        st.rerun()

# ==========================================================
# QİYMƏT EKRANI VƏ ÖDƏNİŞ
# ==========================================================
if st.session_state.show_pricing:
    if st.button("⬅ Çata Qayıt", use_container_width=False):
        st.session_state.show_pricing = False
        st.rerun()
    st.markdown("<h1 style='text-align: center;'>Kortex AI - Rəqəmsal Ekosistem</h1>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="pricing-card"><div class="tier-name">Basic</div><div class="tier-price">$0</div></div>""", unsafe_allow_html=True)
        if st.button("Basic Seç"): st.session_state.selected_tier = "Basic"; st.session_state.show_pricing = False; st.rerun()
    with c2:
        st.markdown("""<div class="pricing-card"><div class="tier-name">Pro</div><div class="tier-price">$12</div></div>""", unsafe_allow_html=True)
        if st.button("Pro Əldə Et"): st.session_state.selected_tier = "Pro"; st.session_state.payment_successful = False; st.session_state.show_pricing = False; st.rerun()
    with c3:
        st.markdown("""<div class="pricing-card" style="border-color:#1a73e8;"><div class="tier-name">Ultra 💎</div><div class="tier-price">$95</div></div>""", unsafe_allow_html=True)
        if st.button("Ultra Əldə Et"): st.session_state.selected_tier = "Ultra"; st.session_state.payment_successful = False; st.session_state.show_pricing = False; st.rerun()
    st.stop()

if st.session_state.selected_tier in ["Pro", "Ultra"] and not st.session_state.payment_successful:
    st.markdown(f"<h2 style='text-align: center; margin-top: 50px;'>Kortex {st.session_state.selected_tier} - Təhlükəsiz Ödəniş</h2>", unsafe_allow_html=True)
    c1, c_pay, c2 = st.columns([1, 2, 1])
    with c_pay:
        st.markdown("<div class='payment-box'>", unsafe_allow_html=True)
        st.text_input("Kart Nömrəsi")
        if st.button("Aktivləşdir", use_container_width=True):
            with st.spinner("💳 İşlənir..."):
                time.sleep(1) 
                st.session_state.payment_successful = True
                st.rerun()
        if st.button("Ləğv Et", use_container_width=True):
            st.session_state.selected_tier = "Basic"
            st.session_state.payment_successful = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==========================================================
# DİNAMİK BEYİN
# ==========================================================
tier_settings = {
    "Basic": ("llama3-8b-8192", 1024),
    "Pro": ("llama-3.3-70b-versatile", 4096),
    "Ultra": ("mixtral-8x7b-32768", 8192)
}
active_llm_model, active_max_tokens = tier_settings[st.session_state.selected_tier]

SYSTEM_PROMPT = "Sən Kortex AI-san. Dünyanın ən güclü süni intellektisən. Yaradıcın Abdullah Mikayılovdur. Azərbaycan dilində təbii cavab ver."

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "img" in msg: st.image(msg["img"])
        if "vid" in msg: st.info(msg["vid"])
        if "mus" in msg: st.success(msg["mus"])

if prompt := st.chat_input("Kortex AI əmrini gözləyir..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        p_low = prompt.lower()
        is_img = any(w in p_low for w in ["şəkil", "sekil", "foto", "rəsm", "yarat"])
        is_vid = any(w in p_low for w in ["video", "animasiya", "canlandır"])
        is_mus = any(w in p_low for w in ["musiqi", "mahni", "bəstələ"])
        
        if is_img and not is_vid and not is_mus:
            with st.spinner("🎨 Kortex şəkli hazırlayır..."):
                img_url = generate_image_hf(prompt, KORTEX_HF_API_KEY)
                if not img_url: img_url = generate_image_pro_engine(prompt)
                st.image(img_url)
                st.session_state.messages.append({"role": "assistant", "content": "Görüntü hazırdır!", "img": img_url})
                
        elif is_vid:
            if st.session_state.selected_tier == "Basic":
                st.markdown("Kortex Video mühərriki aktiv deyil. Lütfən Pro və ya Ultra planına keçin.")
                st.session_state.messages.append({"role": "assistant", "content": "Kortex Video mühərriki aktiv deyil. Lütfən Pro və ya Ultra planına keçin."})
            else:
                with st.spinner("🎥 Video render edilir..."):
                    time.sleep(2)
                    st.markdown("Video arxa planda hazırlanır.")
                    st.info(f"🎞️ [SİMULYASİYA] Veo: '{prompt}'")
                    st.session_state.messages.append({"role": "assistant", "content": "Video arxa planda hazırlanır.", "vid": f"🎞️ [SİMULYASİYA] Veo: '{prompt}'"})
                    
        elif is_mus:
            if st.session_state.selected_tier in ["Basic", "Pro"]:
                st.markdown("Musiqi studiyası yalnız Ultra planında aktivdir.")
                st.session_state.messages.append({"role": "assistant", "content": "Musiqi studiyası yalnız Ultra planında aktivdir."})
            else:
                with st.spinner("🎼 Musiqi bəstələnir..."):
                    time.sleep(2)
                    st.markdown("Musiqi hazırdır.")
                    st.success(f"🎵 [SİMULYASİYA] Lyria 3: '{prompt}'")
                    st.session_state.messages.append({"role": "assistant", "content": "Musiqi hazırdır.", "mus": f"🎵 [SİMULYASİYA] Lyria 3: '{prompt}'"})
                    
        else:
            with st.spinner("🧠 Kortex düşünür..."):
                internet_data = search_internet(prompt)
                final_prompt = SYSTEM_PROMPT + (f"\nİNTERNET: {internet_data}" if internet_data else "")
                msgs = [{"role": "system", "content": final_prompt}] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages if "img" not in m and "vid" not in m and "mus" not in m]
                
                try:
                    chat_completion = client.chat.completions.create(messages=msgs, model=active_llm_model, temperature=0.7, max_tokens=active_max_tokens)
                    resp = chat_completion.choices[0].message.content
                except:
                    resp = "Kortex mühərriki hazırda bağlantı gözləyir. Arxa planda sistem işə salınır..."
                    
                st.markdown(resp)
                st.session_state.messages.append({"role": "assistant", "content": resp})
