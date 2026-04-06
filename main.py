import google.generativeai as genai
import json
import os

# 1. API AÇARI
API_KEY = "SİZİN_API_AÇARINIZI_BURAYA_YAZIN"
genai.configure(api_key=API_KEY)

# 2. SİSTEM TƏLİMATI (System Prompt)
system_instruction = """
Sən KORTEX-AI-san. Qlobal bazarları analiz edən, riskləri hesablayan və 
yüksək gəlirli layihələr üçün addım-addım biznes planları hazırlayan qabaqcıl bir strateqsən. 
Məsləhətlərin konkret, rəqəmlərə əsaslanan və praktik olmalıdır. 
"""

# 3. PARAMETRLƏR
generation_config = genai.GenerationConfig(
    temperature=0.2,
    max_output_tokens=4000,
)

# --- MƏRHƏLƏ 1: KORTEX ÜÇÜN ALƏT (Function Calling) ---
def biznes_budce_hesabla(gelir: float, xerc: float, vergi_faizi: float) -> str:
    """KORTEX-AI bu alətdən istifadə edərək biznesin büdcəsini və vergisini dəqiq hesablayır."""
    vergi_meblegi = (gelir - xerc) * (vergi_faizi / 100)
    xalis_qazanc = (gelir - xerc) - vergi_meblegi
    
    if xalis_qazanc < 0:
        return f"DİQQƏT: Layihə ziyandadır! Ziyan: {abs(xalis_qazanc)} AZN. Vergi: {vergi_meblegi} AZN"
    else:
        return f"UĞURLU: Xalis qazanc {xalis_qazanc} AZN. Ödəniləcək vergi: {vergi_meblegi} AZN."

# 4. MODELİN YARADILMASI
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=system_instruction,
    generation_config=generation_config,
    tools=[biznes_budce_hesabla] # Aləti KORTEX-in beyninə qoşuruq
)

# --- MƏRHƏLƏ 2: YADDAŞ SİSTEMİ (Memory) ---
YADDAS_FAYLI = "kortex_yaddas.json"

def yaddasi_yukle():
    """Söhbət tarixçəsini JSON faylından oxuyur."""
    if os.path.exists(YADDAS_FAYLI):
        with open(YADDAS_FAYLI, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # Əgər yaddaş yoxdursa (proqram ilk dəfə açılırsa), ilkin yaddaş yaradılır
    return [
        {"role": "user", "parts": ["Salam, mənim adım Memardır. Sən mənim strateqimsən."]},
        {"role": "model", "parts": ["Salam Memar, mən KORTEX-AI. Biznesinizi inkişaf etdirmək üçün bütün xatirələri yaddaşımda saxlayacağam. Sizi dinləyirəm."]}
    ]

def yaddasi_saxla(chat_history):
    """Söhbət tarixçəsini xətasız şəkildə JSON faylına yazır."""
    yadda_saxlanilan = []
    for mesaj in chat_history:
        # Təhlükəsizlik: Yalnız adi mətnləri yaddaşa yazırıq ki, fayl xarab olmasın
        try:
            if hasattr(mesaj.parts[0], 'text'):
                yadda_saxlanilan.append({
                    "role": mesaj.role,
                    "parts": [mesaj.parts[0].text]
                })
        except:
            pass
            
    with open(YADDAS_FAYLI, "w", encoding="utf-8") as f:
        json.dump(yadda_saxlanilan, f, ensure_ascii=False, indent=4)

# 5. ƏSAS SİSTEM DÖVRÜ
def main():
    print("="*50)
    print(" KORTEX-AI SİSTEMİ: YADDAŞ VƏ HESABLAMA AKTİVDİR")
    print("="*50)
    print("Çıxmaq üçün 'exit' yazın.\n")

    # Yaddaşı yükləyirik və KORTEX-in söhbətini o yaddaşla başladırıq
    kecmis_yaddas = yaddasi_yukle()
    chat = model.start_chat(history=kecmis_yaddas)

    while True:
        user_input = input("Memar: ")
        
        if user_input.lower() in ['exit', 'quit', 'çix', 'cix', 'bağla']:
            print("\nKORTEX-AI: Məlumatlar yaddaşa yazıldı. Sistem bağlanır.")
            break
            
        if not user_input.strip():
            continue
            
        try:
            print("\nKORTEX-AI analiz edir...")
            response = chat.send_message(user_input)
            print(f"\nKORTEX-AI: {response.text}\n")
            print("-" * 50)
            
            # KORTEX sənə cavab verən kimi dərhal faylı güncəlləyir
            yaddasi_saxla(chat.history)
            
        except Exception as e:
            print(f"\n[XƏTA]: Sistemlə əlaqə kəsildi: {e}\n")

if __name__ == "__main__":
    main()
