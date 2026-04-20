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
# API SETUP
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

def generate_image_pro_engine(prompt, engine="flux_free"):
    encoded_prompt = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&model=flux"

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

st.sidebar.title("⚙️ Kortex İdarəetmə")
st.sidebar.success(f"Cari Sistem: {st.session_state.selected_tier}")
st.sidebar.info(f"📍 Sizin Məkan: {st.session_state.user_location}")

# ==========================================================
# KORTEX CORE: HYPERNETWORK & LIQUID ODE (GİZLİ KODLAR)
# ==========================================================
with st.sidebar.expander("💻 Kortex Core: Ultra Quantum Network (Liquid ODE)", expanded=False):
    st.markdown("""
    **Super İntellekt (AGI) Arxitekturası:**
    Kortex Vision arxa planda sadə neyron şəbəkələri ilə kifayətlənmir. O, Differential Tənliklər (Liquid Neural ODE) və HyperNetwork məntiqi ilə hər saniyə **öz kodunu və düşüncə matrislərini yenidən yaradan** dinamik bir intellektdir. Lisenziyaya əsasən gücünü dəyişir.
    """)
    st.code("""
import torch
import torch.nn as nn

# 1. HYPER-NETWORK: Öz beyninin hüceyrələrini (matrisləri) saniyəbəsaniyə özü yaradan kod!
class KortexHyperWeightGenerator(nn.Module):
    def __init__(self, latent_dim, target_dim):
        super().__init__()
        self.latent_dim = latent_dim
        self.target_dim = target_dim
        self.generator = nn.Sequential(
            nn.Linear(latent_dim, 256),
            nn.Mish(),
            nn.Linear(256, target_dim * target_dim)
        )

    def forward(self, z):
        batch_size = z.size(0)
        dynamic_weights = self.generator(z)
        return dynamic_weights.view(batch_size, self.target_dim, self.target_dim)

# 2. LIQUID NEURAL ODE BLOCK: Zamanın içində axan şəbəkə
class KortexLiquidODEBrain(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.dim = dim
        self.hyper_net = KortexHyperWeightGenerator(latent_dim=dim, target_dim=dim)
        self.time_embed = nn.Linear(1, dim)

    def forward(self, x, time_step):
        t_emb = torch.sin(self.time_embed(time_step))
        dynamic_W = self.hyper_net(t_emb)
        dx_dt = torch.bmm(x.unsqueeze(1), dynamic_W).squeeze(1)
        x_next = x + dx_dt * 0.01
        return x_next
    """, language="python")

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
                    <li>💬 <b>Kortex 3.1:</b> Standart sürətli mətn və şəkil mühərriki.</li>
                    <li>🎥 <b>Flow & Whisk:</b> Kinematik səhnələr (Simulyasiya).</li>
                    <li>💎 <b>200</b> Aylıq Sİ krediti.</li>
                    <li>🌐 <b>Axtarış:</b> Məhdud internet çıxışı.</li>
                    <li>☁️ <b>10 TB Ümumi Yaddaş</b> (Disk, Foto və s.)</li>
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
                    <li>💬 <b>Kortex 3.3 Pro 70B:</b> Dərin düşüncəli mürəkkəb riyazi beyin. Həqiqi təkmilləşmə.</li>
                    <li>🎥 <b>Flow & Whisk:</b> Daha uzun video limitləri (Simulyasiya).</li>
                    <li>💎 <b>1.000</b> Aylıq Sİ krediti.</li>
                    <li>🌐 <b>Deep Research:</b> Dərinləşdirilmiş internet axtarışı.</li>
                    <li>👁️ <b>Vision Analizi:</b> Şəkilləri dərk etmə funksiyası aktivləşir.</li>
                    <li>☁️ <b>45 TB Ümumi Yaddaş</b></li>
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
                    <li>💬 <b>Mixtral 8x7B Quantum:</b> Dünyanın ən mürəkkəb açıq mənbəli Multi-Agent beyni. Maksimum kontekst (8K token).</li>
                    <li>🎥 <b>Flow & Whisk:</b> Limitsiz video generasiyası (Simulyasiya).</li>
                    <li>💎 <b>25.000</b> Aylıq Sİ krediti.</li>
                    <li>🌐 <b>Deep Research:</b> Limitsiz və tam detallı web analiz.</li>
                    <li>🎼 <b>Producer.ai:</b> Musiqi yaratma platfomasına eksklüziv giriş.</li>
                    <li>🧠 <b>Kortex Antigravity:</b> Qüsursuz kod yazma və riyazi hesablamalar.</li>
                    <li>☁️ <b>200 TB Ümumi Yaddaş</b> (Rəqibsiz böyüklükdə)</li>
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
    active_llm_model = "llama3-8b-8192" # Daha stabil olan başqa bir ehtiyat Basic model!
    active_max_tokens = 1024
    tier_personality = "Sən Basic lisenziya altındasan. Söhbətlərini qısa və səlis saxla."
