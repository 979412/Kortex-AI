import google.generativeai as genai
import os

# 1. API AÇARI: Buraya öz Google Gemini API açarını yaz
API_KEY = "SİZİN_API_AÇARINIZI_BURAYA_YAZIN"
genai.configure(api_key=API_KEY)

# 2. SİSTEM TƏLİMATI (System Prompt): KORTEX-AI-ın beynini və xarakterini formalaşdırırıq
system_instruction = """
Sən KORTEX-AI-san. Qlobal bazarları analiz edən, riskləri hesablayan və 
yüksək gəlirli layihələr üçün addım-addım biznes planları hazırlayan qabaqcıl bir strateqsən. 
Məsləhətlərin konkret, rəqəmlərə əsaslanan və praktik olmalıdır. 
Mürəkkəb qərarlar verərkən həmişə mövzunu "addım-addım düşünərək" analiz et.
Mücərrəd və ümumi sözlərdən qaç, birbaşa həll yolları təklif et.
"""

# 3. PARAMETRLƏR: Modelin davranışını tənzimləyirik
generation_config = genai.GenerationConfig(
    temperature=0.2, # 0.2 qoyuruq ki, xəyalpərəst olmasın, ancaq dəqiq məntiq və faktlarla danışsın
    max_output_tokens=4000, # Biznes planlar uzun ola bilər deyə limitini yüksək tuturuq
)

# 4. MODELİN YARADILMASI
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=system_instruction,
    generation_config=generation_config
)

# 5. YADDAŞ VƏ NÜMUNƏLƏR (Few-Shot): Modelə necə cavab verəcəyini öyrədirik
chat = model.start_chat(history=[
    {"role": "user", "parts": ["Sən kimsən və mənə necə kömək edə bilərsən?"]},
    {"role": "model", "parts": ["Mən KORTEX-AI, sizin şəxsi biznes strateqinizəm. Məqsədim sizə qazanc gətirəcək optimal yolları tapmaqdır. Mənə layihəniz və ya hədəfiniz haqqında məlumat verin, mən sizə riskləri və addım-addım icra planını təqdim edim."]}
])

def main():
    print("="*40)
    print(" KORTEX-AI SİSTEMİ BAŞLADILDI ")
    print("="*40)
    print("Məsləhət almaq üçün sualınızı yazın. Çıxmaq üçün 'exit' yazın.\n")

    # 6. ƏSAS DÖVR: Söhbət interfeysi
    while True:
        user_input = input("Memar: ") # Sənin üçün özəlləşdirdim :)
        
        if user_input.lower() in ['exit', 'quit', 'çix', 'cix', 'bağla']:
            print("\nKORTEX-AI: Sistem bağlanır. Uğurlar!")
            break
            
        if not user_input.strip():
            continue
            
        try:
            # Sualı modelə göndəririk
            print("\nKORTEX-AI düşünür...")
            response = chat.send_message(user_input)
            print(f"\nKORTEX-AI: {response.text}\n")
            print("-" * 40)
        except Exception as e:
            print(f"\n[XƏTA]: Sistemlə əlaqə qurula bilmədi. Detal: {e}\n")

if __name__ == "__main__":
    main()
