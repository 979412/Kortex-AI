import pypdf
import pandas as pd

class KortexReader:
    def __init__(self):
        print("🔍 KORTEX-AI Oxu Modulu Aktivdir.")

    def read_pdf(self, file_path):
        """PDF sənədini oxuyur və mətni çıxarır"""
        text = ""
        with open(file_path, "rb") as file:
            reader = pypdf.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text

    def analyze_excel(self, file_path):
        """Excel cədvəlini oxuyur və rəqəmləri analiz edir"""
        df = pd.read_excel(file_path)
        # Cədvəlin qısa xülasəsini Sİ-yə göndərmək üçün hazırlayırıq
        return df.describe().to_string()

# Test üçün (Lokalda işlədəndə):
# reader = KortexReader()
# print(reader.read_pdf("hesabat.pdf"))
