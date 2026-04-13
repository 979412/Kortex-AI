import streamlit as st
from groq import Groq
import time
import base64
from duckduckgo_search import DDGS  
import urllib.parse 

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
# 2. SİSTEM VƏZİYYƏTİ (STATE)
# ==========================================================
if "selected_tier" not in st.session_state:
    st.session_state.selected_tier = "Basic"
if "show_pricing" not in st.session_state:
    st.session_state.show_pricing = False
if "payment_successful" not in st.session_state:
    st.session_state.payment_successful = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================================
# 3. QİYMƏT VƏ PAKET SEÇİMİ EKRANI
# ==========================================================
if st.session_state.show_pricing:
    if st.button("⬅ Çata Qayıt", use_container_width=False):
        st.session_state.show_pricing = False
        st.rerun()

    st.markdown("<h1 style='text-align: center; color: #202124;'>Kortex AI - Rəqəmsal Ekosistem</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #5f6368; margin-bottom: 40px;'>Süni intellektin ən yüksək limitləri ilə rəqiblərinizi geridə qoyun.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="pricing-card">
            <div class="tier-name">Kortex Basic</div>
            <div class="tier-price">$0 <span>/ay</span></div>
            <div class="tier-desc">
                <ul>
                    <li>💬 <b>Kortex 3.1 Pro:</b> Deep Research və limitsiz şəkil mühərriki.</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Basic Seç", use_container_width=True, key="btn_basic"):
            st.session_state.selected_tier = "Basic"
            st.session_state.payment_successful = True
            st.session_state.show_pricing = False
            st.rerun()

    with col2:
        st.markdown("""
        <div class="pricing-card">
            <div class="tier-name">Kortex Pro</div>
            <div class="tier-price">$12 <span>/ay</span></div>
            <div class="tier-desc">
                <ul>
                    <li>💬 <b>Kortex 3.1 Pro:</b> Şəkil, video və Deep Research funksiyalarına yüksək giriş.</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Pro Əldə Et", use_container_width=True, key="btn_pro"):
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
                    <li>💬 <b>Maksimal Limitlər:</b> Limitsiz video, musiqi və Sİ krediti.</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ultra Əldə Et", use_container_width=True, key="btn_ultra"):
            st.session_state.selected_tier = "Ultra"
            st.session_state.payment_successful = False 
            st.session_state.show_pricing = False
            st.rerun()
            
    st.stop()

# ==========================================================
# 4. ÖDƏNİŞ (CHECKOUT) EKRANI
# ==========================================================
if st.session_state.selected_tier in ["Pro", "Ultra"] and not st.session_state.payment_successful:
    price = "$12.00" if st.session_state.selected_tier == "Pro" else "$95.00"
    st.markdown(f"<h2 style='text-align: center; margin-top: 50px;'>Kortex {st.session_state.selected_tier} - Təhlükəsiz Ödəniş</h2>", unsafe_allow_html=True)
    st.markdown("<div class='secure-badge'>🔒 Kortex Qlobal Ödəniş Sistemi</div>", unsafe_allow_html=True)
    
    col_empty1, col_pay, col_empty2 = st.columns([1, 2, 1])
    with col_pay:
        st.markdown(f"<div class='payment-box'>", unsafe_allow_html=True)
        st.info(f"Ödəniləcək Məbləğ: **{price} / Ay**")
        card_name = st.text_input("Kartın üzərində Ad və Soyad", placeholder="Abdullah Mikayılov")
        card_number = st.text_input("Kartın Nömrəsi (16 rəqəm)", placeholder="XXXX XXXX XXXX XXXX", max_chars=19)
        c1, c2 = st.columns(2)
        with c1: exp_date = st.text_input("Bitmə Tarixi (AA/İİ)", placeholder="12/26", max_chars=5)
        with c2: cvv = st.text_input("CVV", placeholder="123", max_chars=3, type="password")
            
        st.write("")
        if st.button(f"Pulu Çıx və {st.session_state.selected_tier} Aktivləşdir", use_container_width=True):
            if card_name and card_number and exp_date and cvv:
                with st.spinner("💳 Bankla əlaqə yaradılır..."):
                    time.sleep(2) 
                    st.session_state.payment_successful = True
                    st.rerun()
            else:
                st.error("Bütün xanaları doldurun!")
        if st.button("Ləğv Et və Pulsuz Rejimə Qayıt", use_container_width=True):
            st.session_state.selected_tier = "Basic"
            st.session_state.payment_successful = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop() 

# ==========================================================
# YAN PANEL (API AÇARI VƏ AYARLAR)
# ==========================================================
st.sidebar.title("⚙️ Kortex İdarəetmə")
st.sidebar.success(f"Cari Sistem: {st.session_state.selected_tier}")

st.sidebar.markdown("---")
st.sidebar.subheader("🔑 Kortex Beyin Açarı")
st.sidebar.caption("Əgər sistem 'salam'a cavab vermirsə, bura yeni Groq API açarını yapışdırın:")
# İSTİFADƏÇİ BURADAN AÇARI YAZA BİLƏR:
user_api_key = st.sidebar.text_input("Groq API Key:", type="password", value="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")

client = None
if user_api_key:
    try:
        client = Groq(api_key=user_api_key)
    except Exception:
        pass

def search_internet(query):
    try:
        results = DDGS().text(query, max_results=5) 
        res_text = ""
        for r in results:
            res_text += f"Mənbə: {r['title']}\nMəlumat: {r['body']}\n\n"
        return res_text
    except Exception as e:
        return ""

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
        st.sidebar.error("❌ Kortex Basic mövcud şəkilləri analiz edə bilmir. Pro/Ultra lazımdır.")
    else:
        st.sidebar.image(uploaded_image, caption="Analiz üçün hazırdır", use_container_width=True)
        base64_image = base64.b64encode(uploaded_image.getvalue()).decode('utf-8')
        image_mime_type = uploaded_image.type
        st.sidebar.success("✅ Şəkil Kortex-in beyninə yükləndi!")

# ==========================================================
# 5. ƏSAS ÇAT EKRANI 
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

if prompt := st.chat_input("Kortex AI-a əmr ver... (Məsələn: qara bmw m3 yarat, qırmızı faralarla)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        live_internet_data = ""
        prompt_lower = prompt.lower()
        
        # ==========================================================
        # SUPER AĞILLI DETEKTOR (XƏTA YOXDUR!)
        # ==========================================================
        is_image_request = False
        if any(x in prompt_lower for x in ["yarat", "yarad", "çək", "cek", "düzəlt", "duzelt"]):
            if any(y in prompt_lower for y in ["şəkil", "sekil", "şəkli", "sekli", "foto", "rəsm", "resm"]):
                is_image_request = True
                
        if "sekli yarat" in prompt_lower or "şəkli yarat" in prompt_lower or "sekil cek" in prompt_lower or "şəkil çək" in prompt_lower:
            is_image_request = True
            
        if prompt_lower.endswith("yarat") or prompt_lower.endswith("çək") or prompt_lower.endswith("duzelt"):
             is_image_request = True
        
        # --- ŞƏKİL YARATMA LOQİKASI (LIMITSIZ VƏ XƏTASIZ) ---
        if is_image_request and use_vision_gen:
            with st.spinner(f"🎨 Kortex Vision Realistik Detalları Oxuyur..."):
                
                clean_prompt = ""
                # Əgər API açarı işləyirsə Tərcüməçini istifadə et
                if client:
                    try:
                        prompt_converter_msg = [
                            {"role": "system", "content": "Sən yalnız gerçək və fotorealistik şəkillər yaradan Prompt Mühəndisisən. İstifadəçinin cümləsindən əsas obyekti və detalları tap, və İngilis dilinə çevir. MÜTLƏQ HƏMİŞƏ BU SÖZLƏRİ ƏLAVƏ ET: ', hyper-realistic, photorealistic, professional automotive photography, 8k resolution, NO neon'. Yalnız bu hazır İngilis dili promptunu yaz."},
                            {"role": "user", "content": prompt}
                        ]
                        converter_chat = client.chat.completions.create(
                            messages=prompt_converter_msg,
                            model="llama-3.3-70b-versatile",
                            temperature=0.1, 
                            max_tokens=70
                        )
                        clean_prompt = converter_chat.choices[0].message.content.strip()
                    except Exception:
                        pass
                
                # Əgər API xarabdırsa, Kortex çökmür! Şəkli birbaşa bu üsulla yaradır:
                if not clean_prompt:
                    clean_prompt = prompt_lower.replace("şəkil", "").replace("sekil", "").replace("şəkli", "").replace("yarat", "").replace("olsun", "").replace("bele", "").replace("mene", "").strip()
                    clean_prompt += ", highly detailed photorealistic car photography, natural lighting, 8k, no neon"
                    
                encoded_prompt = urllib.parse.quote(clean_prompt)
                seed_value = int(time.time()) 
                image_api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&realism=true&model=flux&seed={seed_value}"
                
                response_text = f"Buyur, istədiyin təsvir hazırdır! (4K Fotorealistik Mühərrik)"
                st.markdown(response_text)
                st.image(image_api_url, caption=f"Kortex Vision: Limitsiz Generasiya")
                st.session_state.messages.append({"role": "assistant", "content": response_text, "generated_image_url": image_api_url})
                
        # --- DİGƏR FUNKSİYALAR (VİDEO/MUSİQİ) ---
        elif "video" in prompt_lower and use_video:
            with st.spinner("🎥 Kortex Veo 4.0 video render edir..."):
                time.sleep(2)
                response = f"{st.session_state.selected_tier} lisenziyanız təsdiqləndi. Video animasiyası hazırlanır."
                vid_msg = f"🎞️ [SİMULYASİYA] Kortex Veo 4.0: '{prompt}'"
                st.markdown(response)
                st.info(vid_msg)
                st.session_state.messages.append({"role": "assistant", "content": response, "video_msg": vid_msg})
                
        elif "musiqi" in prompt_lower and use_music:
            with st.spinner("🎼 Producer.ai bəstələyir..."):
                time.sleep(2)
                response = "Musiqi studiyası işə salındı!"
                mus_msg = f"🎵 [SİMULYASİYA] Producer.ai: '{prompt}'"
                st.markdown(response)
                st.success(mus_msg)
                st.session_state.messages.append({"role": "assistant", "content": response, "music_msg": mus_msg})
        
        # --- NORMAL MƏTN ÇAT VƏ XƏTALARIN İDARƏ EDİLMƏSİ ---
        else:
            if not client:
                # XƏTA MESAJI YOXDUR! SƏLİQƏLİ İZAHAT VAR:
                response = "⚠️ **Məlumat:** Kortex-in mətn (söhbət) mühərrikinə gedən API açarının vaxtı bitib. Zəhmət olmasa yan paneldən (solda) yeni açar daxil edin. **Amma narahat olmayın, mən yenə də sizin üçün şəkil yarada bilərəm! Sadəcə '... şəkli yarat' yazın.**"
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                with st.spinner("Kortex AI analiz edir..."):
                    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages if "image_url" not in m and "generated_image_url" not in m and "video_msg" not in m and "music_msg" not in m]

                    try:
                        chat_completion = client.chat.completions.create(
                            messages=messages,
                            model="llama-3.3-70b-versatile",
                            temperature=0.3, max_tokens=2048
                        )
                        response = chat_completion.choices[0].message.content
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        # API VAR AMMA LİMİT BİTİB VƏ YA XARABDIR
                        response = "⚠️ **Məlumat:** Kortex-in mətn (söhbət) mühərrikinə gedən API açarının vaxtı bitib. Zəhmət olmasa yan paneldən (solda) yeni açar daxil edin. **Amma narahat olmayın, mən yenə də sizin üçün şəkil yarada bilərəm! Sadəcə '... şəkli yarat' yazın.**"
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
