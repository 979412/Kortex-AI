# Kortex Süni İntellekti - main.py faylı

def kortex_sistemi():
    print("*" * 50)
    print("Salam! Mən Kortex. Sizin şəxsi və çox güclü süni intellekt köməkçinizəm.")
    print("Sistem tam aktivdir. (Sistemi dayandırmaq üçün 'cixis' yazın)")
    print("*" * 50)

    # while True: dövrü sistemin heç vaxt yatmamasını və avtomatik işləməsini təmin edir
    while True:
        # İstifadəçidən sual alırıq
        sual = input("\nSualınızı yazın: ")
        
        # Əgər istifadəçi çıxmaq istəsə, sistem dayanır
        if sual.lower() == "cixis":
            print("Kortex: Sistem bağlanır. Yenə görüşərik!")
            break
            
        # Gələcəkdə bu hissəyə API qoşacağıq ki, hər suala səhvsiz cavab tapsın.
        # Hələlik isə sistemin avtomatik işlədiyini görmək üçün belə bir cavab veririk:
        print("Kortex: Mən bu sualı analiz edirəm... (Tezliklə burada əsl ağıllı cavablar olacaq!)")

# Kodu işə salmaq üçün əmr
kortex_sistemi()
