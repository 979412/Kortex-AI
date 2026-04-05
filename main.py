import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Konfiqurasiya
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") 
genai.configure(api_key=API_KEY)

class KortexAI:
    def __init__(self):
        # Gemini 1.5 Flash - sürətli və ağıllı biznes analizi üçün
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.history = []
        print("✅ KORTEX-AI: Beyin mərkəzi aktivdir.")

    def analyze_business_case(self, sector, problem):
        """Müştəri üçün strateji analiz hazırlayır"""
        prompt = f"""
        Sən KORTEX-AI sistemisən. Rolun: Yüksək səviyyəli biznes strateqi.
        Sektor: {sector}
        Problem: {problem}
        
        Tapşırıq: Bu biznesi 100,000$ mənfəətə çatdırmaq üçün 3 konkret, 
        riyazi əsaslandırılmış və Sİ dəstəkli addım təklif et. 
        Cavabı peşəkar biznes dilində ver.
        """
        response = self.model.generate_content(prompt)
        return response.text

# --- SİSTEMİN İŞƏ SALINMASI ---
if __name__ == "__main__":
    kortex = KortexAI()
    
    # Nümunə Ssenari: Bir logistika şirkəti xərcləri azaltmaq istəyir
    print("\n[KORTEX-AI ANALİZİ BAŞLAYIR...]\n")
    result = kortex.analyze_business_case("Logistika və Daşıma", "Yanacaq xərcləri və sürücü vaxtı itkisi.")
    print(result)
