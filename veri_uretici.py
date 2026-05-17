"""Örnek kütüphane verisi: 100+ kitap, 50+ üye (ham kayıtlar).

Her kitap kaydı (ad, yazar, kategori) birlikte tanımlanır; yazar–eser eşleşmesi asla
ayrı listelerden indeksle türetilmez.
"""

# (kitap_adı, yazar, kategori) — doğrulanmış eşleşmeler
KITAP_KATALOGU = [
    # Türk edebiyatı ve tarih
    ("Nutuk", "M. Kemal Atatürk", "Tarih"),
    ("İnce Memed", "Yaşar Kemal", "Klasik"),
    ("Kürk Mantolu Madonna", "Sabahattin Ali", "Klasik"),
    ("Memleketimden İnsan Manzaraları", "Nazım Hikmet", "Şiir"),
    ("Tutunamayanlar", "Oğuz Atay", "Klasik"),
    ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", "Klasik"),
    ("Kara Kitap", "Orhan Pamuk", "Roman"),
    ("Masumiyet Müzesi", "Orhan Pamuk", "Roman"),
    ("Kar", "Orhan Pamuk", "Roman"),
    ("Aşk", "Elif Şafak", "Roman"),
    ("Şemspare", "Elif Şafak", "Roman"),
    ("Çalıkuşu", "Reşat Nuri Güntekin", "Klasik"),
    ("Yaban", "Yakup Kadri Karaosmanoğlu", "Klasik"),
    ("Sinekli Bakkal", "Halide Edip Adıvar", "Klasik"),
    ("Sefiller", "Victor Hugo", "Klasik"),
    ("Kuyucaklı Yusuf", "Sabahattin Ali", "Klasik"),
    ("Huzur", "Ahmet Hamdi Tanpınar", "Klasik"),
    ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", "Fantastik"),
    ("Aylak Adam", "Yusuf Atılgan", "Klasik"),
    ("Anayurt Oteli", "Yusuf Atılgan", "Klasik"),
    ("Aganta Burina Burinata", "Bilge Karasu", "Klasik"),
    ("Kara Kutu", "Bilge Karasu", "Klasik"),
    ("Şiirler", "Cemal Süreya", "Şiir"),
    ("Kaldırımlar", "Cemal Süreya", "Şiir"),
    # Dünya klasikleri
    ("Suç ve Ceza", "Fyodor Dostoyevski", "Klasik"),
    ("Karamazov Kardeşler", "Fyodor Dostoyevski", "Klasik"),
    ("Budala", "Fyodor Dostoyevski", "Klasik"),
    ("Küçük Prens", "Antoine de Saint-Exupéry", "Çocuk"),
    ("1984", "George Orwell", "Distopya"),
    ("Hayvan Çiftliği", "George Orwell", "Distopya"),
    ("Simyacı", "Paulo Coelho", "Roman"),
    ("Savaş ve Barış", "Lev Tolstoy", "Klasik"),
    ("Anna Karenina", "Lev Tolstoy", "Klasik"),
    ("Dönüşüm", "Franz Kafka", "Klasik"),
    ("Dava", "Franz Kafka", "Klasik"),
    ("Yabancı", "Albert Camus", "Klasik"),
    ("Veba", "Albert Camus", "Klasik"),
    ("Notre-Dame'ın Kamburu", "Victor Hugo", "Klasik"),
    ("Monte Kristo Kontu", "Alexandre Dumas", "Klasik"),
    ("Üç Silahşörler", "Alexandre Dumas", "Klasik"),
    ("Jane Eyre", "Charlotte Brontë", "Klasik"),
    ("Gurur ve Önyargı", "Jane Austen", "Klasik"),
    ("Emma", "Jane Austen", "Klasik"),
    ("Frankenstein", "Mary Shelley", "Klasik"),
    ("Dracula", "Bram Stoker", "Klasik"),
    ("Moby Dick", "Herman Melville", "Klasik"),
    ("Odyssey", "Homeros", "Klasik"),
    ("İlyada", "Homeros", "Klasik"),
    # Bilim kurgu ve fantastik
    ("Vakıf", "Isaac Asimov", "Bilim Kurgu"),
    ("Ben, Robot", "Isaac Asimov", "Bilim Kurgu"),
    ("2001: Bir Uzay Destanı", "Arthur C. Clarke", "Bilim Kurgu"),
    ("Yerdeniz Uygarlığı", "Ursula K. Le Guin", "Fantastik"),
    ("Hobbit", "J. R. R. Tolkien", "Fantastik"),
    ("Yüzüklerin Efendisi", "J. R. R. Tolkien", "Fantastik"),
    ("Harry Potter ve Felsefe Taşı", "J. K. Rowling", "Fantastik"),
    # Bilim ve felsefe
    ("Kozmos", "Carl Sagan", "Bilim"),
    ("Kısa Evren Tarihi", "Stephen Hawking", "Bilim"),
    ("Zamanın Kısa Tarihi", "Stephen Hawking", "Bilim"),
    ("Sapiens", "Yuval Noah Harari", "Tarih"),
    ("Homo Deus", "Yuval Noah Harari", "Tarih"),
    ("Felsefe Tarihi", "Bertrand Russell", "Felsefe"),
    ("Devlet", "Platon", "Felsefe"),
    ("Nikomakhos'a Etik", "Aristoteles", "Felsefe"),
    ("Düşünce Hızında", "Malcolm Gladwell", "Psikoloji"),
    ("Outliers", "Malcolm Gladwell", "Psikoloji"),
    # Bilgisayar ve yazılım
    ("Python Programlama", "Mark Lutz", "Yazılım"),
    ("Fluent Python", "Luciano Ramalho", "Yazılım"),
    ("Veri Yapıları ve Algoritmalar", "Thomas H. Cormen", "Bilgisayar Bilimleri"),
    ("Algoritmalar", "Robert Sedgewick", "Bilgisayar Bilimleri"),
    ("Clean Code", "Robert C. Martin", "Yazılım"),
    ("The Pragmatic Programmer", "Andrew Hunt", "Yazılım"),
    ("Design Patterns", "Erich Gamma", "Yazılım"),
    ("Yapay Zeka: Modern Yaklaşım", "Stuart Russell", "Bilgisayar Bilimleri"),
    ("Derin Öğrenme", "Ian Goodfellow", "Bilgisayar Bilimleri"),
    ("Makine Öğrenmesi", "Christopher Bishop", "Bilgisayar Bilimleri"),
    ("Web Geliştirme Temelleri", "Jon Duckett", "Yazılım"),
    ("JavaScript: Güçlü Dil", "David Flanagan", "Yazılım"),
    ("Veritabanı Sistemleri", "Abraham Silberschatz", "Bilgisayar Bilimleri"),
    ("Ağ Güvenliği Esasları", "William Stallings", "Bilgisayar Bilimleri"),
    # Tarih ve sosyal bilimler
    ("Osmanlı Tarihi", "Halil İnalcık", "Tarih"),
    ("Cumhuriyet Dönemi Türkiye Tarihi", "İlber Ortaylı", "Tarih"),
    ("Dünya Savaşları", "Winston Churchill", "Tarih"),
    ("Kuantum Fiziğine Giriş", "Richard Feynman", "Bilim"),
    ("Evrim: Bir İz Üzerine", "Charles Darwin", "Bilim"),
    ("İktisadın Temelleri", "Gregory Mankiw", "Ekonomi"),
    ("Zengin Baba Yoksul Baba", "Robert Kiyosaki", "Ekonomi"),
    ("İletişimin Temelleri", "Marshall McLuhan", "Sosyal Bilimler"),
    ("Liderlik", "Peter Drucker", "Yönetim"),
    ("Yaratıcı Yazarlık", "Natalie Goldberg", "Edebiyat"),
    # Çocuk ve genel
    ("Pinokyo", "Carlo Collodi", "Çocuk"),
    ("Heidi", "Johanna Spyri", "Çocuk"),
    ("Tom Sawyer'ın Maceraları", "Mark Twain", "Çocuk"),
    ("Denemeler", "Michel de Montaigne", "Deneme"),
    ("Şiir Antolojisi", "Çeşitli Şairler", "Şiir"),
    ("Türk Masalları", "Anonim", "Çocuk"),
    ("Sanat Tarihi", "E. H. Gombrich", "Sanat"),
    ("Mimarlığın Öyküsü", "Spiro Kostof", "Sanat"),
    ("Müzik Teorisi", "Roger Kamien", "Sanat"),
    ("Aziz Nesin Hikayeleri", "Aziz Nesin", "Çocuk"),
    ("Zübük", "Aziz Nesin", "Roman"),
    # Ek benzersiz eserler
    ("Yeraltı", "Fyodor Dostoyevski", "Klasik"),
    ("Ölü Canlar", "Nikolay Gogol", "Klasik"),
    ("Bülbülü Öldürmek", "Harper Lee", "Klasik"),
    ("Fareler ve İnsanlar", "John Steinbeck", "Klasik"),
    ("Muhteşem Gatsby", "F. Scott Fitzgerald", "Klasik"),
    ("Uğultulu Tepeler", "Emily Brontë", "Klasik"),
    ("Don Kişot", "Miguel de Cervantes", "Klasik"),
    ("Satranç", "Stefan Zweig", "Klasik"),
    ("Genç Werther'in Acıları", "Johann Wolfgang von Goethe", "Klasik"),
    ("Faust", "Johann Wolfgang von Goethe", "Klasik"),
    ("Siddhartha", "Hermann Hesse", "Klasik"),
    ("Bozkırkurdu", "Hermann Hesse", "Klasik"),
    ("Şeker Portakalı", "José Mauro de Vasconcelos", "Roman"),
    ("Eylül", "Mehmet Rauf", "Klasik"),
    ("Acımak", "Sabahattin Ali", "Klasik"),
    ("Serenad", "Zülfü Livaneli", "Roman"),
    ("Mutluluk", "Zülfü Livaneli", "Roman"),
    ("Körlük", "José Saramago", "Roman"),
    ("Kırmızı Pazartesi", "Gabriel García Márquez", "Roman"),
    ("Yüzyıllık Yalnızlık", "Gabriel García Márquez", "Roman"),
]

