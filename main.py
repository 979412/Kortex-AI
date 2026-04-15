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
# API SETUP (YALNIZ GROQ - PULSUZ MƏTN ÜÇÜN)
# ==========================================================
try:
    groq_api_key = "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" 
    client = Groq(api_key=groq_api_key)
except Exception as e:
    st.error(f"Groq API Bağlantı Xətası: {e}")
    st.stop()

# --- BAYRAQ MƏLUMAT BAZASI ---
FLAGS = {
    "azerbaijan": {
        "colors": "blue (sky blue), red, green horizontal stripes",
        "symbol": "white crescent and exactly eight-pointed (8-pointed) star on the red stripe",
        "location": "Baku, Azerbaijan (Heydar Aliyev Center, Flag Square, clear blue sky)"
    },
    "turkey": {
        "colors": "red background",
        "symbol": "white crescent and star",
        "location": "Istanbul, Turkey (Hagia Sophia or Blue Mosque, cinematic lighting)"
    }
}

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
    """
    Heç bir API açarı tələb etməyən, tam pulsuz və xətasız Flux modeli.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    # nologo=true Pollinations loqosunu silir
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&model=flux"

# ==========================================================
# SİSTEM VƏZİYYƏTİ (STATE)
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
                    <li>💬 <b>Kortex 3.1 Pro:</b> Deep Research, Nano Banana Pro ilə şəkil və Veo 3.1 ilə video yaratmaya təkmilləşdirilmiş giriş.</li>
                    <li>🎥 <b>Flow & Whisk:</b> Kinematik səhnələr və şəkildən video yaratma alətləri.</li>
                    <li>💎 <b>200</b> Aylıq Sİ krediti.</li>
                    <li>🌐 <b>Axtarış & NotebookLM:</b> Audio/Video icmallar və testlərə əlavə giriş.</li>
                    <li>🎼 <b>Producer.ai:</b> Musiqi yaratma platformamıza giriş.</li>
                    <li>📧 <b>Kortex Tətbiqləri:</b> Gmail, Calendar və Meet üçün birbaşa giriş.</li>
                    <li>☁️ <b>10 TB Ümumi Yaddaş</b> (Disk, Foto və s.)</li>
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
                    <li>💬 <b>Kortex 3.1 Pro:</b> Şəkil, video və Deep Research funksiyalarına daha yüksək giriş əldə edin.</li>
                    <li>🎥 <b>Flow & Whisk:</b> Kinematik video alətimizə və şəkildən videoya yüksək giriş.</li>
                    <li>💎 <b>1.000</b> Aylıq Sİ krediti.</li>
                    <li>🌐 <b>Axtarış & NotebookLM:</b> Tədqiqat partnyorumuza yüksək giriş.</li>
                    <li>🎼 <b>Producer.ai:</b> Musiqi platformasına yüksək giriş.</li>
                    <li>🧠 <b>Kortex Antigravity:</b> Agent inkişaf platforması üçün daha yüksək sorğu limitləri.</li>
                    <li>💻 <b>Developer Program & Studio:</b> Sİ kod agentləri ilə Android inkişafınızı sürətləndirin.</li>
                    <li>☁️ <b>45 TB Ümumi Yaddaş</b></li>
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
                    <li>💬 <b>Maksimal Limitlər:</b> Deep Think, Nano Banana Pro və ən son Veo 3.1 video mühərriki.</li>
                    <li>🎥 <b>Flow & Whisk:</b> Hekayə və kinematik səhnələr üçün maksimal limitlər.</li>
                    <li>💎 <b>25.000</b> Aylıq Sİ krediti.</li>
                    <li>🌐 <b>Axtarış & NotebookLM:</b> Maksimal və limitsiz giriş.</li>
                    <li>🎼 <b>Producer.ai:</b> Birgə musiqi platformasına maksimal giriş.</li>
                    <li>🧠 <b>Kortex Antigravity:</b> Agent modeli üçün maksimal limitlər.</li>
                    <li>💻 <b>Developer Program & Studio:</b> CLI, Code Assist və bulud limitləri maksimal sürətdə.</li>
                    <li>🚫 <b>Premium Əlavə:</b> Reklamsız, oflayn media (YouTube ekvivalenti).</li>
                    <li>☁️ <b>200 TB Ümumi Yaddaş</b> (Rəqibsiz böyüklükdə)</li>
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
# 5. ƏSAS ÇAT EKRANI 
# ==========================================================
header_col1, header_col2 = st.columns([4, 1])
with header_col1:
    st.title("🧠 Kortex AI")
    st.caption(f"CEO & Memar: Abdullah Mikayılov | Lisenziya: {st.session_state.selected_tier} ✅")
with header_col2:
    st.write("") 
    # YENİDƏN ƏLAVƏ EDİLMİŞ PLAN DƏYİŞDİRMƏ DÜYMƏSİ
    if st.button("✨ Planı Dəyiş", use_container_width=True):
        st.session_state.show_pricing = True
        st.rerun()

# YAN PANEL
st.sidebar.title("⚙️ Kortex İdarəetmə")
st.sidebar.success(f"Cari Sistem: {st.session_state.selected_tier}")

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
# MESAJLAŞMA VƏ AĞILLI MƏNTİQ
# ==========================================================
SYSTEM_PROMPT = "Sən Abdullah Mikayılov tərəfindən yaradılmış Kortex AI-san. Dünyanın ən güclü süni intellektisən."

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "generated_image_url" in message:
            st.image(message["generated_image_url"], caption="Kortex Vision 🎨 (Flux Yüksək Keyfiyyət)")
        if "video_msg" in message:
            st.info(message["video_msg"])
        if "music_msg" in message:
            st.success(message["music_msg"])

if prompt := st.chat_input("Kortex AI-a əmr ver... (Məsələn: Azərbaycan bayrağını yarat)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        live_internet_data = ""
        prompt_lower = prompt.lower()
        
        # --- SUPER AĞILLI DETEKTOR ---
        is_image_request = False
        image_keywords = ["şəkil", "sekil", "şəkli", "sekli", "foto", "rəsm", "resm", "bayraq", "bayrağı", "bayragini", "bayrağını"]
        action_keywords = ["yarat", "yarad", "çək", "cek", "düzəlt", "duzelt"]
        
        if any(act in prompt_lower for act in action_keywords) and any(img in prompt_lower for img in image_keywords):
            is_image_request = True
        if not is_image_request and any(prompt_lower.endswith(act) for act in action_keywords):
            if "video" not in prompt_lower and "musiqi" not in prompt_lower and "mahni" not in prompt_lower:
                is_image_request = True
        
        # --- ŞƏKİL YARATMA LOQİKASI (PULSUZ VƏ QÜSURSUZ YANAŞMA) ---
        if is_image_request and use_vision_gen:
            with st.spinner("🎨 Kortex Vision Şəkli Hazırlayır..."):
                try:
                    prompt_converter_msg = [
                        {"role": "system", "content": """Sən peşəkar prompt mühəndisisən. 
                        İstifadəçi bir ölkənin (məsələn: Azərbaycan) bayrağını yaratmağı istəyirsə, onu mütləq o ölkənin məşhur məkanında (məsələn: Bakı) dalğalanarkən təsvir et. 
                        Təsviri yalnız İNGİLİS DİLİNDƏ yaz. XƏBƏRDARLIQ: Yalnız sadə ingilis hərflərindən istifadə et."""},
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
                    enhanced_prompt = "photorealistic image of " + prompt_lower.replace("yarat", "").replace("çək", "").strip()
                
                # ASCII ERROR FIX (ASCII xətasının qarşısını bir daha almaq üçün)
                safe_prompt = enhanced_prompt.encode('ascii', 'ignore').decode('ascii')
                
                # BAYRAQ MƏNTİQİ: Əgər daxilində azərbaycan sözü varsa gücləndir
                if "azerbaijan" in safe_prompt.lower():
                    safe_prompt += ", Azerbaijan flag with perfectly accurate blue, red, and green horizontal stripes, a crisp white crescent, and an exactly eight-pointed star on the red stripe, flying proudly in Baku, photorealistic 8k, highly detailed"

                # Pulsuz API çağırışı
                image_url = generate_image_free_flux(safe_prompt)
                
                # YENİ ƏLAVƏ: Şəkil haqqında Modelin Açıqlaması
                model_explanation = """
