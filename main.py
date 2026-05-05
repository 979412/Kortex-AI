import google.generativeai as genai

# Kortex-in oyanması üçün lazım olan sehrli açar (API Key) bura yazılacaq
genai.configure(api_key="SƏNİN_API_AÇARIN_BURADA_OLACAQ")

# Kortex-in beyni kimi istifadə edəcəyimiz modeli seçirik
model = genai.GenerativeModel('gemini-1.5-flash')

def kortex_sistemi():
    print("*" * 50)
    print("Salam! Mən Kortex. Sizin şəxsi və çox güclü süni intellekt köməkçinizəm.")
    print("Sistem tam aktivdir. (Sistemi dayandırmaq üçün 'cixis' yazın)")
    print("*" * 50)

    while True:
        sual = input("\nSualınızı yazın: ")
        
        if sual.lower() == "cixis":
            print("Kortex: Sistem bağlanır. Yenə görüşərik!")
            break
            
        print("Kortex düşünür...")
        
        # Kortex sualı öz beyninə (API-yə) göndərir və avtomatik cavab hazırlayır
        try:
            cavab = model.generate_content(sual)
            print(f"\nKortex: {cavab.text}")
        except Exception as e:
            print("\nKortex: Bağışlayın, nəsə xəta baş verdi. Zəhmət olmasa bir də cəhd edin.")

# Sistemi işə salırıq
kortex_sistemi()
