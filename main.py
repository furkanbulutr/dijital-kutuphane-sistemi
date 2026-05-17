import re
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from veri_uretici import kitaplari_uret, uyeleri_uret


# ─── Renk paleti ve tipografi ───────────────────────────────────────────────
class Tema:
    BG = "#f4f1ea"
    SURFACE = "#ffffff"
    SURFACE_ALT = "#faf8f4"
    HEADER = "#1e3a5f"
    HEADER_ACCENT = "#2d5a87"
    PRIMARY = "#1e3a5f"
    PRIMARY_HOVER = "#2d5a87"
    ACCENT = "#c9a227"
    ACCENT_LIGHT = "#f0e6c8"
    TEXT = "#1a202c"
    TEXT_MUTED = "#64748b"
    TEXT_ON_DARK = "#f8fafc"
    BORDER = "#e2ddd3"
    SUCCESS = "#2f855a"
    SUCCESS_BG = "#e6f4ec"
    WARNING = "#c05621"
    WARNING_BG = "#fef3e6"
    DANGER = "#c53030"
    DANGER_BG = "#fde8e8"
    ROW_ALT = "#f8f6f1"
    ROW_SELECT = "#dbeafe"
    FONT = "Segoe UI"
    FONT_MONO = "Consolas"


class Kitap:
    def __init__(self, kitap_id, ad, yazar, kategori):
        self.kitap_id = kitap_id
        self.ad = ad
        self.yazar = yazar
        self.kategori = kategori
        self.durum = "Mevcut"
        self.su_anki_sahibi = None

    def kitap_durumu_degistir(self, yeni_durum):
        self.durum = yeni_durum


class Uye:
    def __init__(self, uye_id, ad, email):
        self.uye_id = uye_id
        self.ad = ad
        self.email = email
        self.odunc_alinan_kitaplar = []

    def kitap_odunc_al(self, kitap):
        self.odunc_alinan_kitaplar.append(kitap)
        kitap.kitap_durumu_degistir("Ödünç Verildi")
        kitap.su_anki_sahibi = self

    def kitap_iade_et(self, kitap):
        if kitap in self.odunc_alinan_kitaplar:
            self.odunc_alinan_kitaplar.remove(kitap)
            kitap.kitap_durumu_degistir("Mevcut")
            kitap.su_anki_sahibi = None


class Odunc:
    def __init__(self, odunc_id, kitap, uye, odunc_tarihi):
        self.odunc_id = odunc_id
        self.kitap = kitap
        self.uye = uye
        self.odunc_tarihi = odunc_tarihi
        self.iade_tarihi = None


class Kutuphane:
    UYE_SAYISI = 55

    def __init__(self):
        self.kitaplar = []
        self.uyeler = []
        self.oduncler = []
        self.odunc_sayaci = 1
        self.verileri_yukle()

    def verileri_yukle(self):
        for kayit in kitaplari_uret():
            self.kitaplar.append(Kitap(*kayit))
        for kayit in uyeleri_uret(self.UYE_SAYISI):
            self.uyeler.append(Uye(*kayit))

    def sonraki_uye_id(self):
        if not self.uyeler:
            return 1
        return max(u.uye_id for u in self.uyeler) + 1

    def email_kullaniliyor(self, email):
        email = email.strip().lower()
        return any(u.email.lower() == email for u in self.uyeler)

    def uye_kaydet(self, ad, email):
        ad = ad.strip()
        email = email.strip().lower()

        if not ad:
            return None, "Lütfen ad soyad girin."
        if len(ad) < 2:
            return None, "Ad soyad en az 2 karakter olmalıdır."
        if not email:
            return None, "Lütfen e-posta adresi girin."
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            return None, "Geçerli bir e-posta adresi girin (ör. ad@ornek.com)."
        if self.email_kullaniliyor(email):
            return None, "Bu e-posta adresi zaten kayıtlı."

        yeni_id = self.sonraki_uye_id()
        uye = Uye(yeni_id, ad, email)
        self.uyeler.append(uye)
        return uye, None

    def uye_bul(self, uye_id):
        return next((u for u in self.uyeler if u.uye_id == uye_id), None)


class KutuphaneUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Dijital Kütüphane")
        self.root.geometry("1024x700")
        self.root.minsize(900, 620)
        self.root.configure(bg=Tema.BG)

        self.sistem = Kutuphane()
        self.aktif_kullanici = None
        self._arama_degiskenleri = {}

        self._stil_kur()
        self.giris_ekrani()

    # ─── Stil ve yardımcı bileşenler ─────────────────────────────────────────

    def _stil_kur(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(".", background=Tema.BG, font=(Tema.FONT, 10))
        style.configure("TFrame", background=Tema.BG)
        style.configure("Card.TFrame", background=Tema.SURFACE)
        style.configure("Header.TFrame", background=Tema.HEADER)
        style.configure("Surface.TFrame", background=Tema.SURFACE)

        style.configure(
            "Title.TLabel",
            font=(Tema.FONT, 22, "bold"),
            foreground=Tema.PRIMARY,
            background=Tema.BG,
        )
        style.configure(
            "Subtitle.TLabel",
            font=(Tema.FONT, 10),
            foreground=Tema.TEXT_MUTED,
            background=Tema.BG,
        )
        style.configure(
            "HeaderTitle.TLabel",
            font=(Tema.FONT, 16, "bold"),
            foreground=Tema.TEXT_ON_DARK,
            background=Tema.HEADER,
        )
        style.configure(
            "HeaderSub.TLabel",
            font=(Tema.FONT, 9),
            foreground="#94a3b8",
            background=Tema.HEADER,
        )
        style.configure(
            "Section.TLabel",
            font=(Tema.FONT, 11, "bold"),
            foreground=Tema.TEXT,
            background=Tema.SURFACE,
        )
        style.configure(
            "Hint.TLabel",
            font=(Tema.FONT, 9),
            foreground=Tema.TEXT_MUTED,
            background=Tema.SURFACE,
        )
        style.configure(
            "StatValue.TLabel",
            font=(Tema.FONT, 18, "bold"),
            foreground=Tema.PRIMARY,
            background=Tema.SURFACE,
        )
        style.configure(
            "StatLabel.TLabel",
            font=(Tema.FONT, 8),
            foreground=Tema.TEXT_MUTED,
            background=Tema.SURFACE,
        )
        style.configure(
            "Field.TLabel",
            font=(Tema.FONT, 9),
            foreground=Tema.TEXT,
            background=Tema.SURFACE,
        )

        style.configure(
            "Primary.TButton",
            font=(Tema.FONT, 10, "bold"),
            padding=(20, 10),
            background=Tema.PRIMARY,
            foreground=Tema.TEXT_ON_DARK,
            borderwidth=0,
        )
        style.map(
            "Primary.TButton",
            background=[("active", Tema.PRIMARY_HOVER), ("pressed", Tema.HEADER)],
        )

        style.configure(
            "Accent.TButton",
            font=(Tema.FONT, 10, "bold"),
            padding=(16, 8),
            background=Tema.ACCENT,
            foreground=Tema.TEXT,
            borderwidth=0,
        )
        style.map("Accent.TButton", background=[("active", "#b8921f")])

        style.configure(
            "Success.TButton",
            font=(Tema.FONT, 10, "bold"),
            padding=(16, 8),
            background=Tema.SUCCESS,
            foreground=Tema.TEXT_ON_DARK,
            borderwidth=0,
        )
        style.map("Success.TButton", background=[("active", "#276749")])

        style.configure(
            "Warning.TButton",
            font=(Tema.FONT, 10, "bold"),
            padding=(16, 8),
            background=Tema.WARNING,
            foreground=Tema.TEXT_ON_DARK,
            borderwidth=0,
        )
        style.map("Warning.TButton", background=[("active", "#9c4221")])

        style.configure(
            "Ghost.TButton",
            font=(Tema.FONT, 9),
            padding=(12, 6),
            background=Tema.HEADER_ACCENT,
            foreground=Tema.TEXT_ON_DARK,
            borderwidth=0,
        )
        style.map("Ghost.TButton", background=[("active", "#3d6a9e")])

        style.configure(
            "Danger.TButton",
            font=(Tema.FONT, 9),
            padding=(10, 6),
            background=Tema.DANGER,
            foreground=Tema.TEXT_ON_DARK,
            borderwidth=0,
        )
        style.map("Danger.TButton", background=[("active", "#9b2c2c")])

        style.configure(
            "TEntry",
            font=(Tema.FONT, 11),
            fieldbackground=Tema.SURFACE,
            bordercolor=Tema.BORDER,
            lightcolor=Tema.BORDER,
            darkcolor=Tema.BORDER,
            padding=8,
        )

        style.configure(
            "TNotebook",
            background=Tema.BG,
            borderwidth=0,
            tabmargins=[2, 6, 2, 0],
        )
        style.configure(
            "TNotebook.Tab",
            font=(Tema.FONT, 10),
            padding=[16, 10],
            background=Tema.SURFACE_ALT,
            foreground=Tema.TEXT_MUTED,
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", Tema.SURFACE)],
            foreground=[("selected", Tema.PRIMARY)],
            expand=[("selected", [1, 1, 1, 0])],
        )

        style.configure(
            "Modern.Treeview",
            font=(Tema.FONT, 10),
            rowheight=36,
            background=Tema.SURFACE,
            fieldbackground=Tema.SURFACE,
            foreground=Tema.TEXT,
            bordercolor=Tema.BORDER,
            relief="flat",
        )
        style.configure(
            "Modern.Treeview.Heading",
            font=(Tema.FONT, 9, "bold"),
            background=Tema.SURFACE_ALT,
            foreground=Tema.PRIMARY,
            relief="flat",
            padding=8,
        )
        style.map(
            "Modern.Treeview",
            background=[("selected", Tema.ROW_SELECT)],
            foreground=[("selected", Tema.TEXT)],
        )

    def _kart(self, parent, padding=20):
        outer = tk.Frame(parent, bg=Tema.BORDER, padx=1, pady=1)
        outer.pack(fill=tk.BOTH, expand=True)
        inner = ttk.Frame(outer, style="Card.TFrame", padding=padding)
        inner.pack(fill=tk.BOTH, expand=True)
        return inner

    def _tree_olustur(self, parent, cols, col_widths=None):
        frame = ttk.Frame(parent, style="Surface.TFrame")
        frame.pack(fill=tk.BOTH, expand=True, pady=(0, 12))

        tree = ttk.Treeview(
            frame,
            columns=cols,
            show="headings",
            style="Modern.Treeview",
            selectmode="browse",
        )
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)

        for i, col in enumerate(cols):
            tree.heading(col, text=col, anchor="w")
            w = (col_widths[i] if col_widths else 120)
            tree.column(col, width=w, minwidth=60, anchor="w")

        tree.tag_configure("odd", background=Tema.ROW_ALT)
        tree.tag_configure("even", background=Tema.SURFACE)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        return tree

    def _tree_doldur(self, tree, satirlar):
        for i in tree.get_children():
            tree.delete(i)
        for idx, row in enumerate(satirlar):
            tag = "odd" if idx % 2 else "even"
            tree.insert("", "end", values=row, tags=(tag,))

    def _aksiyon_cubugu(self, parent, tarih_etiketi, tarih_varsayilan, buton_metni, buton_stili, komut):
        bar = ttk.Frame(parent, style="Surface.TFrame")
        bar.pack(fill=tk.X, pady=(4, 0))

        sol = ttk.Frame(bar, style="Surface.TFrame")
        sol.pack(side=tk.LEFT)
        ttk.Label(sol, text=tarih_etiketi, style="Field.TLabel").pack(side=tk.LEFT, padx=(0, 8))
        entry = ttk.Entry(sol, width=14, font=(Tema.FONT, 10))
        entry.pack(side=tk.LEFT)
        entry.insert(0, tarih_varsayilan)

        ttk.Button(bar, text=buton_metni, style=buton_stili, command=komut).pack(
            side=tk.RIGHT, padx=4
        )
        return entry

    def _arama_kutusu(self, parent, placeholder, filtre_callback):
        var = tk.StringVar()
        self._arama_degiskenleri[placeholder] = var

        wrap = ttk.Frame(parent, style="Surface.TFrame")
        wrap.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(wrap, text="Ara", style="Field.TLabel").pack(side=tk.LEFT, padx=(0, 8))
        entry = ttk.Entry(wrap, textvariable=var, font=(Tema.FONT, 10))
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        def on_change(*_):
            filtre_callback(var.get().strip().lower())

        var.trace_add("write", on_change)
        return var

    def temizle(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ─── Giriş ekranı ────────────────────────────────────────────────────────

    def giris_ekrani(self):
        self.temizle()
        self.aktif_kullanici = None

        container = ttk.Frame(self.root, padding=40)
        container.pack(fill=tk.BOTH, expand=True)

        sol = ttk.Frame(container)
        sol.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 30))

        ttk.Label(sol, text="Dijital Kütüphane", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            sol,
            text="Kitaplarınızı keşfedin, ödünç alın ve iade edin — hepsi tek yerden.",
            style="Subtitle.TLabel",
            wraplength=420,
        ).pack(anchor="w", pady=(8, 24))

        ozellikler = [
            ("📚", "Geniş koleksiyon", f"{len(self.sistem.kitaplar)} benzersiz kitap"),
            ("🔄", "Kolay ödünç", "Tek tıkla ödünç alma ve iade"),
            ("📋", "İşlem geçmişi", "Tüm ödünç kayıtlarını takip edin"),
        ]
        for ikon, baslik, aciklama in ozellikler:
            satir = ttk.Frame(sol)
            satir.pack(anchor="w", pady=6)
            ttk.Label(satir, text=ikon, font=(Tema.FONT, 14), background=Tema.BG).pack(
                side=tk.LEFT, padx=(0, 12)
            )
            metin = ttk.Frame(satir)
            metin.pack(side=tk.LEFT)
            ttk.Label(
                metin, text=baslik, font=(Tema.FONT, 10, "bold"), foreground=Tema.TEXT, background=Tema.BG
            ).pack(anchor="w")
            ttk.Label(metin, text=aciklama, style="Subtitle.TLabel").pack(anchor="w")

        mevcut = sum(1 for k in self.sistem.kitaplar if k.durum == "Mevcut")
        ttk.Label(
            sol,
            text=(
                f"{len(self.sistem.kitaplar)} kitap · "
                f"{len(self.sistem.uyeler)} kayıtlı üye · "
                f"{mevcut} müsait"
            ),
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(30, 0))

        sag_wrap = tk.Frame(container, bg=Tema.BORDER, padx=1, pady=1)
        sag_wrap.pack(side=tk.RIGHT, fill=tk.Y)

        kart = ttk.Frame(sag_wrap, style="Card.TFrame", padding=24)
        kart.pack(fill=tk.BOTH)

        auth_tabs = ttk.Notebook(kart)
        auth_tabs.pack(fill=tk.BOTH, expand=True)

        tab_giris = ttk.Frame(auth_tabs, style="Card.TFrame", padding=8)
        tab_kayit = ttk.Frame(auth_tabs, style="Card.TFrame", padding=8)
        auth_tabs.add(tab_giris, text="  Giriş  ")
        auth_tabs.add(tab_kayit, text="  Kayıt Ol  ")

        ttk.Label(tab_giris, text="Üye kimliğinizle giriş", style="Section.TLabel").pack(
            anchor="w"
        )
        ttk.Label(
            tab_giris,
            text="Kayıt sonrası size verilen ID numarasını kullanın.",
            style="Hint.TLabel",
            wraplength=280,
        ).pack(anchor="w", pady=(4, 16))

        ttk.Label(tab_giris, text="Üye ID", style="Field.TLabel").pack(anchor="w")
        self.id_giris = ttk.Entry(tab_giris, width=28, font=(Tema.FONT, 12))
        self.id_giris.pack(fill=tk.X, pady=(6, 12))
        self.id_giris.insert(0, "1")
        self.id_giris.bind("<Return>", lambda e: self.login())

        ttk.Button(
            tab_giris, text="Giriş Yap →", style="Primary.TButton", command=self.login
        ).pack(fill=tk.X, pady=(0, 12))

        ttk.Label(tab_giris, text="Örnek üyeler", style="Hint.TLabel").pack(anchor="w", pady=(4, 6))
        for u in self.sistem.uyeler[:5]:
            satir_btn = tk.Frame(tab_giris, bg=Tema.SURFACE, cursor="hand2")
            satir_btn.pack(fill=tk.X, pady=2)
            satir_btn.bind("<Button-1>", lambda e, uid=u.uye_id: self._hizli_giris(uid))

            tk.Label(
                satir_btn,
                text=str(u.uye_id),
                font=(Tema.FONT, 9, "bold"),
                bg=Tema.ACCENT_LIGHT,
                fg=Tema.PRIMARY,
                width=3,
                padx=4,
                pady=4,
            ).pack(side=tk.LEFT, padx=(0, 8))
            tk.Label(
                satir_btn,
                text=u.ad,
                font=(Tema.FONT, 9),
                bg=Tema.SURFACE,
                fg=Tema.TEXT,
                anchor="w",
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
            for child in satir_btn.winfo_children():
                child.bind("<Button-1>", lambda e, uid=u.uye_id: self._hizli_giris(uid))

        kalan_uye = max(0, len(self.sistem.uyeler) - 5)
        if kalan_uye:
            ttk.Label(
                tab_giris,
                text=f"… ve {kalan_uye} üye daha",
                style="Hint.TLabel",
            ).pack(anchor="w", pady=(6, 0))

        ttk.Label(tab_kayit, text="Yeni üye kaydı", style="Section.TLabel").pack(anchor="w")
        ttk.Label(
            tab_kayit,
            text="Kayıt sonrası üye ID'niz otomatik atanır ve size gösterilir.",
            style="Hint.TLabel",
            wraplength=280,
        ).pack(anchor="w", pady=(4, 16))

        ttk.Label(tab_kayit, text="Ad Soyad", style="Field.TLabel").pack(anchor="w")
        self.kayit_ad = ttk.Entry(tab_kayit, width=28, font=(Tema.FONT, 11))
        self.kayit_ad.pack(fill=tk.X, pady=(6, 12))

        ttk.Label(tab_kayit, text="E-posta", style="Field.TLabel").pack(anchor="w")
        self.kayit_email = ttk.Entry(tab_kayit, width=28, font=(Tema.FONT, 11))
        self.kayit_email.pack(fill=tk.X, pady=(6, 16))
        self.kayit_email.bind("<Return>", lambda e: self.kayit_ol())

        ttk.Button(
            tab_kayit, text="Kayıt Ol", style="Accent.TButton", command=self.kayit_ol
        ).pack(fill=tk.X)

        sonraki = self.sistem.sonraki_uye_id()
        ttk.Label(
            tab_kayit,
            text=f"Sıradaki üye ID: {sonraki}",
            style="Hint.TLabel",
        ).pack(anchor="w", pady=(12, 0))

    def _hizli_giris(self, uye_id):
        self.id_giris.delete(0, tk.END)
        self.id_giris.insert(0, str(uye_id))
        self.login()

    def login(self):
        try:
            girilen_id = int(self.id_giris.get().strip())
            uye = self.sistem.uye_bul(girilen_id)
            if uye:
                self.aktif_kullanici = uye
                self.ana_panel()
            else:
                messagebox.showerror(
                    "Hata",
                    f"ID {girilen_id} ile kayıtlı üye bulunamadı.\n"
                    "Kayıt olduysanız size verilen numarayı kullanın.",
                )
        except ValueError:
            messagebox.showerror("Hata", "Lütfen sayısal bir üye ID girin.")

    def kayit_ol(self):
        ad = self.kayit_ad.get()
        email = self.kayit_email.get()
        uye, hata = self.sistem.uye_kaydet(ad, email)

        if hata:
            messagebox.showerror("Kayıt başarısız", hata)
            return

        messagebox.showinfo(
            "Kayıt başarılı",
            f"Hoş geldiniz, {uye.ad}!\n\n"
            f"Üye ID'niz: {uye.uye_id}\n"
            f"E-posta: {uye.email}\n\n"
            "Bu ID ile giriş yapabilirsiniz. Şimdi otomatik giriş yapılıyor.",
        )
        self.aktif_kullanici = uye
        self.ana_panel()

    # ─── Ana panel ───────────────────────────────────────────────────────────

    def ana_panel(self):
        self.temizle()

        header = tk.Frame(self.root, bg=Tema.HEADER, height=72)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        h_inner = tk.Frame(header, bg=Tema.HEADER)
        h_inner.pack(fill=tk.BOTH, expand=True, padx=24, pady=12)

        logo = tk.Label(
            h_inner,
            text="📖",
            font=(Tema.FONT, 20),
            bg=Tema.HEADER,
            fg=Tema.ACCENT,
        )
        logo.pack(side=tk.LEFT, padx=(0, 12))

        baslik_wrap = tk.Frame(h_inner, bg=Tema.HEADER)
        baslik_wrap.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(
            baslik_wrap,
            text="Dijital Kütüphane",
            font=(Tema.FONT, 14, "bold"),
            bg=Tema.HEADER,
            fg=Tema.TEXT_ON_DARK,
        ).pack(anchor="w")
        tk.Label(
            baslik_wrap,
            text=f"{self.aktif_kullanici.ad}  ·  {self.aktif_kullanici.email}",
            font=(Tema.FONT, 9),
            bg=Tema.HEADER,
            fg="#94a3b8",
        ).pack(anchor="w")

        tk.Button(
            h_inner,
            text="  Güvenli Çıkış  ",
            font=(Tema.FONT, 9),
            bg=Tema.HEADER_ACCENT,
            fg=Tema.TEXT_ON_DARK,
            activebackground="#3d6a9e",
            activeforeground=Tema.TEXT_ON_DARK,
            relief="flat",
            cursor="hand2",
            command=self.giris_ekrani,
        ).pack(side=tk.RIGHT)

        stats_bar = ttk.Frame(self.root, padding=(24, 12, 24, 0))
        stats_bar.pack(fill=tk.X)

        mevcut = sum(1 for k in self.sistem.kitaplar if k.durum == "Mevcut")
        oduncte = sum(1 for k in self.sistem.kitaplar if k.durum != "Mevcut")
        benim = len(self.aktif_kullanici.odunc_alinan_kitaplar)

        for deger, etiket, renk in [
            (str(mevcut), "Müsait kitap", Tema.SUCCESS),
            (str(oduncte), "Ödünçte", Tema.WARNING),
            (str(benim), "Elinizde", Tema.PRIMARY),
            (str(len(self.sistem.oduncler)), "Toplam işlem", Tema.TEXT_MUTED),
        ]:
            self._istatistik_karti(stats_bar, deger, etiket, renk)

        content = ttk.Frame(self.root, padding=(24, 12, 24, 24))
        content.pack(fill=tk.BOTH, expand=True)

        self.tabs = ttk.Notebook(content)
        self.tabs.pack(fill=tk.BOTH, expand=True)

        self.tab_al = ttk.Frame(self.tabs, style="Surface.TFrame", padding=16)
        self.tabs.add(self.tab_al, text="  Ödünç Al  ")
        self.kitap_al_sayfasi()

        self.tab_yok = ttk.Frame(self.tabs, style="Surface.TFrame", padding=16)
        self.tabs.add(self.tab_yok, text="  Başkasında  ")
        self.kitap_yok_sayfasi()

        self.tab_iade = ttk.Frame(self.tabs, style="Surface.TFrame", padding=16)
        self.tabs.add(self.tab_iade, text="  Kitaplarım  ")
        self.kitap_iade_sayfasi()

        self.tab_gecmis = ttk.Frame(self.tabs, style="Surface.TFrame", padding=16)
        self.tabs.add(self.tab_gecmis, text="  Geçmiş  ")
        self.islem_gecmisi_sayfasi()

    def _istatistik_karti(self, parent, deger, etiket, renk):
        wrap = tk.Frame(parent, bg=Tema.BORDER, padx=1, pady=1)
        wrap.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        kart = tk.Frame(wrap, bg=Tema.SURFACE, padx=16, pady=12)
        kart.pack(fill=tk.BOTH, expand=True)
        tk.Label(kart, text=deger, font=(Tema.FONT, 20, "bold"), fg=renk, bg=Tema.SURFACE).pack(
            anchor="w"
        )
        tk.Label(
            kart, text=etiket, font=(Tema.FONT, 8), fg=Tema.TEXT_MUTED, bg=Tema.SURFACE
        ).pack(anchor="w")

    # ─── Sekmeler ────────────────────────────────────────────────────────────

    def kitap_al_sayfasi(self):
        ttk.Label(
            self.tab_al,
            text="Ödünç alınabilir kitaplar",
            style="Section.TLabel",
        ).pack(anchor="w")
        ttk.Label(
            self.tab_al,
            text="Listeden bir kitap seçin, tarihi kontrol edin ve ödünç alın.",
            style="Hint.TLabel",
        ).pack(anchor="w", pady=(2, 12))

        cols = ("ID", "Kitap Adı", "Yazar", "Kategori")
        self.tree_al = self._tree_olustur(
            self.tab_al, cols, [60, 220, 160, 140]
        )
        self._al_tum_satirlar = []
        self._arama_kutusu(self.tab_al, "al", self._filtre_al)

        self.odunc_tarih_giris = self._aksiyon_cubugu(
            self.tab_al,
            "Ödünç alma tarihi",
            datetime.now().strftime("%d.%m.%Y"),
            "Seçili Kitabı Ödünç Al",
            "Success.TButton",
            self.odunc_al_aksiyon,
        )
        self.listele_al()

    def _filtre_al(self, arama):
        if not arama:
            self._tree_doldur(self.tree_al, self._al_tum_satirlar)
            return
        filtreli = [
            r
            for r in self._al_tum_satirlar
            if any(arama in str(c).lower() for c in r)
        ]
        self._tree_doldur(self.tree_al, filtreli)

    def kitap_yok_sayfasi(self):
        ttk.Label(
            self.tab_yok,
            text="Başka üyelerde olan kitaplar",
            style="Section.TLabel",
        ).pack(anchor="w")
        ttk.Label(
            self.tab_yok,
            text="Şu an kütüphanede bulunmayan, ödünç verilmiş kitapların listesi.",
            style="Hint.TLabel",
        ).pack(anchor="w", pady=(2, 12))

        cols = ("ID", "Kitap Adı", "Şu An Kimde?", "Ödünç Tarihi")
        self.tree_yok = self._tree_olustur(
            self.tab_yok, cols, [60, 240, 140, 120]
        )

        uyari = tk.Frame(self.tab_yok, bg=Tema.WARNING_BG, padx=12, pady=8)
        uyari.pack(fill=tk.X, pady=(0, 8))
        tk.Label(
            uyari,
            text="Bu kitaplar başka üyeler tarafından ödünç alınmıştır.",
            font=(Tema.FONT, 9),
            bg=Tema.WARNING_BG,
            fg=Tema.WARNING,
        ).pack(anchor="w")

        self.listele_yok()

    def kitap_iade_sayfasi(self):
        ttk.Label(
            self.tab_iade,
            text="Elinizdeki kitaplar",
            style="Section.TLabel",
        ).pack(anchor="w")
        ttk.Label(
            self.tab_iade,
            text="İade etmek istediğiniz kitabı seçin ve iade tarihini girin.",
            style="Hint.TLabel",
        ).pack(anchor="w", pady=(2, 12))

        cols = ("ID", "Kitap Adı", "Ödünç Alma Tarihi")
        self.tree_iade = self._tree_olustur(
            self.tab_iade, cols, [60, 280, 140]
        )

        self.iade_tarih_giris = self._aksiyon_cubugu(
            self.tab_iade,
            "İade tarihi",
            datetime.now().strftime("%d.%m.%Y"),
            "Seçili Kitabı İade Et",
            "Warning.TButton",
            self.iade_et_aksiyon,
        )
        self.listele_iade()

    def islem_gecmisi_sayfasi(self):
        ttk.Label(
            self.tab_gecmis,
            text="Tüm işlem geçmişi",
            style="Section.TLabel",
        ).pack(anchor="w")
        ttk.Label(
            self.tab_gecmis,
            text="Sistemde kayıtlı tüm ödünç alma ve iade işlemleri.",
            style="Hint.TLabel",
        ).pack(anchor="w", pady=(2, 12))

        cols = ("İşlem ID", "Kitap", "Üye", "Ödünç", "İade")
        self.tree_gecmis = self._tree_olustur(
            self.tab_gecmis, cols, [70, 200, 100, 100, 120]
        )

        bilgi = tk.Frame(self.tab_gecmis, bg=Tema.SUCCESS_BG, padx=12, pady=8)
        bilgi.pack(fill=tk.X, pady=(0, 8))
        tk.Label(
            bilgi,
            text="Henüz iade edilmemiş kayıtlar «Henüz İade Edilmedi» olarak görünür.",
            font=(Tema.FONT, 9),
            bg=Tema.SUCCESS_BG,
            fg=Tema.SUCCESS,
        ).pack(anchor="w")

        self.listele_gecmis()

    # ─── Listeleme ───────────────────────────────────────────────────────────

    def listele_al(self):
        self._al_tum_satirlar = [
            (k.kitap_id, k.ad, k.yazar, k.kategori)
            for k in self.sistem.kitaplar
            if k.durum == "Mevcut"
        ]
        arama = ""
        if hasattr(self, "_arama_degiskenleri"):
            var = self._arama_degiskenleri.get("al")
            if var:
                arama = var.get().strip().lower()
        if arama:
            self._filtre_al(arama)
        else:
            self._tree_doldur(self.tree_al, self._al_tum_satirlar)

    def listele_yok(self):
        satirlar = []
        for k in self.sistem.kitaplar:
            if k.durum != "Mevcut" and k not in self.aktif_kullanici.odunc_alinan_kitaplar:
                sahip_adi = k.su_anki_sahibi.ad if k.su_anki_sahibi else "Bilinmiyor"
                aktif_odunc = next(
                    (o for o in self.sistem.oduncler if o.kitap == k and o.iade_tarihi is None),
                    None,
                )
                odunc_tarihi = aktif_odunc.odunc_tarihi if aktif_odunc else "—"
                satirlar.append((k.kitap_id, k.ad, sahip_adi, odunc_tarihi))
        self._tree_doldur(self.tree_yok, satirlar)

    def listele_iade(self):
        satirlar = []
        for k in self.aktif_kullanici.odunc_alinan_kitaplar:
            aktif_odunc = next(
                (o for o in self.sistem.oduncler if o.kitap == k and o.iade_tarihi is None),
                None,
            )
            odunc_tarihi = aktif_odunc.odunc_tarihi if aktif_odunc else "—"
            satirlar.append((k.kitap_id, k.ad, odunc_tarihi))
        self._tree_doldur(self.tree_iade, satirlar)

    def listele_gecmis(self):
        satirlar = []
        for o in self.sistem.oduncler:
            iade = o.iade_tarihi if o.iade_tarihi else "Henüz İade Edilmedi"
            satirlar.append((o.odunc_id, o.kitap.ad, o.uye.ad, o.odunc_tarihi, iade))
        self._tree_doldur(self.tree_gecmis, satirlar)

    # ─── İşlemler ────────────────────────────────────────────────────────────

    def odunc_al_aksiyon(self):
        secili = self.tree_al.selection()
        girilen_tarih = self.odunc_tarih_giris.get().strip()

        if not secili:
            messagebox.showwarning("Uyarı", "Lütfen listeden bir kitap seçin.")
            return
        if not girilen_tarih:
            messagebox.showwarning("Uyarı", "Lütfen bir ödünç alma tarihi girin.")
            return

        kitap_id = self.tree_al.item(secili)["values"][0]
        kitap = next(k for k in self.sistem.kitaplar if k.kitap_id == kitap_id)

        self.aktif_kullanici.kitap_odunc_al(kitap)
        yeni_odunc = Odunc(
            self.sistem.odunc_sayaci, kitap, self.aktif_kullanici, girilen_tarih
        )
        self.sistem.oduncler.append(yeni_odunc)
        self.sistem.odunc_sayaci += 1

        messagebox.showinfo(
            "Başarılı",
            f"«{kitap.ad}» kitabını {girilen_tarih} tarihinde ödünç aldınız.",
        )
        self.ana_panel()
        self.tabs.select(self.tab_iade)

    def iade_et_aksiyon(self):
        secili = self.tree_iade.selection()
        girilen_tarih = self.iade_tarih_giris.get().strip()

        if not secili:
            messagebox.showwarning("Uyarı", "İade etmek için listeden bir kitap seçin.")
            return
        if not girilen_tarih:
            messagebox.showwarning("Uyarı", "Lütfen bir iade tarihi girin.")
            return

        kitap_id = self.tree_iade.item(secili)["values"][0]
        kitap = next(
            k for k in self.aktif_kullanici.odunc_alinan_kitaplar if k.kitap_id == kitap_id
        )

        self.aktif_kullanici.kitap_iade_et(kitap)
        for odunc in self.sistem.oduncler:
            if odunc.kitap == kitap and odunc.iade_tarihi is None:
                odunc.iade_tarihi = girilen_tarih
                break

        messagebox.showinfo(
            "Başarılı", f"«{kitap.ad}» {girilen_tarih} tarihinde iade edildi."
        )
        self.ana_panel()
        self.tabs.select(self.tab_al)

    def tum_listeleri_guncelle(self):
        self.listele_al()
        self.listele_yok()
        self.listele_iade()
        self.listele_gecmis()


if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.iconbitmap(default="")
    except tk.TclError:
        pass
    app = KutuphaneUygulamasi(root)
    root.mainloop()
