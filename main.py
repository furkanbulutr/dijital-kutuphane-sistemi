import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class Kitap:
    # Sınıf (class): Ortak özellik ve davranışları tanımlayan kalıptır.
    # Nesne (instance): Kitap(...) dediğimizde bu kalıptan tek bir kitap örneği oluşur.

    def __init__(self, kitap_id, ad, yazar, kategori):
        # __init__: Sınıftan yeni bir nesne yaratıldığında otomatik çalışan kurucu metottur.
        # self: "Bu nesnenin kendisi" demektir; aşağıdaki özellikler (attribute) bu kitap örneğine aittir.
        self.kitap_id = kitap_id
        self.ad = ad
        self.yazar = yazar
        self.kategori = kategori
        self.durum = "Mevcut"
        self.su_anki_sahibi = None

    def kitap_durumu_degistir(self, yeni_durum):
        # Metot: Nesnenin davranışı; bu kitabın durumunu değiştirir (ör. Mevcut → Ödünç Verildi).
        self.durum = yeni_durum


class Uye:
    # Üye de bir sınıftır; Furkan, Ayşe gibi her kişi ayrı bir Uye nesnesidir.

    def __init__(self, uye_id, ad, email):
        self.uye_id = uye_id
        self.ad = ad
        self.email = email
        self.odunc_alinan_kitaplar = []

    def kitap_odunc_al(self, kitap):
        # Parametredeki kitap başka bir nesnedir; onun metot ve alanlarına buradan erişebiliriz.
        self.odunc_alinan_kitaplar.append(kitap)
        kitap.kitap_durumu_degistir("Ödünç Verildi")
        kitap.su_anki_sahibi = self

    def kitap_iade_et(self, kitap):
        # Sadece gerçekten bu üyenin listesindeyse iade işlemi yapılır (güvenli kontrol).
        if kitap in self.odunc_alinan_kitaplar:
            self.odunc_alinan_kitaplar.remove(kitap)
            kitap.kitap_durumu_degistir("Mevcut")
            kitap.su_anki_sahibi = None


class Odunc:
    # Ödünç kaydı: İçinde Kitap ve Uye nesnelerine referans tutar (ilişki kurar).

    def __init__(self, odunc_id, kitap, uye, odunc_tarihi):
        self.odunc_id = odunc_id
        self.kitap = kitap
        self.uye = uye
        self.odunc_tarihi = odunc_tarihi
        self.iade_tarihi = None


class Kutuphane:
    # Tek bir kütüphane sistemini temsil eder; listeler içinde birçok Kitap/Uye/Odunc nesnesi tutulur.

    def __init__(self):
        self.kitaplar = []
        self.uyeler = []
        self.oduncler = []
        self.odunc_sayaci = 1
        # Nesne oluşur oluşmaz örnek veriyi doldururuz; böylece liste her zaman dolu başlar.
        self.verileri_yukle()

    def verileri_yukle(self):
        # Başlangıç verisi: demetlerden Kitap nesneleri üretip self.kitaplar listesine ekliyoruz.
        kitap_listesi = [
            (101, "Python Programlama", "M. Tarkan", "Yazılım"),
            (102, "Veri Yapıları", "A. Yılmaz", "Bilgisayar Bilimleri"),
            (103, "Nutuk", "M. Kemal Atatürk", "Tarih"),
            (104, "Suç ve Ceza", "Dostoyevski", "Klasik"),
            (105, "Küçük Prens", "Saint-Exupéry", "Çocuk"),
            (106, "1984", "George Orwell", "Distopya")
        ]
        for k in kitap_listesi:
            # *k: demeti açıp Kitap.__init__'e ayrı argümanlar olarak verir (ör. 101, "Python...", ...).
            self.kitaplar.append(Kitap(*k))

        self.uyeler.append(Uye(1, "Furkan", "furkan@mail.com"))
        self.uyeler.append(Uye(2, "Ayşe", "ayse@mail.com"))
        self.uyeler.append(Uye(3, "Mehmet", "mehmet@mail.com"))