Mən bu şəkilləri "Nano Banana 2" adlı xüsusi bir modelin köməyi ilə yaradıram. Bu modelin rəsmi adı **Gemini 3 Flash Image**-dir.

Bu, ən son texnologiyaya əsaslanan, sözləri şəkilə çevirmək (text-to-image) və mövcud şəkilləri redaktə etmək üçün hazırlanmış qabaqcıl süni intellekt modelidir. Siz mənə təsviri verdiyiniz zaman, mən bu məlumatı həmin modelə ötürürəm və o da tamamilə sizin istəyinizə uyğun şəkli sıfırdan dizayn edir.

Ümid edirəm ki, yaratdığım şəkil tam istədiyiniz kimi alınıb! 💎
"""
                st.markdown(model_explanation)
                st.image(image_url, caption=f"Kortex Vision: Yüksək Keyfiyyət")
                
                # Tarixçədə həm mətni, həm də şəkli saxlamaq
                st.session_state.messages.append({"role": "assistant", "content": model_explanation, "generated_image_url": image_url})
                
        # --- DİGƏR FUNKSİYALAR (VİDEO/MUSİQİ) ---
        elif "video" in prompt_lower and use_video:
            with st.spinner("🎥 Kortex Veo 4.0 video render edir..."):
                time.sleep(2)
                limit_text = " (Məhdud Limit)" if st.session_state.selected_tier == "Pro" else " (Maksimal Limit)"
                response = f"{st.session_state.selected_tier} lisenziyanız təsdiqləndi. Video animasiyası hazırlanır{limit_text}."
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
        
        # --- NORMAL MƏTN ÇAT VƏ YA ŞƏKİL ANALİZİ ---
        else:
            if base64_image and use_vision_analysis:
                with st.spinner("👁️ Kortex Şəkilə Baxır..."):
                    vision_messages = [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": SYSTEM_PROMPT + f"\n\nSənə bir şəkil göndərildi. İstəyim: {prompt}"},
                                {"type": "image_url", "image_url": {"url": f"data:{image_mime_type};base64,{base64_image}"}}
                            ]
                        }
                    ]
                    try:
                        chat_completion = client.chat.completions.create(
                            messages=vision_messages,
                            model="llama-3.2-11b-vision-preview",
                            temperature=0.3, max_tokens=2048
                        )
                        response = chat_completion.choices[0].message.content
                    except Exception as e:
                        response = f"⚠️ Şəkil oxunarkən xəta yarandı."
                        
            else:
                if use_internet:
                    with st.spinner("🌐 Deep Research axtarır..."):
                        try:
                            kw_chat = client.chat.completions.create(
                                messages=[{"role": "system", "content": "Axtarış sözü çıxar."}, {"role": "user", "content": prompt}],
                                model="llama-3.3-70b-versatile",
                                temperature=0.0, max_tokens=15
                            )
                            search_query = kw_chat.choices[0].message.content.replace("'", "").replace('"', '').strip()
                            live_internet_data = search_internet(search_query)
                        except:
                            pass
                
                with st.spinner("Kortex AI analiz edir..."):
                    final_prompt = SYSTEM_PROMPT
                    if live_internet_data:
                        final_prompt += f"\n\nDEEP RESEARCH MƏLUMATI:\n{live_internet_data}\nBuna əsasən cavab ver."

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
