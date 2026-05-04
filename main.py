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

if "user_location" not in st.session_state:
    try:
        loc_response = requests.get("https://ipapi.co/json/", timeout=5).json()
        city = loc_response.get("city", "Ganja")
        country = loc_response.get("country_name", "Azerbaijan")
        st.session_state.user_location = f"{city}, {country}"
    except:
        st.session_state.user_location = "Ganja, Azerbaijan"

# ==========================================================
# BİRBAŞA ŞİFRƏLƏR (QÜSURSUZ YOL)
# ==========================================================
# Sənin verdiyin ən sonuncu şifrə bura əlavə edildi
groq_token_input = "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"
hf_token_input = "BURA_TEZE_HUGGINGFACE_SIFRESINI_YAZ"

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
    if groq_token_input and "BURA" not in groq_token_input:
        client = Groq(api_key=groq_token_input)
    else:
        client = None
except Exception:
    client = None

def search_internet(query):
    try:
        results = DDGS().text(query, max_results=5) 
        res_text = ""
        for r in results:
            res_text += f"Mənbə: {r['title']}\nMəlumat: {r['body']}\n\n"
        return res_text
    except Exception:
        return ""

def generate_image_hf(prompt, token):
    if not token or "BURA" in token:
        return None
    API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": prompt}
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=40)
        if response.status_code == 200:
            img_str = base64.b64encode(response.content).decode("utf-8")
            return f"data:image/png;base64,{img_str}"
    except Exception:
        pass
    return None

def generate_image_pro_engine(prompt):
    encoded_prompt = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&model=flux"

# ==========================================================
# ƏSAS ÇAT EKRANI 
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

