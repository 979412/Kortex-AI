import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Ayarlar
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") # Sənin aldığın o kod bura gələcək
genai.configure(api_key=API_KEY)

class KortexEngine:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ KORTEX-AI Beyni Aktivləşdirildi.")

    def ask_strategy(self, prompt):
        # Bu hissə Sİ-yə biznesmen kimi düşünmək tapşırığını verir
        full_prompt = f"Sən KORTEX-AI Strateji Məsləhətçisisən. Bu biznes problemini analiz et və 3 konkret addım de: {prompt}"
        response = self.model.generate_content(full_prompt)
        return response.text

# İcra hissəsi
if __name__ == "__main__":
    kortex = KortexEngine()
    print(kortex.ask_strategy("Azərbaycanda Sİ əsaslı aqrar biznes qurmaq üçün ən böyük imkan haradadır?"))