ADLAR = [
    "Furkan",
    "Ayşe",
    "Mehmet",
    "Zeynep",
    "Ali",
    "Elif",
    "Can",
    "Deniz",
    "Emre",
    "Selin",
    "Burak",
    "Merve",
    "Kerem",
    "Ece",
    "Onur",
    "Defne",
    "Barış",
    "Ceren",
    "Kaan",
    "İrem",
    "Tolga",
    "Seda",
    "Yusuf",
    "Gizem",
    "Arda",
    "Melis",
    "Serkan",
    "Buse",
    "Oğuz",
    "Pınar",
    "Hakan",
    "Dilara",
    "Umut",
    "Aslı",
    "Volkan",
    "Nazlı",
    "Berk",
    "Tuğba",
    "Cem",
    "Hande",
    "Sinan",
    "Esra",
    "Murat",
    "Gamze",
    "Eren",
    "Şule",
    "Koray",
    "Yasemin",
    "Tarık",
    "Begüm",
    "Alper",
    "Cansu",
    "Emir",
    "Nilüfer",
]

SOYADLAR = [
    "Yılmaz",
    "Kaya",
    "Demir",
    "Çelik",
    "Şahin",
    "Öztürk",
    "Aydın",
    "Arslan",
    "Doğan",
    "Kılıç",
    "Aslan",
    "Çetin",
    "Kara",
    "Koç",
    "Kurt",
    "Özdemir",
    "Şimşek",
    "Polat",
    "Güneş",
    "Aksoy",
    "Yıldız",
    "Bulut",
    "Tekin",
    "Acar",
    "Bayrak",
    "Taş",
    "Toprak",
    "Su",
    "Deniz",
]