class KutuphaneUygulamasi:
    # Arayüz sınıfı: Kutuphane veri sınıfından bağımsızdır; self.sistem ile ona erişir (ayırmak bakımı kolaylaştırır).

    def __init__(self, root):
        self.root = root
        self.root.title("Dijital Kütüphane Sistemi v6.0 (Tam Sürüm)")
        self.root.geometry("850x600")
        # Kutuphane: tüm kitap/üye/ödünç verisi burada; arayüz doğrudan listelere karışmaz, self.sistem üzerinden gider.
        self.sistem = Kutuphane()
        self.aktif_kullanici = None

        self.giris_ekrani()

    def giris_ekrani(self):
        # Önce penceredeki eski bileşenleri silip sadece giriş arayüzünü kuruyoruz.
        self.temizle()
        self.ana_cerceve = tk.Frame(self.root, pady=50)
        self.ana_cerceve.pack()

        tk.Label(self.ana_cerceve, text="Kütüphane Girişi", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(self.ana_cerceve, text="Üye ID Numaranız (1, 2 veya 3):").pack()

        self.id_giris = tk.Entry(self.ana_cerceve)
        self.id_giris.pack(pady=10)
        self.id_giris.insert(0, "1")

        tk.Button(self.ana_cerceve, text="Giriş Yap", command=self.login, bg="blue", fg="white", width=15).pack()

    def login(self):
        try:
            girilen_id = int(self.id_giris.get())
            # next(..., None): Listede eşleşen ilk üyeyi bulur; yoksa None döner (hata vermez).
            uye = next((u for u in self.sistem.uyeler if u.uye_id == girilen_id), None)

            if uye:
                self.aktif_kullanici = uye
                self.ana_panel()
            else:
                messagebox.showerror("Hata", "Bu ID ile kayıtlı üye bulunamadı!")
        except ValueError:
            messagebox.showerror("Hata", "Lütfen sayısal ID girin.")

    def ana_panel(self):
        self.temizle()
        # Notebook: Sekmeli yapı; her sekme bir Frame, içine farklı sayfa metotları yerleştirir.

        ust_panel = tk.Frame(self.root, pady=10, bg="#f0f0f0")
        ust_panel.pack(fill=tk.X)
        tk.Label(ust_panel, text=f"Aktif Kullanıcı: {self.aktif_kullanici.ad}", font=("Arial", 11, "bold"), bg="#f0f0f0").pack(side=tk.LEFT, padx=20)
        tk.Button(ust_panel, text="Güvenli Çıkış", command=self.giris_ekrani, bg="red", fg="white").pack(side=tk.RIGHT, padx=20)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)

        self.tab_al = tk.Frame(self.tabs)
        self.tabs.add(self.tab_al, text="Kitap Ödünç Al")
        self.kitap_al_sayfasi()

        self.tab_yok = tk.Frame(self.tabs)
        self.tabs.add(self.tab_yok, text="Kütüphanede Olmayanlar")
        self.kitap_yok_sayfasi()

        self.tab_iade = tk.Frame(self.tabs)
        self.tabs.add(self.tab_iade, text="Eldeki Kitaplarım")
        self.kitap_iade_sayfasi()

        self.tab_gecmis = tk.Frame(self.tabs)
        self.tabs.add(self.tab_gecmis, text="Tüm İşlem Geçmişi")
        self.islem_gecmisi_sayfasi()

    def kitap_al_sayfasi(self):
        cols = ('ID', 'Kitap Adı', 'Yazar', 'Kategori')
        self.tree_al = ttk.Treeview(self.tab_al, columns=cols, show='headings')
        for col in cols: self.tree_al.heading(col, text=col)
        self.tree_al.pack(expand=True, fill="both", padx=10, pady=10)

        tk.Label(self.tab_al, text="Ödünç Alma Tarihi:").pack()
        self.odunc_tarih_giris = tk.Entry(self.tab_al)
        self.odunc_tarih_giris.pack(pady=5)
        self.odunc_tarih_giris.insert(0, datetime.now().strftime("%d.%m.%Y"))

        tk.Button(self.tab_al, text="Seçili Kitabı Ödünç Al", command=self.odunc_al_aksiyon, bg="green", fg="white").pack(pady=10)
        self.listele_al()

    def kitap_yok_sayfasi(self):
        cols = ('ID', 'Kitap Adı', 'Şu An Kimde?', 'Ödünç Alındığı Tarih')
        self.tree_yok = ttk.Treeview(self.tab_yok, columns=cols, show='headings')
        for col in cols: self.tree_yok.heading(col, text=col)
        self.tree_yok.pack(expand=True, fill="both", padx=10, pady=10)

        tk.Label(self.tab_yok, text="* Bu kitaplar başka üyeler tarafından alınmıştır.", fg="red").pack()
        self.listele_yok()

    def kitap_iade_sayfasi(self):
        cols = ('ID', 'Kitap Adı', 'Ödünç Alma Tarihi')
        self.tree_iade = ttk.Treeview(self.tab_iade, columns=cols, show='headings')
        for col in cols: self.tree_iade.heading(col, text=col)
        self.tree_iade.pack(expand=True, fill="both", padx=10, pady=10)

        tk.Label(self.tab_iade, text="İade Edilme Tarihi:").pack()
        self.iade_tarih_giris = tk.Entry(self.tab_iade)
        self.iade_tarih_giris.pack(pady=5)
        self.iade_tarih_giris.insert(0, datetime.now().strftime("%d.%m.%Y"))

        tk.Button(self.tab_iade, text="Seçili Kitabı İade Et", command=self.iade_et_aksiyon, bg="orange", fg="white").pack(pady=10)
        self.listele_iade()

    def islem_gecmisi_sayfasi(self):
        cols = ('İşlem ID', 'Kitap Adı', 'Üye Adı', 'Ödünç Tarihi', 'İade Tarihi')
        self.tree_gecmis = ttk.Treeview(self.tab_gecmis, columns=cols, show='headings')
        for col in cols: self.tree_gecmis.heading(col, text=col)
        self.tree_gecmis.pack(expand=True, fill="both", padx=10, pady=10)

        tk.Label(self.tab_gecmis, text="* Sistemde yapılan tüm ödünç alma ve iade işlemleri burada listelenir.", fg="blue").pack()
        self.listele_gecmis()

    def listele_al(self):
        # Treeview'i sıfırla; sonra veri modelindeki (Kitap nesneleri) duruma göre satır ekle.
        for i in self.tree_al.get_children(): self.tree_al.delete(i)
        for k in self.sistem.kitaplar:
            if k.durum == "Mevcut":
                self.tree_al.insert("", "end", values=(k.kitap_id, k.ad, k.yazar, k.kategori))

    def listele_yok(self):
        for i in self.tree_yok.get_children(): self.tree_yok.delete(i)
        for k in self.sistem.kitaplar:
            # Başkasında olan kitaplar; kendi listemizdekileri burada göstermiyoruz.
            if k.durum != "Mevcut" and k not in self.aktif_kullanici.odunc_alinan_kitaplar:
                sahip_adi = k.su_anki_sahibi.ad if k.su_anki_sahibi else "Bilinmiyor"
                # Aynı kitap için iade edilmemiş Odunc kaydından ödünç tarihini okuyoruz.
                aktif_odunc = next((o for o in self.sistem.oduncler if o.kitap == k and o.iade_tarihi is None), None)
                odunc_tarihi = aktif_odunc.odunc_tarihi if aktif_odunc else "-"
                self.tree_yok.insert("", "end", values=(k.kitap_id, k.ad, sahip_adi, odunc_tarihi))

    def listele_iade(self):
        for i in self.tree_iade.get_children(): self.tree_iade.delete(i)
        # Sadece giriş yapan üyenin (aktif_kullanici) elindeki kitaplar listelenir.
        for k in self.aktif_kullanici.odunc_alinan_kitaplar:
            aktif_odunc = next((o for o in self.sistem.oduncler if o.kitap == k and o.iade_tarihi is None), None)
            odunc_tarihi = aktif_odunc.odunc_tarihi if aktif_odunc else "-"
            self.tree_iade.insert("", "end", values=(k.kitap_id, k.ad, odunc_tarihi))

    def listele_gecmis(self):
        for i in self.tree_gecmis.get_children(): self.tree_gecmis.delete(i)
        # Her Odunc nesnesi bir satır: o.kitap.ad gibi nokta ile diğer nesnenin özelliğine ulaşıyoruz.
        for o in self.sistem.oduncler:
            iade_durumu = o.iade_tarihi if o.iade_tarihi else "Henüz İade Edilmedi"
            self.tree_gecmis.insert("", "end", values=(o.odunc_id, o.kitap.ad, o.uye.ad, o.odunc_tarihi, iade_durumu))

    def odunc_al_aksiyon(self):
        secili = self.tree_al.selection()
        girilen_tarih = self.odunc_tarih_giris.get().strip()

        if not secili:
            messagebox.showwarning("Uyarı", "Lütfen bir kitap seçin!")
            return

        if not girilen_tarih:
            messagebox.showwarning("Uyarı", "Lütfen bir ödünç alma tarihi girin!")
            return

        kitap_id = self.tree_al.item(secili)['values'][0]
        kitap = next(k for k in self.sistem.kitaplar if k.kitap_id == kitap_id)

        # Uye sınıfının metodu hem üyenin listesini hem kitabın durumunu günceller.
        self.aktif_kullanici.kitap_odunc_al(kitap)

        # Geçmiş için ayrıca Odunc nesnesi oluşturup kütüphane listesine ekliyoruz.
        yeni_odunc = Odunc(self.sistem.odunc_sayaci, kitap, self.aktif_kullanici, girilen_tarih)
        self.sistem.oduncler.append(yeni_odunc)
        self.sistem.odunc_sayaci += 1

        messagebox.showinfo("Başarılı", f"'{kitap.ad}' kitabını {girilen_tarih} tarihinde aldınız.")
        self.tum_listeleri_guncelle()

    def iade_et_aksiyon(self):
        secili = self.tree_iade.selection()
        girilen_tarih = self.iade_tarih_giris.get().strip()

        if not secili:
            messagebox.showwarning("Uyarı", "İade etmek için kitap seçin!")
            return

        if not girilen_tarih:
            messagebox.showwarning("Uyarı", "Lütfen bir iade tarihi girin!")
            return

        kitap_id = self.tree_iade.item(secili)['values'][0]
        kitap = next(k for k in self.aktif_kullanici.odunc_alinan_kitaplar if k.kitap_id == kitap_id)

        self.aktif_kullanici.kitap_iade_et(kitap)

        # İlgili Odunc kaydını bulup iade_tarihi alanını dolduruyoruz (nesne içinde kalıcı güncelleme).
        for odunc in self.sistem.oduncler:
            if odunc.kitap == kitap and odunc.iade_tarihi is None:
                odunc.iade_tarihi = girilen_tarih
                break

        messagebox.showinfo("Başarılı", f"Kitap {girilen_tarih} tarihinde iade edildi.")
        self.tum_listeleri_guncelle()

    def tum_listeleri_guncelle(self):
        # Veri değişince tüm tabloları yeniden çizeriz; tek yerden çağırmak kod tekrarını azaltır.
        self.listele_al()
        self.listele_yok()
        self.listele_iade()
        self.listele_gecmis()

    def temizle(self):
        # Ana pencerenin tüm alt bileşenlerini yok eder; böylece ekranlar arası geçiş temiz olur.
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    # Program doğrudan çalıştırıldığında: pencere oluştur, uygulama nesnesini bağla, olay döngüsünü başlat.
    root = tk.Tk()
    app = KutuphaneUygulamasi(root)
    root.mainloop()
