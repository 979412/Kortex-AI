import os
import time
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# ==========================================
# 1. KONFİQURASİYA VƏ TƏHLÜKƏSİZLİK
# ==========================================
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("XƏTA: .env faylında API açarı tapılmadı!")
    exit()

genai.configure(api_key=API_KEY)
# Ən güclü modeli seçirik
model = genai.GenerativeModel('gemini-1.5-flash')

# ==========================================
# 2. KORTEX-İN YADDAŞ SİSTEMİ
# ==========================================
class KortexMemory:
    def __init__(self):
        self.chat_history = []
        self.data_folder = "data"
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

    def save_chat(self, user_input, ai_response):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.chat_history.append({"user": user_input, "ai": ai_response, "time": timestamp})

    def read_knowledge_base(self):
        """Data qovluğundakı bütün faylları oxuyur"""
        combined_text = ""
        for filename in os.listdir(self.data_folder):
            if filename.endswith(".txt"):
                with open(os.path.join(self.data_folder, filename), "r", encoding="utf-8") as f:
                    combined_text += f.read() + "\n"
        return combined_text

# ==========================================
# 3. ƏSAS FUNKSİYALAR
# ==========================================
memory = KortexMemory()

def generate_kortex_response(prompt, use_knowledge=False):
    context = ""
    if use_knowledge:
        context = "ŞİRKƏT MƏLUMATLARI:\n" + memory.read_knowledge_base() + "\n---\n"
    
    full_prompt = f"{context}İstifadəçi sualı: {prompt}\nSən Kortex AI-sən. Ciddi və ağıllı cavab ver."
    
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Sistem xətası: {str(e)}"

# ==========================================
# 4. İDARƏETMƏ PANELİ (MENU)
# ==========================================
def start_kortex():
    print("="*50)
    print("      KORTEX AI v1.0 - BY ABDULLAH MIKAYILOV")
    print("="*50)
    
    while True:
        print("\n[1] Kortex-lə söhbət et")
        print("[2] Şirkət sənədlərini analiz et (RAG)")
        print("[3] Yaddaşa bax (Keçmiş söhbətlər)")
        print("[4] Çıxış")
        
        secim = input("\nSeçiminizi edin (1-4): ")
        
        if secim == "1":
            user_msg = input("\nSualınız: ")
            print("\nKortex düşünür...")
            ai_msg = generate_kortex_response(user_msg)
            print(f"\nKortex: {ai_msg}")
            memory.save_chat(user_msg, ai_msg)
            
        elif secim == "2":
            print("\nSənədlər oxunur...")
            user_msg = input("Sənəd haqqında nəyi bilmək istəyirsiz?: ")
            ai_msg = generate_kortex_response(user_msg, use_knowledge=True)
            print(f"\nKortex (Analiz): {ai_msg}")
            
        elif secim == "3":
            print("\n--- KEÇMİŞ SÖHBƏTLƏR ---")
            for chat in memory.chat_history:
                print(f"[{chat['time']}] Sən: {chat['user']}")
                print(f"AI: {chat['ai'][:50]}...")
                
        elif secim == "4":
            print("Sistem bağlanır. Sağ ol, Abdullah!")
            break
        else:
            print("Yanlış seçim!")

if __name__ == "__main__":
    start_kortex()
    import json

