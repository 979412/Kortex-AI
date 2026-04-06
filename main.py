import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="API Açarının Analizi", page_icon="🔍")
st.title("🔍 API Açarının Modelləri")

API_KEY = "AIzaSyAvgUNZUco4-KxQxtFOcKnoh4oUOyjIxmk"
genai.configure(api_key=API_KEY)

st.write("Sizin API açarınızın dəstəklədiyi modellər axtarılır...")

try:
    # Açarın dəstəklədiyi bütün modelləri siyahıya alırıq
    modeller = []
    for model in genai.list_models():
        # Yalnız 'generateContent' dəstəyi olanları (yəni çat edə bilənləri) seçirik
        if 'generateContent' in model.supported_generation_methods:
            modeller.append(model.name)
    
    if modeller:
        st.success(f"Tapıldı! API açarınız {len(modeller)} ədəd modeli dəstəkləyir:")
        
        # Modelləri siyahı şəklində göstəririk
        for m in modeller:
            st.code(m)
            
        st.info("KORTEX-AI kodunda `model_name=` hissəsinə yuxarıdakı siyahıdan ən güclü görünənini (məsələn, 'models/gemini-1.5-pro' və ya 'models/gemini-pro') yazmalısınız.")
    else:
        st.error("Sizin API açarınız heç bir mətn yaratma (generateContent) modelini dəstəkləmir.")

except Exception as e:
    st.error(f"Kritik Xəta: {e}")
    st.warning("Bu açar bloklanmış, səhv kopyalanmış və ya regional məhdudiyyətə (məsələn, IP bloku) düşmüş ola bilər.")
