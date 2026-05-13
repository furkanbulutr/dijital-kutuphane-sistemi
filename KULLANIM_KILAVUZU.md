# Dijital Kütüphane Sistemi — Kullanım Kılavuzu

Bu belge, masaüstü uygulamasının nasıl çalıştırılacağını ve ekranların nasıl kullanılacağını anlatır.

## Program nedir?

**Dijital Kütüphane Sistemi**, örnek kitap ve üye verileriyle çalışan bir **ödünç alma / iade** simülasyonudur. Grafik arayüz **Python** ve **Tkinter** ile yazılmıştır; kitapları listeleyebilir, ödünç alabilir, iade edebilir ve işlem geçmişini görebilirsiniz.

## Gereksinimler

- **Python 3** (bilgisayarınızda yüklü olmalıdır).
- **Tkinter**: Çoğu resmi Python kurulumunda birlikte gelir. Eksikse işletim sisteminize göre `python3-tk` benzeri bir paket kurmanız gerekebilir.

## Programı nasıl çalıştırırım?

1. Proje klasörüne gidin (`dijital_kutuphane`).
2. Terminal veya Komut İstemi’nde şu komutu çalıştırın:

```bash
python main.py
```

Python komutunuz `python3` ise:

```bash
python3 main.py
```

Pencere açıldığında önce **giriş ekranını** görürsünüz.

## Önemli not: Verilerin saklanması

Uygulama şu an **bellek içinde** çalışır; kitaplar ve işlemler **dosyaya kaydedilmez**. Programı kapattığınızda yaptığınız ödünç alma ve iadeler sıfırlanır; bir sonraki açılışta yine örnek kitaplar ve üç üye ile başlarsınız.

---

## 1. Giriş ekranı

- **Üye ID**: Sistemde tanımlı üyelerin kimlik numaraları **1**, **2** ve **3** şeklindedir.
  - **1** — Furkan  
  - **2** — Ayşe  
  - **3** — Mehmet  
- Kutuya sayı yazıp **Giriş Yap** düğmesine basın.
- Geçersiz ID veya sayı olmayan bir girişte program uyarı veya hata mesajı gösterir.

**Güvenli Çıkış**: Ana ekrandan çıkıp tekrar giriş ekranına dönmek için üst barda bu düğmeyi kullanın.

---

## 2. Ana panel ve sekmeler

Giriş yaptıktan sonra üstte **aktif kullanıcı adınız**, altta ise **sekmeler** görünür. Her sekme farklı bir işe yarar.

### Sekme: Kitap Ödünç Al

- Listede yalnızca **kütüphanede bulunan** (henüz kimseye verilmemiş) kitaplar görünür.
- Tabloda bir satıra tıklayarak kitabı **seçin**.
- **Ödünç Alma Tarihi** alanına tarih yazın (varsayılan olarak bugünün tarihi doldurulabilir).
- **Seçili Kitabı Ödünç Al** düğmesine basın.
- Başarılı olursa bilgi penceresi açılır; listeler güncellenir.

**Dikkat**: Önce satır seçmeden düğmeye basarsanız uyarı alırsınız. Tarih boş bırakılamaz.

### Sekme: Kütüphanede Olmayanlar

- Başka bir üye tarafından ödünç alınmış kitaplar burada listelenir.
- **Şu An Kimde?** sütunu kitabın elinde olduğu üyeyi gösterir.
- **Ödünç Alındığı Tarih**, o işlem için girilen ödünç tarihini gösterir (kayıt yoksa tire olabilir).
- Kendi aldığınız kitaplar bu sekmede **sizin için** gösterilmez; onlar **Eldeki Kitaplarım** sekmesindedir.

### Sekme: Eldeki Kitaplarım

- Giriş yaptığınız üyenin **şu an ödünçte tuttuğu** kitaplar listelenir.
- İade etmek istediğiniz kitabı seçin.
- **İade Edilme Tarihi** alanını doldurun.
- **Seçili Kitabı İade Et** düğmesine basın.

İade sonrası kitap tekrar **kütüphanede mevcut** sayılır ve başka kullanıcılar ödünç alabilir.

### Sekme: Tüm İşlem Geçmişi

- Yapılan **tüm ödünç işlemleri** (hangi kitap, hangi üye, ödünç ve varsa iade tarihi) burada toplanır.
- Henüz iade edilmemiş kayıtlarda iade sütunu **Henüz İade Edilmedi** şeklinde görünebilir.

---

## 3. Sık karşılaşılan durumlar

| Durum | Ne yapmalıyım? |
|--------|----------------|
| “Lütfen bir kitap seçin” | Tabloda bir satıra tıklayıp satırı vurgulayın, sonra işlem düğmesine basın. |
| “Bu ID ile kayıtlı üye bulunamadı” | Sadece **1**, **2** veya **3** kullanın. |
| “Sayısal ID girin” | ID kutusuna harf yerine rakam yazın. |
| Kitap listede yok | Ya başkasında ya da zaten sizde olabilir; diğer sekmelere bakın. |

---

## 4. Örnek kitaplar (başlangıç)

Program açıldığında örnek olarak şu kitaplar yüklenir (ID’ler sabittir): Python Programlama, Veri Yapıları, Nutuk, Suç ve Ceza, Küçük Prens, 1984. Yeni kitap eklemek için `main.py` içindeki veri yükleme bölümünü kod üzerinden değiştirmeniz gerekir.

---

## 5. Sorun giderme

- **Pencere açılmıyor**: Python sürümünüzü kontrol edin (`python --version`). Tkinter hatası alıyorsanız Python kurulumunuzda Tk desteğini etkinleştirin veya işletim sisteminize uygun Tk paketini kurun.
- **Komut bulunamadı**: `py main.py` (Windows) veya tam yol ile Python çağırmayı deneyin.

---

Bu kılavuz, proje klasöründeki `main.py` dosyasındaki mevcut davranışa göre hazırlanmıştır. Özellik ekledikçe bu dosyayı da güncellemeniz iyi olur.
