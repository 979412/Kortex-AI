import google.generativeai as genai
import PIL.Image
import os

# 1. API AÇARI
API_KEY = "SİZİN_API_AÇARINIZI_BURAYA_YAZIN"
genai.configure(api_key=API_KEY)

# 2. MODELİN YARADILMASI (Gemini 1.5 Pro həm mətni, həm də şəkli eyni anda anlaya bilir)
model = genai.GenerativeModel("gemini-1.5-pro")

def vizual_analiz_et(sekil_yolu, sual):
    """KORTEX-AI-a şəkil/qrafik göndərib onun haqqında sual vermək üçün funksiya"""
    try:
        # Şəkli sistemdən oxuyuruq
        print(f"\n[KORTEX-AI] '{sekil_yolu}' faylı yüklənir və analiz edilir...")
        sekil = PIL.Image.open(sekil_yolu)
        
        # Həm şəkli, həm də sualı modelə göndəririk
        cavab = model.generate_content([sual, sekil])
        
        return cavab.text
    except FileNotFoundError:
        return "XƏTA: Şəkil tapılmadı. Faylın yolunu (path) düzgün yazdığınıza əmin olun."
    except Exception as e:
        return f"XƏTA: Sistem xətası baş verdi: {e}"

def main():
    print("="*50)
    print(" KORTEX-AI VİZUAL ANALİZ SİSTEMİ ")
    print("="*50)
    
    # Nümunə ssenari: Kompüterində olan bir qrafiki analiz etdirmək
    # QEYD: Kodu işlətməzdən əvvəl kompyuterində 'qrafik.jpg' adlı bir şəkil olmalıdır.
    fayl_yolu = input("Analiz etmək istədiyiniz şəklin adını (məsələn, qrafik.jpg) yazın: ")
    sual = input("KORTEX-AI-dan bu şəkillə bağlı nə istəyirsiniz? (Məsələn: 'Bu satış qrafikinə əsasən gələn ay üçün riskləri yaz'): ")
    
    if fayl_yolu and sual:
        netice = vizual_analiz_et(fayl_yolu, sual)
        print("\nKORTEX-AI-ın RƏYİ:\n")
        print(netice)
        print("-" * 50)

if __name__ == "__main__":
    main()