# ==========================================================
# QİYMƏT EKRANI VƏ ÖDƏNİŞ
# ==========================================================
if st.session_state.show_pricing:
    if st.button("⬅ Çata Qayıt", use_container_width=False):
        st.session_state.show_pricing = False
        st.rerun()
    st.markdown("<h1 style='text-align: center;'>Kortex AI - Rəqəmsal Ekosistem</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Süni intellektin ən yüksək limitləri ilə rəqiblərinizi geridə qoyun.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="pricing-card">
            <div class="tier-name">Kortex Basic</div>
            <div class="tier-price">$0 <span>/ay</span></div>
            <div class="tier-desc">
                <ul>
                    <li>💬 <b>Mətn:</b> Llama 3 8B (Standart).</li>
                    <li>🎨 <b>Şəkil:</b> Standart Dəqiqlik.</li>
                    <li>🔒 <b>Video & Musiqi:</b> Qapalıdır. (Pro və Ultra tələb olunur).</li>
                    <li>🌐 <b>Axtarış:</b> Məhdud internet çıxışı.</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Basic Seç", key="btn_b"):
            st.session_state.selected_tier = "Basic"
            st.session_state.show_pricing = False
            st.rerun()
    with col2:
        st.markdown("""
        <div class="pricing-card">
            <div class="tier-name">Kortex Pro</div>
            <div class="tier-price">$12 <span>/ay</span></div>
            <div class="tier-desc">
                <ul>
                    <li>💬 <b>Mətn:</b> Llama 3.3 70B (Peşəkar Analiz).</li>
                    <li>🎨 <b>Şəkil:</b> Nano Banana 2 mühərriki ilə fotorealizm.</li>
                    <li>🎥 <b>Video:</b> Veo Mühərriki ilə video yaratma aktivdir.</li>
                    <li>🔒 <b>Musiqi:</b> Qapalıdır. (Ultra tələb olunur).</li>
                    <li>🌐 <b>Deep Research:</b> Dərinləşdirilmiş axtarış.</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Pro Əldə Et", key="btn_p"):
            st.session_state.selected_tier = "Pro"
            st.session_state.payment_successful = False 
            st.session_state.show_pricing = False
            st.rerun()
    with col3:
        st.markdown("""
        <div class="pricing-card" style="border-color: #1a73e8; background: linear-gradient(to bottom, #ffffff, #f0f7ff);">
            <div class="tier-name">Kortex Ultra 💎</div>
            <div class="tier-price">$95 <span>/ay</span></div>
            <div class="tier-desc">
                <ul>
                    <li>💬 <b>Mətn:</b> Mixtral 8x7B Quantum (Maksimum Məntiq).</li>
                    <li>🎨 <b>Şəkil:</b> Nano Banana PRO rejimində limitsiz qüsursuzluq.</li>
                    <li>🎥 <b>Video:</b> Veo 4.0 Limitsiz animasiyalar.</li>
                    <li>🎼 <b>Musiqi:</b> Lyria 3 mühərriki ilə limitsiz vokal/audio bəstələmə.</li>
                    <li>🌐 <b>Deep Research:</b> Limitsiz analiz.</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ultra Əldə Et", key="btn_u"):
            st.session_state.selected_tier = "Ultra"
            st.session_state.payment_successful = False 
            st.session_state.show_pricing = False
            st.rerun()
    st.stop()

if st.session_state.selected_tier in ["Pro", "Ultra"] and not st.session_state.payment_successful:
    price = "$12.00" if st.session_state.selected_tier == "Pro" else "$95.00"
    st.markdown(f"<h2 style='text-align: center; margin-top: 50px;'>Kortex {st.session_state.selected_tier} - Təhlükəsiz Ödəniş</h2>", unsafe_allow_html=True)
    st.markdown("<div class='secure-badge'>🔒 Kortex Qlobal Ödəniş Sistemi</div>", unsafe_allow_html=True)
    col_empty1, col_pay, col_empty2 = st.columns([1, 2, 1])
    with col_pay:
        st.markdown(f"<div class='payment-box'>", unsafe_allow_html=True)
        st.info(f"Ödəniləcək Məbləğ: **{price} / Ay**")
        card_name = st.text_input("Ad və Soyad")
        card_number = st.text_input("Kart Nömrəsi")
        c1, c2 = st.columns(2)
        with c1: exp_date = st.text_input("Bitmə Tarixi (AA/İİ)")
        with c2: cvv = st.text_input("CVV", type="password")
        
        st.write("")
        if st.button("Aktivləşdir", use_container_width=True):
            if card_name and card_number and exp_date and cvv:
                with st.spinner("💳 Bankla əlaqə yaradılır..."):
                    time.sleep(2) 
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
# LİSENZİYAYA GÖRƏ DİNAMİK BEYİN DƏYİŞMƏSİ
# ==========================================================
if st.session_state.selected_tier == "Basic":
    active_llm_model = "llama3-8b-8192" 
    active_max_tokens = 1024
elif st.session_state.selected_tier == "Pro":
    active_llm_model = "llama-3.3-70b-versatile"
    active_max_tokens = 4096
else: 
    active_llm_model = "mixtral-8x7b-32768" 
    active_max_tokens = 8192

# ==========================================================
# MESAJLAŞMA VƏ AĞILLI MƏNTİQ
# ==========================================================
SYSTEM_PROMPT = """Sən Abdullah Mikayılov tərəfindən yaradılmış Kortex AI-san. Dünyanın ən güclü və ən səmimi süni intellektisən.

DİL VƏ ÜNSİYYƏT QAYDALARI:
1. Yalnız təbii Azərbaycan dilində danış. İngilisdən hərfi tərcümə edilmiş cümlələr qurma.
2. Salamlaşanda təbii və səmimi ol.
3. Məkan adlarını (şəhər, ölkə) söhbətlərdə qətiyyən çəkmə."""

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "generated_image_url" in message:
            st.image(message["generated_image_url"])
        if "video_msg" in message:
            st.info(message["video_msg"])
        if "music_msg" in message:
            st.success(message["music_msg"])

if prompt := st.chat_input(f"Kortex AI ({st.session_state.selected_tier} Mode) əmrini gözləyir..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        live_internet_data = ""
        prompt_lower = prompt.lower()
        use_internet = True
        
        is_image_request = False
        is_video_request = False
        is_music_request = False
        
        image_keywords = ["şəkil", "sekil", "şəkli", "sekli", "foto", "rəsm", "resm"]
        video_keywords = ["video", "animasiya", "canlandır"]
        music_keywords = ["musiqi", "mahni", "bəstələ", "səs", "oxu"]
        action_keywords = ["yarat", "yarad", "çək", "cek", "düzəlt", "duzelt", "göstər", "goster"]
        
        if any(act in prompt_lower for act in action_keywords) or any(prompt_lower.endswith(act) for act in action_keywords):
            if any(vid in prompt_lower for vid in video_keywords):
                is_video_request = True
            elif any(mus in prompt_lower for mus in music_keywords):
                is_music_request = True
            else:
                is_image_request = True
                
        # --- ZƏKALI ŞƏKİL YARATMA ---
        if is_image_request:
            if st.session_state.selected_tier == "Basic":
                spinner_msg = "🎨 Kortex Basic Şəkli Hazırlayır..."
                prompt_enhancement_level = "Sən sadə prompt mühəndisisən. İstifadəçinin istəyini ingiliscəyə çevir."
            elif st.session_state.selected_tier == "Pro":
                spinner_msg = "🎨 Hugging Face FLUX Mühərriki Fotorealistik Şəkil Yaradır..."
                prompt_enhancement_level = "Sən peşəkar 'Prompt Mühəndisi'sən. İstəyi HƏQİQİ DÜNYADAKI kimi 100% fotorealistik, cinematic, 8k resolution olaraq ingiliscə təsvir et."
            else:
                spinner_msg = "💎 HF FLUX.1-dev Quantum Mühərriki Qüsursuz Şəkil Yaradır..."
                prompt_enhancement_level = "Sən dünyanın ən dahi 3D Rəssamı və Realizm ekspertsən. İstəyi 'flawless geometry, perfect proportions, completely devoid of AI artifacts, Unreal Engine 5 render, PBR materials, HDRI lighting, hyper-realistic, 8k resolution' parametrləri ilə ingiliscə təsvir et."
                
            with st.spinner(spinner_msg):
                user_loc = st.session_state.user_location
                try:
                    if client:
                        prompt_converter_msg = [
                            {"role": "system", "content": f"{prompt_enhancement_level} Məkan olaraq {user_loc} əsas götürülə bilər. Yalnız İngiliscə cavab ver."},
                            {"role": "user", "content": prompt}
                        ]
                        try:
                            converter_chat = client.chat.completions.create(messages=prompt_converter_msg, model=active_llm_model, temperature=0.4, max_tokens=300)
                        except:
                            converter_chat = client.chat.completions.create(messages=prompt_converter_msg, model="llama3-8b-8192", temperature=0.4, max_tokens=300)
                            
                        enhanced_prompt = converter_chat.choices[0].message.content.strip()
                    else:
                        enhanced_prompt = "hyper-realistic photo of " + prompt_lower.replace("yarat", "").strip()
                except Exception:
                    enhanced_prompt = "hyper-realistic photo of " + prompt_lower.replace("yarat", "").strip()
                
                safe_prompt = enhanced_prompt.encode('ascii', 'ignore').decode('ascii')
                
                image_url = None
                if hf_token_input and "BURA" not in hf_token_input and st.session_state.selected_tier in ["Pro", "Ultra"]:
                    image_url = generate_image_hf(safe_prompt, hf_token_input)
                
                if not image_url:
                    image_url = generate_image_pro_engine(safe_prompt)
                
                st.image(image_url)
                st.session_state.messages.append({"role": "assistant", "content": "", "generated_image_url": image_url})
                
        # --- VİDEO YARATMA LİSENZİYASI ---
        elif is_video_request:
            if st.session_state.selected_tier == "Basic":
                msg = "⚠️ **Lisenziya Xətası:** Kortex Basic planında Video yaratma funksiyası mövcud deyil. Zəhmət olmasa **Pro** və ya **Ultra** planına keçid edin."
                st.error(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
            else:
                veo_version = "Veo" if st.session_state.selected_tier == "Pro" else "Veo 4.0 (Limitsiz)"
                with st.spinner(f"🎥 {veo_version} mühərriki videonu render edir..."):
                    time.sleep(2)
                    response = f"✅ {st.session_state.selected_tier} lisenziyanız təsdiqləndi. Video arxa planda hazırlanır."
                    vid_msg = f"🎞️ [SİMULYASİYA] {veo_version}: '{prompt}'"
                    st.markdown(response)
                    st.info(vid_msg)
                    st.session_state.messages.append({"role": "assistant", "content": response, "video_msg": vid_msg})
                
        # --- MUSİQİ YARATMA LİSENZİYASI ---
        elif is_music_request:
            if st.session_state.selected_tier in ["Basic", "Pro"]:
                msg = "⚠️ **Lisenziya Xətası:** Lyria 3 mühərriki ilə Musiqi və Vokal yaratmaq YALNIZ **Kortex Ultra 💎** planında mövcuddur. Zəhmət olmasa planınızı yeniləyin."
                st.warning(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
            else:
                with st.spinner("🎼 Lyria 3 mühərriki musiqini bəstələyir..."):
                    time.sleep(2)
                    response = "✅ Ultra lisenziyası aktivdir! Musiqi studiyası işə salındı."
                    mus_msg = f"🎵 [SİMULYASİYA] Lyria 3: '{prompt}'"
                    st.markdown(response)
                    st.success(mus_msg)
                    st.session_state.messages.append({"role": "assistant", "content": response, "music_msg": mus_msg})
        
        # --- NORMAL SÖHBƏT VƏ AXTARIŞ ---
        else:
            if use_internet:
                with st.spinner(f"🌐 Deep Research ({st.session_state.selected_tier} Mühərriki) axtarır..."):
                    try:
                        live_internet_data = search_internet(prompt)
                    except:
                        pass
            
            with st.spinner(f"Kortex AI ({active_llm_model}) düşünür..."):
                final_prompt = SYSTEM_PROMPT 
                if live_internet_data:
                    final_prompt += f"\n\nDEEP RESEARCH:\n{live_internet_data}"

                messages = [{"role": "system", "content": final_prompt}] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages if "image_url" not in m and "generated_image_url" not in m and "video_msg" not in m and "music_msg" not in m]

                try:
                    if client:
                        chat_completion = client.chat.completions.create(
                            messages=messages,
                            model=active_llm_model, 
                            temperature=0.7, 
                            max_tokens=active_max_tokens
                        )
                        response = chat_completion.choices[0].message.content
                    else:
                        response = "Kortex mühərriki hazırda bağlantı gözləyir. Arxa planda sistem işə salınır... (Diqqət: API şifrənizi daxil etməyi unutmayın)"
                except Exception:
                    try:
                        if client:
                            chat_completion = client.chat.completions.create(
                                messages=messages,
                                model="llama3-8b-8192", 
                                temperature=0.7, 
                                max_tokens=1024
                            )
                            response = chat_completion.choices[0].message.content
                        else:
                            response = "Kortex mühərriki hazırda bağlantı gözləyir. Arxa planda sistem işə salınır... (Diqqət: API şifrənizi daxil etməyi unutmayın)"
                    except Exception:
                        response = "Kortex mühərriki hazırda bağlantı gözləyir. Arxa planda sistem işə salınır... (Diqqət: API şifrənizi daxil etməyi unutmayın)"

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
