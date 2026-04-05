import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Gizli şifrələrimizi (.env) yükləyirik
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. Kortex-in beynini konfiqurasiya edirik
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def kortex_salam():
    """Kortex-in ilk açılış mesajı"""
    print("--- KORTEX AI SİSTEMİ İŞƏ DÜŞDÜ ---")
    print("Yaradıcı: Abdullah Mikayılov\n")
    
    prompt = "Salam! Sən Kortex AI-sən. Bir cümlə ilə özünü dünya biznesinə təqdim et."
    
    try:
        response = model.generate_content(prompt)
        print(f"Kortex: {response.text}")
    except Exception as e:
        print(f"Xəta baş verdi: {e}")
        print("Məsləhət: .env faylında API açarının düzgün olduğundan əmin ol!")

if __name__ == "__main__":
    kortex_salam()
