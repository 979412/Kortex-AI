import os
from reader import KortexReader
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class KortexSystem:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.reader = KortexReader()
        print("🧠 KORTEX-AI Tam Sistem (Brain + Reader) İşə Düşdü.")

    def audit_document(self, file_path):
        print(f"📄 {file_path} analiz edilir...")
        
        # 1. Sənədi oxu
        doc_text = self.reader.read_pdf(file_path)
        
        # 2. Sİ-yə tapşırıq ver
        prompt = f"""
        Sən KORTEX-AI-san. Aşağıdakı biznes sənədini analiz et. 
        Məqsədimiz 100,000$ mənfəətə çatmaqdır. 
        Sənəddəki maliyyə risklərini və böyümə imkanlarını tap:
        
        SƏNƏD MƏTNİ:
        {doc_text[:5000]} # İlk 5000 simvolu göndəririk (limitə görə)
        """
        
        response = self.model.generate_content(prompt)
        return response.text

if __name__ == "__main__":
    kortex = KortexSystem()
    # Müştərinin PDF hesabatını bura daxil edirik
    # report = kortex.audit_document("musteri_hesabati.pdf")
    # print(report)