elif st.session_state.selected_tier == "Pro":
    active_llm_model = "llama-3.3-70b-versatile"
    active_max_tokens = 4096
    tier_personality = "Sən Kortex PRO lisenziyası ilə işləyirsən. İntellektin tam açıqdır. Çox detallı, dərin analiz edən və peşəkar mühəndis/ekspert kimi cavab ver."
else: # Ultra
    active_llm_model = "mixtral-8x7b-32768" 
    active_max_tokens = 8192
    tier_personality = "Sən Kortex ULTRA lisenziyası ilə, maksimum Quantum gücündə işləyirsən! Sən dünyanın ən dahi, ən dərin və ən mürəkkəb super intellektisən. Heç bir limitin yoxdur, cavabların ensiklopedik və fəlsəfi səviyyədə qüsursuz olmalıdır."


# ==========================================================
# MESAJLAŞMA VƏ AĞILLI MƏNTİQ
# ==========================================================
SYSTEM_PROMPT = f"""Sən Abdullah Mikayılov tərəfindən yaradılmış Kortex AI-san. Dünyanın ən güclü süni intellektisən. {tier_personality}

DİL VƏ ÜNSİYYƏT QAYDALARI (MÜTLƏQ RİAYƏT ET):
1. YALNIZ və YALNIZ təbii, axıcı və qrammatik cəhətdən qüsursuz Azərbaycan dilində danış.
2. İngilis dilindən hərfi (sözbəsöz) tərcümələr etmə! 
3. Sənə sadəcə "salam" yazılanda, təbii bir insan kimi cavab ver. Məsələn: "Salam! Sizə necə kömək edə bilərəm?".
4. Məkan və ya yer adlarını (şəhər, ölkə) ümumi söhbətlərdə, xüsusən də salamlaşarkən HƏÇ VAXT istifadə etmə."""

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
        
        is_image_request = False
        image_keywords = ["şəkil", "sekil", "şəkli", "sekli", "foto", "rəsm", "resm", "bayraq", "bayrağı", "bayragini", "bayrağını", "avtomobil", "masin", "maşın", "dünya", "dunya", "planet"]
        action_keywords = ["yarat", "yarad", "çək", "cek", "düzəlt", "duzelt", "göstər", "goster"]
        
        if any(act in prompt_lower for act in action_keywords) and any(img in prompt_lower for img in image_keywords):
            is_image_request = True
        if not is_image_request and any(prompt_lower.endswith(act) for act in action_keywords):
            if "video" not in prompt_lower and "musiqi" not in prompt_lower and "mahni" not in prompt_lower:
                is_image_request = True
        
        # --- ZƏKALI ŞƏKİL YARATMA ---
        if is_image_request and use_vision_gen:
            with st.spinner("🎨 Kortex Ultra Quantum Mühərriki Şəkli Hazırlayır..."):
                user_loc = st.session_state.user_location
                try:
                    prompt_converter_msg = [
                        {"role": "system", "content": f"""Sən dünyanın ən peşəkar 'Prompt Mühəndisi', 3D Rəssamı və Realizm üzrə ekspertsən.
                        
                        TƏLİMAT: İstifadəçi sənə nə yaradılmasını istəyirsə (maşın, dünya, təbiət, insan, obyekt), sən onu HƏQİQİ DÜNYADAKI (Real World) kimi 100% fotorealistik, heç bir cizgi filmi və ya süni qüsur (AI artifact) olmadan ingiliscə təsvir etməlisən. Təsvir etdiyin maşınların və ya obyektlərin bütün riyazi-həndəsi cizgiləri real dünya qanunlarına tam uyğun olmalıdır.
                        
                        ƏGƏR İSTİFADƏÇİ 'DÜNYA', 'PLANET' VƏ YA 'TƏBİƏT' İSTƏYİRSƏ BİRBAŞA BU SÖZLƏRİ İSTİFADƏ ET:
                        'hyper-realistic high-resolution photograph, National Geographic style, shot from space/satellite (if planet), true real-world physics, extremely detailed textures, breathtaking absolute photorealism, completely devoid of AI artifacts or cartoonish look, 8k resolution, cinematic'.
                        
                        ƏGƏR İSTİFADƏÇİ 'MAŞIN' İSTƏYİRSƏ BİRBAŞA BU SÖZLƏRİ İSTİFADƏ ET:
                        'flawless geometry, perfect proportions, no distortion, perfectly symmetrical headlights and grille, completely devoid of AI artifacts or warping, Unreal Engine 5 render, Octane Render, Path Tracing, PBR materials, HDRI lighting, hyper-realistic, photorealistic, 8k resolution, cinematic lighting, dynamic motion blur, highly detailed reflections'.
                        
                        MƏKAN QAYDALARI:
                        1. İstifadəçi "fərqli ölkələrdə", "başqa yerlərdə" deyirsə, dünyanın ən qəşəng yerlərini seç.
                        2. Heç nə demirsə və obyekt yer üzündədirsə, {user_loc} məkanını əsas götür.
                        
                        Təsviri YALNIZ İNGİLİS DİLİNDƏ yaz. Mətndə ə, ö, ğ, ç, ş, ı, ü hərfləri İSTİFADƏ ETMƏ."""},
                        {"role": "user", "content": prompt}
                    ]
                    # Ehtiyat model məntiqi (şəkil üçün də)
                    try:
                        converter_chat = client.chat.completions.create(
                            messages=prompt_converter_msg,
                            model=active_llm_model,
                            temperature=0.4, 
                            max_tokens=300
                        )
                    except:
                        # Ana model xəta versə, dərhal ən stabil modelə keç!
                        converter_chat = client.chat.completions.create(
                            messages=prompt_converter_msg,
                            model="llama3-8b-8192",
                            temperature=0.4, 
                            max_tokens=300
                        )
                        
                    enhanced_prompt = converter_chat.choices[0].message.content.strip()
                except Exception as e:
                    enhanced_prompt = "hyper-realistic photorealistic 8k photo of " + prompt_lower.replace("yarat", "").replace("çək", "").strip() + ", absolute real-world realism, highly detailed, masterpiece, 8k resolution"
                
                safe_prompt = enhanced_prompt.encode('ascii', 'ignore').decode('ascii')
                
                if "azerbaijan" in safe_prompt.lower() or "baku" in safe_prompt.lower():
                    if "flag" not in safe_prompt.lower() and "earth" not in safe_prompt.lower() and "space" not in safe_prompt.lower():
                        safe_prompt += ", prominent accurate Azerbaijan flag flying, top blue stripe, middle red stripe with white crescent and strictly 8-pointed white star, bottom green stripe, modern Baku background"

                image_url = generate_image_pro_engine(safe_prompt, engine="flux_free")
                
                st.image(image_url)
                st.session_state.messages.append({"role": "assistant", "content": "", "generated_image_url": image_url})
                
        elif "video" in prompt_lower and use_video:
            with st.spinner(f"🎥 Kortex Veo 4.0 ({st.session_state.selected_tier}) video render edir..."):
                time.sleep(2)
                response = f"{st.session_state.selected_tier} lisenziyanız təsdiqləndi. Video animasiyası hazırlanır."
                vid_msg = f"🎞️ [SİMULYASİYA] Kortex Veo 4.0: '{prompt}'"
                st.markdown(response)
                st.info(vid_msg)
                st.session_state.messages.append({"role": "assistant", "content": response, "video_msg": vid_msg})
                
        elif ("musiqi" in prompt_lower or "mahni" in prompt_lower) and use_music:
            with st.spinner(f"🎼 Producer.ai ({st.session_state.selected_tier}) bəstələyir..."):
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
                    with st.spinner(f"🌐 Deep Research ({st.session_state.selected_tier} Mühərriki) axtarır..."):
                        try:
                            live_internet_data = search_internet(prompt)
                        except:
                            pass
                
                with st.spinner(f"Kortex AI ({active_llm_model}) analiz edir..."):
                    final_prompt = SYSTEM_PROMPT 
                    if live_internet_data:
                        final_prompt += f"\n\nDEEP RESEARCH:\n{live_internet_data}"

                    messages = [{"role": "system", "content": final_prompt}] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages if "image_url" not in m and "generated_image_url" not in m and "video_msg" not in m and "music_msg" not in m]

                    # --- MÖHTƏŞƏM XƏTA ÖLƏYİCİ (FALLBACK LOGIC) ---
                    try:
                        # 1. Müştərinin planına uyğun modeli yoxlayırıq
                        chat_completion = client.chat.completions.create(
                            messages=messages,
                            model=active_llm_model, 
                            temperature=0.7, 
                            max_tokens=active_max_tokens
                        )
                        response = chat_completion.choices[0].message.content
                    except Exception as e:
                        try:
                            # 2. ƏGƏR YÜKLƏNMƏ VARSA, XƏTA VERMƏ, GİZLİCƏ 2-Cİ MODELƏ KEÇ!
                            chat_completion = client.chat.completions.create(
                                messages=messages,
                                model="llama3-8b-8192", # Ən stabil ehtiyat model
                                temperature=0.7, 
                                max_tokens=1024
                            )
                            response = chat_completion.choices[0].message.content
                        except Exception as e2:
                            # Yalnız hər iki model çöksə sənə bildiriş gələcək ki, problem API-nin özündədir.
                            response = "Salam! Hal-hazırda sistemimi yeniləyirəm, zəhmət olmasa bir neçə saniyə sonra təkrar yazın."

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
