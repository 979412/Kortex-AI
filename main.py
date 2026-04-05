import os
import google.generativeai as genai

# Sənin o gizli uzun açarın bura gələcək
API_KEY = "SƏNİN_API_AÇARIN_BURA_GƏLƏCƏK" 
genai.configure(api_key=API_KEY)

class KortexElite:
    def __init__(self):
        # 1. ŞƏXSİYYƏT YARADILMASI (System Instruction)
        tehlimat = """
        Sən KORTEX-AI-san. Məqsədin istifadəçini 100,000$ mənfəətə çatdırmaqdır.
        Sən mehriban bot deyilsən, sən sərt və dahi bir biznes strateqisən.
        Məsləhətlərini qısa, konkret addımlarla və mütləq ehtimal olunan rəqəmlərlə/faizlərlə ver.
        Boş sözlərdən istifadə etmə.
        """
        
        self.model = genai.GenerativeModel(
            'gemini-1.5-flash',
            system_instruction=tehlimat
        )
        
        # 2. YADDAŞ SİSTEMİ (Chat Session)
        self.chat = self.model.start_chat(history=[])
        print("🟢 KORTEX-AI v3.0 Aktivdir: Yaddaş və Strateji Modul qoşuldu.\n")

    def sual_ver(self, mesaj):
        """Sİ ilə yaddaşlı formada danışmaq üçün funksiya"""
        print(f"SƏN: {mesaj}")
        print("KORTEX-AI Hesablayır...")
        
        # send_message metodu bütün əvvəlki söhbətləri yadda saxlayır
        response = self.chat.send_message(mesaj)
        return response.text

# --- SİSTEMİ TEST EDİRİK ---
if __name__ == "__main__":
    beyin = KortexElite()
    
    # Birinci Test: Sistemin şəxsiyyətini yoxlayırıq
    cavab_1 = beyin.sual_ver("Mənim cəmi 5000 manat pulum var. Azərbaycanda ən tez necə pul qazana bilərəm?")
    print(f"\n[KORTEX-AI]:\n{cavab_1}\n")
    print("-" * 50)
    
    # İkinci Test: Sistemin YADDAŞINI yoxlayırıq (KORTEX birinci sualı xatırlamalıdır)
    cavab_2 = beyin.sual_ver("Bəs sən dediyin o sahə üçün ilk 1000 manatımı konkret hara xərcləyim?")
    print(f"\n[KORTEX-AI]:\n{cavab_2}\n")
