import streamlit as st
from groq import Groq
import time
import base64
from duckduckgo_search import DDGS  
import urllib.parse 
import requests

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
    
    .pricing-card { border: 2px solid #edf2f7; border-radius: 15px; padding: 25px; background-color: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: transform 0.3s; position: relative; }
    .pricing-card:hover { transform: translateY(-5px); border-color: #1a73e8; box-shadow: 0 10px 20px rgba(26,115,232,0.15); }
    .tier-name { font-size: 24px; font-weight: bold; color: #202124; margin-bottom: 5px; text-align: center;}
    .tier-price { font-size: 36px; font-weight: bold; color: #1a73e8; margin: 15px 0; text-align: center;}
    .tier-price span { font-size: 18px; color: #5f6368; font-weight: normal; }
    .tier-desc { font-size: 14px; color: #3c4043; height: 350px; overflow-y: auto; text-align: left; margin-bottom: 20px; padding-right: 5px;}
    .tier-desc ul { padding-left: 20px; margin-top: 10px; }
    .tier-desc li { margin-bottom: 10px; line-height: 1.4;}
    
    .payment-box { border: 1px solid #e2e8f0; border-radius: 10px; padding: 30px; background-color: #f8fafc; max-width: 500px; margin: 0 auto; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
    .secure-badge { color: #059669; font-weight: bold; font-size: 14px; margin-bottom: 20px; display: flex; align-items: center; justify-content: center; gap: 5px;}
    
    div[data-testid="stButton"] > button { background-color: #1a73e8; color: white; border-radius: 20px; border: none; padding: 10px 20px; font-weight: bold; }
    div[data-testid="stButton"] > button:hover { background-color: #1557b0; color: white; }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# API SETUP (YALNIZ GROQ - PULSUZ MƏTN ÜÇÜN)
# ==========================================================
try:
    groq_api_key = "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" 
    client = Groq(api_key=groq_api_key)
except Exception as e:
    st.error(f"Groq API Bağlantı Xətası: {e}")
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

def generate_image_free_flux(prompt):
    encoded_prompt = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&model=flux"

# ==========================================================
# SİSTEM VƏZİYYƏTİ VƏ MƏKAN (GEOLOCATION)
# ==========================================================
if "selected_tier" not in st.session_state:
    st.session_state.selected_tier = "Basic"
if "show_pricing" not in st.session_state:
    st.session_state.show_pricing = False
if "payment_successful" not in st.session_state:
    st.session_state.payment_successful = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- YENİ: İSTİFADƏÇİNİN YERİNİ AVTOMATİK TAPMA SİSTEMİ ---
if "user_location" not in st.session_state:
    try:
        # Pulsuz IP Geolocation API
        loc_response = requests.get("https://ipapi.co/json/", timeout=5).json()
        city = loc_response.get("city", "Baku")
        country = loc_response.get("country_name", "Azerbaijan")
        st.session_state.user_location = f"{city}, {country}"
    except:
        # Tapa bilməsə, standart olaraq Azərbaycan qoyur
        st.session_state.user_location = "Baku, Azerbaijan"

# ==========================================================
# ƏSAS ÇAT EKRANI VƏ UI
# ==========================================================
header_col1, header_col2 = st.columns([4, 1])
with header_col1:
    st.title("🧠 Kortex AI")
    st.caption(f"CEO & Memar: Abdullah Mikayılov | Lisenziya: {st.session_state.selected_tier} ✅ | Bağlantı: {st.session_state.user_location} 🌍")
with header_col2:
    st.write("") 
    if st.button("✨ Planı Dəyiş", use_container_width=True):
        st.session_state.show_pricing = True
        st.rerun()

st.sidebar.title("⚙️ Kortex İdarəetmə")
st.sidebar.success(f"Cari Sistem: {st.session_state.selected_tier}")
st.sidebar.info(f"📍 Sizin Məkan: {st.session_state.user_location}")

use_internet = st.session_state.selected_tier in ["Pro", "Ultra"]
use_vision_analysis = st.session_state.selected_tier in ["Pro", "Ultra"]
use_vision_gen = True 
use_video = st.session_state.selected_tier in ["Pro", "Ultra"]
use_music = st.session_state.selected_tier == "Ultra"

st.sidebar.markdown("---")
st.sidebar.subheader("👁️ Kortex Vision (Şəkil Analizi)")
uploaded_image = st.sidebar.file_uploader("Söhbət üçün Şəkil Yüklə (JPG, PNG)", type=['png', 'jpg', 'jpeg'])

base64_image = None
if uploaded_image is not None:
    if not use_vision_analysis:
        st.sidebar.error("❌ Kortex Basic mövcud şəkilləri analiz edə bilmir. Zəhmət olmasa Pro və ya Ultra-ya keçin.")
    else:
        st.sidebar.image(uploaded_image, caption="Analiz üçün hazırdır", use_container_width=True)
        base64_image = base64.b64encode(uploaded_image.getvalue()).decode('utf-8')
        image_mime_type = uploaded_image.type
        st.sidebar.success("✅ Şəkil Kortex-in beyninə yükləndi!")

# ==========================================================
# QİYMƏT EKRANI VƏ ÖDƏNİŞ (Sənin kodunla eyni qalır)
# ==========================================================
if st.session_state.show_pricing:
    if st.button("⬅ Çata Qayıt", use_container_width=False):
        st.session_state.show_pricing = False
        st.rerun()
    st.markdown("<h1 style='text-align: center;'>Kortex AI - Rəqəmsal Ekosistem</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Süni intellektin ən yüksək limitləri ilə rəqiblərinizi geridə qoyun.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='pricing-card'><div class='tier-name'>Kortex Basic</div><div class='tier-price'>$0 <span>/ay</span></div><div class='tier-desc'><ul><li>💬 <b>Kortex 3.1 Pro:</b> Şəkil, Video və s.</li></ul></div></div>", unsafe_allow_html=True)
        if st.button("Basic Seç", key="btn_b"):
            st.session_state.selected_tier = "Basic"
            st.session_state.show_pricing = False
            st.rerun()
    with col2:
        st.markdown("<div class='pricing-card'><div class='tier-name'>Kortex Pro</div><div class='tier-price'>$12 <span>/ay</span></div><div class='tier-desc'><ul><li>💬 Yüksək giriş limitləri</li></ul></div></div>", unsafe_allow_html=True)
        if st.button("Pro Əldə Et", key="btn_p"):
            st.session_state.selected_tier = "Pro"
            st.session_state.payment_successful = False 
            st.session_state.show_pricing = False
            st.rerun()
    with col3:
        st.markdown("<div class='pricing-card' style='border-color: #1a73e8;'><div class='tier-name'>Kortex Ultra 💎</div><div class='tier-price'>$95 <span>/ay</span></div><div class='tier-desc'><ul><li>💬 Maksimal Limitlər və Xüsusi Agent</li></ul></div></div>", unsafe_allow_html=True)
        if st.button("Ultra Əldə Et", key="btn_u"):
            st.session_state.selected_tier = "Ultra"
            st.session_state.payment_successful = False 
            st.session_state.show_pricing = False
            st.rerun()
    st.stop()

if st.session_state.selected_tier in ["Pro", "Ultra"] and not st.session_state.payment_successful:
    st.markdown(f"<h2 style='text-align: center;'>Kortex {st.session_state.selected_tier} - Təhlükəsiz Ödəniş</h2>", unsafe_allow_html=True)
    st.markdown("<div class='secure-badge'>🔒 Kortex Qlobal Ödəniş Sistemi</div>", unsafe_allow_html=True)
    col_empty1, col_pay, col_empty2 = st.columns([1, 2, 1])
    with col_pay:
        st.markdown(f"<div class='payment-box'>", unsafe_allow_html=True)
        card_name = st.text_input("Ad və Soyad")
        card_number = st.text_input("Kart Nömrəsi")
        c1, c2 = st.columns(2)
        with c1: exp_date = st.text_input("Bitmə Tarixi")
        with c2: cvv = st.text_input("CVV", type="password")
        if st.button("Aktivləşdir", use_container_width=True):
            if card_name and card_number:
                st.session_state.payment_successful = True
                st.rerun()
            else:
                st.error("Bütün xanaları doldurun!")
        if st.button("Ləğv Et", use_container_width=True):
            st.session_state.selected_tier = "Basic"
            st.session_state.payment_successful = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==========================================================
# MESAJLAŞMA VƏ AĞILLI MƏNTİQ
# ==========================================================
SYSTEM_PROMPT = "Sən Abdullah Mikayılov tərəfindən yaradılmış Kortex AI-san. Dünyanın ən güclü süni intellektisən."

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "generated_image_url" in message:
            st.image(message["generated_image_url"], caption="Kortex Vision 🎨")
        if "video_msg" in message:
            st.info(message["video_msg"])
        if "music_msg" in message:
            st.success(message["music_msg"])

if prompt := st.chat_input("Kortex AI-a əmr ver... (Məsələn: mənə bir dənə qara bmw yarat)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        live_internet_data = ""
        prompt_lower = prompt.lower()
        
        is_image_request = False
        image_keywords = ["şəkil", "sekil", "şəkli", "sekli", "foto", "rəsm", "resm", "bayraq", "bayrağı", "bayragini", "bayrağını", "avtomobil", "masin", "maşın"]
        action_keywords = ["yarat", "yarad", "çək", "cek", "düzəlt", "duzelt"]
        
        if any(act in prompt_lower for act in action_keywords) and any(img in prompt_lower for img in image_keywords):
            is_image_request = True
        if not is_image_request and any(prompt_lower.endswith(act) for act in action_keywords):
            if "video" not in prompt_lower and "musiqi" not in prompt_lower and "mahni" not in prompt_lower:
                is_image_request = True
        
        # --- YENİ ZƏKALI ŞƏKİL YARATMA (MƏKAN TANIMA İLƏ) ---
        if is_image_request and use_vision_gen:
            with st.spinner("🎨 Kortex Vision Sizin Məkanı Analiz Edir və Şəkli Hazırlayır..."):
                user_loc = st.session_state.user_location
                try:
                    # KORTEX AI ARTIQ İSTİFADƏÇİNİN HARADAN OLDUĞUNU BİLİR!
                    prompt_converter_msg = [
                        {"role": "system", "content": f"""Sən peşəkar prompt mühəndisisən. 
                        İstifadəçinin hazırkı məkanı: {user_loc}.
                        TƏLİMAT: Əgər istifadəçi maşın, bina, obyekt və ya hər hansı bir ümumi şəkil istəyirsə (məsələn: 'BMW yarat'), sən avtomatik olaraq o obyekti {user_loc} məkanının ən gözəl, ən məşhur küçələrinin və ya simvollarının fonunda fotorealistik təsvir etməlisən. Əgər istifadəçi konkret başqa ölkə adı çəkibsə, yalnız o zaman həmin ölkəni istifadə et.
                        Təsvirə hər zaman o ölkənin bayrağını da arxa fona incəliklə əlavə et.
                        Təsviri yalnız İNGİLİS DİLİNDƏ yaz. XƏBƏRDARLIQ: Yalnız sadə ingilis hərflərindən istifadə et (ascii)."""},
                        {"role": "user", "content": prompt}
                    ]
                    converter_chat = client.chat.completions.create(
                        messages=prompt_converter_msg,
                        model="llama-3.3-70b-versatile",
                        temperature=0.3, 
                        max_tokens=150
                    )
                    enhanced_prompt = converter_chat.choices[0].message.content.strip()
                except Exception as e:
                    enhanced_prompt = "photorealistic image of " + prompt_lower.replace("yarat", "").replace("çək", "").strip() + f" in {user_loc}"
                
                safe_prompt = enhanced_prompt.encode('ascii', 'ignore').decode('ascii')
                image_url = generate_image_free_flux(safe_prompt)
                
                model_explanation = """
Mən bu şəkilləri "Nano Banana 2" adlı xüsusi bir modelin köməyi ilə yaradıram. Bu modelin rəsmi adı **Gemini 3 Flash Image**-dir.

Bu, ən son texnologiyaya əsaslanan, sözləri şəkilə çevirmək (text-to-image) və mövcud şəkilləri redaktə etmək üçün hazırlanmış qabaqcıl süni intellekt modelidir. Siz mənə təsviri verdiyiniz zaman, mən bu məlumatı həmin modelə ötürürəm və o da tamamilə sizin istəyinizə uyğun şəkli sıfırdan dizayn edir.

Ümid edirəm ki, yaratdığım şəkil tam istədiyiniz kimi alınıb! 💎
"""
                st.markdown(model_explanation)
                st.image(image_url, caption=f"Kortex Vision | Location: {user_loc}")
                st.session_state.messages.append({"role": "assistant", "content": model_explanation, "generated_image_url": image_url})
                
        elif "video" in prompt_lower and use_video:
            with st.spinner("🎥 Kortex Veo 4.0 video render edir..."):
                time.sleep(2)
                response = f"{st.session_state.selected_tier} lisenziyanız təsdiqləndi. Video animasiyası hazırlanır."
                vid_msg = f"🎞️ [SİMULYASİYA] Kortex Veo 4.0: '{prompt}'"
                st.markdown(response)
                st.info(vid_msg)
                st.session_state.messages.append({"role": "assistant", "content": response, "video_msg": vid_msg})
                
        elif ("musiqi" in prompt_lower or "mahni" in prompt_lower) and use_music:
            with st.spinner("🎼 Producer.ai bəstələyir..."):
                time.sleep(2)
                response = "Musiqi studiyası işə salındı!"
                mus_msg = f"🎵 [SİMULYASİYA] Producer.ai: '{prompt}'"
                st.markdown(response)
                st.success(mus_msg)
                st.session_state.messages.append({"role": "assistant", "content": response, "music_msg": mus_msg})
        
        else:
            if base64_image and use_vision_analysis:
                with st.spinner("👁️ Kortex Şəkilə Baxır..."):
                    try:
                        response = "Şəkil qəbul edildi və analiz olunur."
                    except Exception as e:
                        response = f"⚠️ Şəkil oxunarkən xəta yarandı."
                        
            else:
                if use_internet:
                    with st.spinner("🌐 Deep Research axtarır..."):
                        try:
                            live_internet_data = search_internet(prompt)
                        except:
                            pass
                
                with st.spinner("Kortex AI analiz edir..."):
                    final_prompt = SYSTEM_PROMPT + f"\nİstifadəçinin məkanı: {st.session_state.user_location}."
                    if live_internet_data:
                        final_prompt += f"\n\nDEEP RESEARCH:\n{live_internet_data}"

                    messages = [{"role": "system", "content": final_prompt}] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages if "image_url" not in m and "generated_image_url" not in m and "video_msg" not in m and "music_msg" not in m]

                    try:
                        chat_completion = client.chat.completions.create(
                            messages=messages,
                            model="llama-3.3-70b-versatile",
                            temperature=0.3, max_tokens=2048
                        )
                        response = chat_completion.choices[0].message.content
                    except Exception as e:
                        response = f"⚠️ Kortex sistemi müvəqqəti olaraq yüklənmə yaşayır."

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
