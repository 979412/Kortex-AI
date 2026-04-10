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
    
    /* GÜCLƏNDİRİLMİŞ QİYMƏT KARTLARI */
    .pricing-card { border: 2px solid #edf2f7; border-radius: 15px; padding: 25px; background-color: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: transform 0.3s; position: relative; }
    .pricing-card:hover { transform: translateY(-5px); border-color: #1a73e8; box-shadow: 0 10px 20px rgba(26,115,232,0.15); }
    .tier-name { font-size: 24px; font-weight: bold; color: #202124; margin-bottom: 5px; text-align: center;}
    .tier-price { font-size: 36px; font-weight: bold; color: #1a73e8; margin: 15px 0; text-align: center;}
    .tier-price span { font-size: 18px; color: #5f6368; font-weight: normal; }
    .tier-desc { font-size: 14px; color: #3c4043; height: 260px; overflow-y: auto; text-align: left; margin-bottom: 20px; padding-right: 5px;}
    .tier-desc ul { padding-left: 20px; margin-top: 10px; }
    .tier-desc li { margin-bottom: 10px; line-height: 1.4;}
    
    /* ÖDƏNİŞ EKRANI */
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
                Gündəlik sadə işlər üçün başlanğıc:
                <ul>
                    <li>💬 Sadə mətn modeli</li>
                    <li>📄 1 MB PDF oxuma limiti</li>
                    <li>❌ İnternet bağlantısı yoxdur</li>
                    <li>❌ Media yaratma yoxdur</li>
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
                Peşəkarlar üçün gücləndirilmiş alətlər:
                <ul>
                    <li>🌐 <b>Deep Research:</b> Canlı İnternet Axtarışı</li>
                    <li>🎨 <b>Kortex Vision:</b> Şəkil yaratma (Gündəlik 50 limit)</li>
                    <li>☁️ <b>2 TB</b> Kortex Cloud Yaddaşı</li>
                    <li>📄 50 MB-a qədər PDF analizi</li>
                    <li>📧 Kortex Docs & Gmail İnteqrasiyası</li>
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
                <b>Limitsiz Ekosistem (Rəqibsiz):</b>
                <ul>
                    <li>🎥 <b>Veo 4.0:</b> Sinematik Video Yaratma</li>
                    <li>🎼 <b>Producer.ai:</b> Avtonom Musiqi Bəstələmə</li>
                    <li>🧠 <b>Antigravity:</b> Öz-özünə kod yazan Agent (Android Studio, CLI)</li>
                    <li>💎 <b>100,000</b> Aylıq AI Krediti</li>
                    <li>☁️ <b>Limitsiz (Unlimited)</b> Cloud Yaddaş</li>
                    <li>🚫 YouTube & Spotify Premium ekvivalenti</li>
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
    st.markdown("<div class='secure-badge'>🔒 Kortex Qlobal Ödəniş Sistemi (Stripe İnteqrasiyası)</div>", unsafe_allow_html=True)
    
    col_empty1, col_pay, col_empty2 = st.columns([1, 2, 1])
    with col_pay:
        st.markdown(f"<div class='payment-box'>", unsafe_allow_html=True)
        st.info(f"Ödəniləcək Məbləğ: **{price} / Ay**")
        card_name = st.text_input("Kartın üzərindəki Ad və Soyad", placeholder="Abdullah Mikayılov")
        card_number = st.text_input("Kartın Nömrəsi (16 rəqəm)", placeholder="XXXX XXXX XXXX XXXX", max_chars=19)
        c1, c2 = st.columns(2)
        with c1: exp_date = st.text_input("Bitmə Tarixi (AA/İİ)", placeholder="12/26", max_chars=5)
        with c2: cvv = st.text_input("CVV", placeholder="123", max_chars=3, type="password")
            
        st.write("")
        if st.button(f"Pulu Çıx və {st.session_state.selected_tier} Aktivləşdir", use_container_width=True):
            if card_name and card_number and exp_date and cvv:
                with st.spinner("💳 Bankla əlaqə yaradılır... Pul köçürülür..."):
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
    if st.button("✨ Planı Dəyiş", use_container_width=True):
        st.session_state.show_pricing = True
        st.rerun()

# ==========================================================
# YAN PANEL (TƏMİZLƏNDİ - YENİ ƏLAVƏLƏR ÜÇÜN HAZIRDIR)
# ==========================================================
st.sidebar.title("⚙️ Kortex İdarəetmə")
st.sidebar.success(f"Cari Sistem: {st.session_state.selected_tier}")

# Arxa planda işləyən funksiyalar (Ekranda görünmür, paketə görə avtomatik işləyir)
use_internet = st.session_state.selected_tier in ["Pro", "Ultra"]
use_vision = st.session_state.selected_tier in ["Pro", "Ultra"]
use_video = st.session_state.selected_tier == "Ultra"
use_music = st.session_state.selected_tier == "Ultra"

st.sidebar.markdown("---")
# İstifadəçi "ora nə əlavə edəcəm deyəcəm" dediyi üçün buranı boş saxladıq.

# PDF YÜKLƏMƏ
uploaded_file = st.sidebar.file_uploader("Sənəd Yüklə (PDF)", type=['pdf'])
document_text = ""
if uploaded_file is not None:
    if st.session_state.selected_tier == "Basic" and uploaded_file.size > 1000000:
        st.sidebar.error("❌ Basic paketdə 1 MB limiti var.")
    else:
        with st.spinner("Sənəd oxunur..."):
            try:
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text: document_text += text + "\n"
                document_text = document_text[:25000] 
                st.sidebar.success("✅ Sənəd hazır!")
            except Exception as e:
                st.sidebar.error(f"Xəta: {e}")

# ==========================================================
# MESAJLAŞMA VƏ AĞILLI MƏNTİQ
# ==========================================================
if document_text:
    SYSTEM_PROMPT = f"Sən Kortex AI-san. Mətn budur: {document_text}. Buna əsasən cavab ver."
else:
    SYSTEM_PROMPT = "Sən Abdullah Mikayılov tərəfindən yaradılmış Kortex AI-san. Dünyanın ən güclü Azərbaycanlı süni intellektisən. Heç nə uydurma."

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image_url" in message:
            st.image(message["image_url"], caption="Kortex Vision 🎨")
        if "video_msg" in message:
            st.info(message["video_msg"])
        if "music_msg" in message:
            st.success(message["music_msg"])

if prompt := st.chat_input("Kortex AI-a əmr ver... (Məs: 'Şəkil yarat', 'Video yarat', 'Musiqi bəstələ')"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        live_internet_data = ""
        prompt_lower = prompt.lower()
        
        # --- VİDEO YARATMA (VEO 4.0) ---
        if "video" in prompt_lower and use_video:
            with st.spinner("🎥 Kortex Veo 4.0 video render edir (Bu bir qədər vaxt apara bilər)..."):
                time.sleep(2)
                response = "Ultra lisenziyanız təsdiqləndi. Kortex Veo 4.0 mühərriki tapşırığınız üzrə yüksək keyfiyyətli video generasiyasına başladı."
                vid_msg = f"🎞️ [SİMULYASİYA] Kortex Veo 4.0 tərəfindən yaradılan video fayı: '{prompt}' (Sistem tam aktivləşəndə MP4 olaraq endiriləcək)"
                st.markdown(response)
                st.info(vid_msg)
                st.session_state.messages.append({"role": "assistant", "content": response, "video_msg": vid_msg})
                
        # --- MUSİQİ YARATMA (PRODUCER.AI) ---
        elif "musiqi" in prompt_lower and use_music:
            with st.spinner("🎼 Producer.ai notları və ritmi bəstələyir..."):
                time.sleep(2)
                response = "Musiqi studiyası işə salındı! İstəyinizə uyğun audiotrek bəstələnir."
                mus_msg = f"🎵 [SİMULYASİYA] Producer.ai Tərəfindən Bəstələnən Musiqi: '{prompt}' (MP3 kimi hazırlanır)"
                st.markdown(response)
                st.success(mus_msg)
                st.session_state.messages.append({"role": "assistant", "content": response, "music_msg": mus_msg})
        
        # --- ŞƏKİL YARATMA (KORTEX VISION) ---
        elif "şəkil" in prompt_lower and use_vision:
            with st.spinner("🎨 Kortex Vision şəkli çəkir..."):
                time.sleep(1) 
                img_prompt = prompt_lower.replace("şəkil", "").replace("yarat", "").replace("çək", "").strip()
                if not img_prompt: img_prompt = "futuristic AI core"
                generated_image_url = f"https://image.pollinations.ai/prompt/{img_prompt.replace(' ', '%20')}"
                response = f"Buyur, istədiyin **'{img_prompt}'** şəkli hazırdır!"
                st.markdown(response)
                st.image(generated_image_url, caption="Kortex Vision 🎨")
                st.session_state.messages.append({"role": "assistant", "content": response, "image_url": generated_image_url})
                
        # --- İNTERNET VƏ SÖHBƏT ---
        else:
            if use_internet:
                with st.spinner("🌐 Kortex Deep Research interneti axtarır..."):
                    try:
                        kw_chat = client.chat.completions.create(
                            messages=[{"role": "system", "content": "Axtarış sözü çıxar. Məs: 'boralonu taniyirsan' -> 'Boralo youtuber'"}, {"role": "user", "content": prompt}],
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
                    final_prompt += f"\n\nDEEP RESEARCH (İNTERNET) MƏLUMATI:\n{live_internet_data}\nBuna əsasən cavab ver."

                messages = [{"role": "system", "content": final_prompt}] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages if "image_url" not in m and "video_msg" not in m and "music_msg" not in m]

                try:
                    chat_completion = client.chat.completions.create(
                        messages=messages,
                        model="llama-3.3-70b-versatile",
                        temperature=0.3, max_tokens=2048
                    )
                    response = chat_completion.choices[0].message.content
                except Exception as e:
                    response = f"Xəta: {str(e)}"

                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