# ==========================================
# 5. KORTEX BİZNES MODULU (CRM)
# ==========================================
class KortexBusiness:
    def __init__(self):
        self.customers_file = "data/customers.json"
        self.ensure_db()

    def ensure_db(self):
        if not os.path.exists(self.customers_file):
            with open(self.customers_file, "w") as f:
                json.dump({"customers": []}, f)

    def add_customer(self, name, business_type, problem):
        with open(self.customers_file, "r+") as f:
            data = json.load(f)
            new_cust = {
                "id": len(data["customers"]) + 1,
                "name": name,
                "type": business_type,
                "problem": problem,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            data["customers"].append(new_cust)
            f.seek(0)
            json.dump(data, f, indent=4)
        return f"Müştəri {name} uğurla bazaya əlavə edildi."

    def get_all_customers(self):
        with open(self.customers_file, "r") as f:
            return json.load(f)["customers"]

# Biznes modulunu işə salırıq
business_node = KortexBusiness()

# ==========================================
# 6. AVTOMATİK STRATEQİYA YARADICI
# ==========================================
def generate_business_strategy(customer_id):
    customers = business_node.get_all_customers()
    target = next((c for c in customers if c["id"] == int(customer_id)), None)
    
    if not target:
        return "Müştəri tapılmadı!"
    
    prompt = f"""
    Müştəri: {target['name']}
    Sahə: {target['type']}
    Problem: {target['problem']}
    
    Sən Kortex AI-sən. Bu müştəri üçün 3 addımlıq satış strategiyası yaz və 
    onun qazancını necə 2 qat artıra biləcəyimizi izah et.
    """
    return generate_kortex_response(prompt)
    print("[5] Yeni Müştəri Əlavə Et (CRM)")
        print("[6] Müştəri Üçün Satış Strategiyası Qur")
        
        # ... (digər if-lər) ...
        
        elif secim == "5":
            name = input("Müştəri adı: ")
            b_type = input("Biznes sahəsi: ")
            prob = input("Əsas problemi nədir?: ")
            result = business_node.add_customer(name, b_type, prob)
            print(result)
            
        elif secim == "6":
            c_id = input("Strategiya qurulacaq müştəri ID-si: ")
            print("\nKortex strategiya hazırlayır...")
            strategy = generate_business_strategy(c_id)
            print(f"\n--- ÖZƏL STRATEGİYA ---\n{strategy}")
import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from colorama import Fore, Back, Style, init

# Rəngləri işə salırıq
init(autoreset=True)

# ==========================================
# 1. AYARLAR VƏ TƏHLÜKƏSİZLİK
# ==========================================
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print(Fore.RED + "XƏTA: .env faylında API açarı tapılmadı!")
    exit()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ==========================================
# 2. KORTEX MƏLUMAT SİSTEMİ (DATABASE)
# ==========================================
class KortexDB:
    def __init__(self):
        self.base_dir = "data"
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
        
        self.cust_file = os.path.join(self.base_dir, "customers.json")
        self.fin_file = os.path.join(self.base_dir, "finance.json")
        self._init_files()

    def _init_files(self):
        for file in [self.cust_file, self.fin_file]:
            if not os.path.exists(file):
                with open(file, "w") as f:
                    json.dump({"data": []}, f)

    def add_data(self, file_path, entry):
        with open(file_path, "r+") as f:
            content = json.load(f)
            content["data"].append(entry)
            f.seek(0)
            json.dump(content, f, indent=4)

# Verilənlər bazasını yaradırıq
db = KortexDB()

# ==========================================
# 3. MALİYYƏ ANALİZ MODULU (YENİ!)
# ==========================================
def add_expense(item, amount):
    """Şirkət xərclərini qeyd edir"""
    entry = {
        "item": item,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    db.add_data(db.fin_file, entry)
    return f"{item} üçün {amount} AZN xərc qeyd olundu."

def get_financial_report():
    """Kortex bütün xərcləri analiz edir"""
    with open(db.fin_file, "r") as f:
        data = json.load(f)["data"]
    
    if not data:
        return "Hələ ki, maliyyə məlumatı yoxdur."
    
    total = sum(float(x["amount"]) for x in data)
    report_context = f"Ümumi xərc: {total} AZN. Detallar: {str(data)}"
    
    prompt = f"Məlumat: {report_context}\nSən Kortex-sən. Bu maliyyə vəziyyətini analiz et və qənaət üçün 2 məsləhət ver."
    response = model.generate_content(prompt)
    return f"Ümumi Xərc: {total} AZN\n\nKortex Analizi:\n{response.text}"

# ==========================================
# 4. KORTEX LOGO VƏ MENYU
# ==========================================
def show_logo():
    print(Fore.CYAN + Style.BRIGHT + """
    #################################################
    #                                               #
    #      K O R T E X   A I   S Y S T E M          #
    #         Created by: Abdullah M.               #
    #                                               #
    #################################################
    """)

def start_kortex():
    show_logo()
    
    while True:
        print(Fore.YELLOW + "\n--- ƏSAS MENYU ---")
        print("1. Kortex ilə Söhbət")
        print("2. Müştəri Əlavə Et")
        print("3. Xərc Qeyd Et (Maliyyə)")
        print("4. Maliyyə Hesabatı Al (AI Analiz)")
        print("5. Çıxış")
        
        secim = input(Fore.GREEN + "\nSeçiminiz: ")
        
        if secim == "1":
            msg = input("Siz: ")
            res = model.generate_content(msg)
            print(Fore.BLUE + f"\nKortex: {res.text}")
            
        elif secim == "2":
            name = input("Ad: ")
            biz = input("Sahə: ")
            entry = {"name": name, "type": biz, "date": str(datetime.now())}
            db.add_data(db.cust_file, entry)
            print(Fore.GREEN + "Müştəri uğurla yadda saxlanıldı!")
            
        elif secim == "3":
            item = input("Nə almısınız?: ")
            price = input("Qiyməti (AZN): ")
            print(add_expense(item, price))
            
        elif secim == "4":
            print(Fore.MAGENTA + "\nKortex rəqəmləri hesablayır...")
            print(get_financial_report())
            
        elif secim == "5":
            print(Fore.RED + "Sistem söndürülür. Uğurlar, Abdullah!")
            break

if __name__ == "__main__":
    start_kortex()
