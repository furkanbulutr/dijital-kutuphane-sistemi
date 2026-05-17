# 📖 Dijital Kütüphane Yönetim Sistemi

Python ve Tkinter kullanılarak geliştirilmiş, modern kullanıcı arayüzüne sahip bir masaüstü kütüphane otomasyonudur. Proje, kullanıcıların kitap ödünç alma, iade etme ve geçmiş işlemlerini takip etmelerini sağlarken, kütüphane envanterinin dinamik bir şekilde yönetilmesine olanak tanır.

## ✨ Özellikler

* **Kullanıcı Yönetimi:** Üye ID ile hızlı giriş veya yeni üye kaydı oluşturma.
* **Geniş Koleksiyon:** 100'den fazla benzersiz kitap ve 50'den fazla örnek üye verisi (`veri_uretici.py` ile otomatik üretilir).
* **Dinamik İstatistikler:** Müsait kitaplar, ödünçte olanlar ve kullanıcının elindeki kitapların anlık takibi.
* **Kolay Ödünç & İade Sistemi:** Tek tıkla kitap ödünç alma ve tarih belirterek iade etme işlemleri.
* **Detaylı Takip:** Başka üyelerde olan kitapları görüntüleme ve tüm sistemdeki işlem geçmişini loglama.
* **Modern Arayüz:** Geleneksel Tkinter görünümlerinden uzak, özel renk paleti ve tipografi ile tasarlanmış kullanıcı dostu UI.

## 🚀 Kurulum ve Çalıştırma

Projeyi yerel bilgisayarında çalıştırmak için bilgisayarında **Python 3.x** kurulu olması yeterlidir. Ekstra bir dış kütüphane (pip paketi) gerektirmez.

1. Projeyi bilgisayarına klonla veya indir:
   ```bash
   git clone [https://github.com/kullaniciadin/dijital-kutuphane.git](https://github.com/kullaniciadin/dijital-kutuphane.git)
2. Proje dizinine git:
Bash
cd dijital-kutuphane

3. Uygulamayı başlat:
Bash
python main.py

📂 Proje Yapısı
main.py: Uygulamanın ana giriş noktasıdır. Arayüz (GUI) bileşenlerini, tema ayarlarını ve sistemin temel mantığını (Kullanıcı, Kitap, Ödünç sınıfları) içerir.
veri_uretici.py: Sistemin boş kalmaması için test amaçlı kitap kataloğu ve üye verilerini otomatik olarak oluşturan yardımcı modüldür.

📸 Ekran Görüntüleri
Giriş ve Kayıt Ekranı
Kullanıcıların mevcut ID'leri ile hızlıca giriş yapabildiği veya yeni kayıt oluşturabildiği karşılama ekranı.
![Giriş Ekranı](images/Ekran%20görüntüsü%202026-05-17%20162717.png)
![Kayıt Ol Ekranı](images/Ekran%20görüntüsü%202026-05-17%20162728.png)

Kitap Ödünç Alma Paneli
Müsait olan kitapların listelendiği, arama yapılabildiği ve tarih seçilerek ödünç alma işleminin gerçekleştirildiği sekme.
![Ödünç Al](images/Ekran%20görüntüsü%202026-05-17%20162741.png)

İade İşlemleri (Kitaplarım)
Aktif kullanıcının elinde bulunan kitapları görüntülediği ve kütüphaneye iade edebildiği bölüm.
![Kitaplarım](images/Ekran%20görüntüsü%202026-05-17%20162817.png)

Başkasında Olan Kitaplar
Kütüphanede o an müsait olmayan kitapların hangi üyede olduğunun ve ne zaman ödünç alındığının takip edildiği liste.
![Başkasında Olan Kitaplar](images/Ekran%20görüntüsü%202026-05-17%20162837.png)

Tüm İşlem Geçmişi
Sistemdeki tüm ödünç alma ve iade hareketlerinin anlık olarak kaydedildiği ve listelendiği genel log ekranı.
![İşlem Geçmişi](images/Ekran%20görüntüsü%202026-05-17%20162849.png)

🛠️ Kullanılan Teknolojiler
Dil: Python
GUI Kütüphanesi: Tkinter (ve ttk modülleri)
Tema: Clam Theme (Özel stil ve renk paleti giydirmeleri ile)