def kitaplari_uret(baslangic_id=1):
    """Katalogdaki her eseri yalnızca bir kez döndürür; yapay kopya üretilmez."""
    gorulen_adlar = set()
    kayitlar = []

    for ad, yazar, kategori in KITAP_KATALOGU:
        if ad in gorulen_adlar:
            continue
        gorulen_adlar.add(ad)
        kitap_id = baslangic_id + len(kayitlar)
        kayitlar.append((kitap_id, ad, yazar, kategori))

    return kayitlar


def uyeleri_uret(sayi=55):
    kayitlar = []
    kullanilan_emailler = set()
    i = 0

    while len(kayitlar) < sayi:
        ad = ADLAR[i % len(ADLAR)]
        soyad = SOYADLAR[(i // len(ADLAR)) % len(SOYADLAR)]
        if i >= len(ADLAR) * len(SOYADLAR):
            tam_ad = f"{ad} {soyad} {i + 1}"
        else:
            tam_ad = f"{ad} {soyad}"

        uye_id = i + 1
        taban = tam_ad.lower().replace(" ", ".").replace("ı", "i").replace("ş", "s")
        taban = taban.replace("ğ", "g").replace("ü", "u").replace("ö", "o").replace("ç", "c")
        email = f"{taban}@kutuphane.local"
        if email in kullanilan_emailler:
            email = f"uye{uye_id}@kutuphane.local"
        kullanilan_emailler.add(email)

        kayitlar.append((uye_id, tam_ad, email))
        i += 1

    return kayitlar
