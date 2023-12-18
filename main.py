import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3
import datetime
from abc import ABC, abstractmethod
class Araba(ABC):
    def __init__(self, marka, model, yil):
        self.id = None
        self.marka = marka
        self.model = model
        self._yil = yil  # Protected özellik
        self.__kilometre = 0  # Private özellik

    def get_yil(self):
        return self._yil

    def set_kilometre(self, km):
        if km >= 0:
            self.__kilometre = km
        else:
            print("Geçersiz kilometre değeri.")

    def get_kilometre(self):
        return self.__kilometre

    @abstractmethod
    def bakim(self):
        pass

class ElektrikliAraba(Araba):
    def __init__(self, marka, model, yil, batarya_durumu):
        super().__init__(marka, model, yil)
        self.batarya_durumu = batarya_durumu

    def bakim(self):
        return f"{self.marka} {self.model} elektrikli araba bakımı: Pil sağlığı kontrol ediliyor. Batarya Durumu: {self.batarya_durumu}"

class BenzinliAraba(Araba):
    def __init__(self, marka, model, yil, yakit_durumu):
        super().__init__(marka, model, yil)
        self.yakit_durumu = yakit_durumu

    def bakim(self):
        return f"{self.marka} {self.model} benzinli araba bakımı: Yağ değiştiriliyor. Yakıt Durumu: {self.yakit_durumu}"
class Kiralama:
    def __init__(self, musteri, araba, kiralama_tipi, sure):
        self.musteri = musteri
        self.araba = araba
        self.kiralama_tipi = kiralama_tipi
        self.sure = sure

    def hesapla_ucret(self):
        if self.kiralama_tipi == "günlük":
            return self.sure * 1000
        elif self.kiralama_tipi == "saatlik":
            return self.sure * 500
        else:
            print("Geçersiz kiralama tipi")
            return -1


class AracKiralamaUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Araç Kiralama Uygulaması")

        self.create_database_connection()

        self.create_main_frame()

    def create_database_connection(self):
        self.baglanti = sqlite3.connect("rent-a.db")
        self.cursor = self.baglanti.cursor()

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.label_welcome = ttk.Label(self.main_frame, text="Araç Kiralama Uygulamasına Hoş Geldiniz!", font=('Arial', 16, 'bold', "italic"))
        self.label_welcome.grid(row=0, column=0, columnspan=3, pady=20)

        self.label_instruction = ttk.Label(self.main_frame, text="Adınız Soyadınız:", font=('Arial', 12))
        self.label_instruction.grid(row=1, column=0, columnspan=3, pady=10)

        self.entry_ad_soyad = ttk.Entry(self.main_frame, font=('Arial', 12))
        self.entry_ad_soyad.grid(row=2, column=0, columnspan=3, pady=10)

        # Giriş yap butonu ve stili
        self.button_giris = tk.Button(self.main_frame, text="Giriş Yap", command=self.musteri_giris,
                                      width=10, height=1, bg="purple", fg="white", font=("Arial", 12))
        self.button_giris.grid(row=3, column=0, columnspan=3, pady=20)

    def musteri_giris(self):
        ad_soyad = self.entry_ad_soyad.get()

        if not ad_soyad:
            messagebox.showwarning("Uyarı", "Lütfen adınızı ve soyadınızı girin.")
            return

        musteri_id = self.add_musteri(ad_soyad)
        if musteri_id:
            self.musteri_id = musteri_id
            self.label_welcome.config(text=f"Hoş Geldin, {ad_soyad}!")
            self.label_instruction.grid_remove()
            self.entry_ad_soyad.grid_remove()
            self.button_giris.grid_remove()

            self.show_arac_list()

    def add_musteri(self, ad_soyad):
        self.cursor.execute("INSERT INTO musteri (ad_soyad) VALUES (?)", (ad_soyad,))
        self.baglanti.commit()
        return self.cursor.lastrowid

    def show_arac_list(self):
        araclar = self.get_arac_list()

        self.tree_araclar = ttk.Treeview(self.main_frame, columns=("id", "Marka", "Model", "Yıl", "Tip", "Durum"), show="headings")
        self.tree_araclar.heading("id", text="id")
        self.tree_araclar.heading("Marka", text="Marka")
        self.tree_araclar.heading("Model", text="Model")
        self.tree_araclar.heading("Yıl", text="Yıl")
        self.tree_araclar.heading("Tip", text="Tip")
        self.tree_araclar.heading("Durum", text="Durum")

        for arac in araclar:
            self.tree_araclar.insert("", "end", values=arac)

        self.tree_araclar.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E))

        self.button_kirala = ttk.Button(self.main_frame, text="Araç Kirala", command=self.arac_kirala)
        self.button_kirala.grid(row=2, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))

    def get_arac_list(self):
        self.cursor.execute(
            "SELECT arabalar.id, marka, model, yil, tip, durumu FROM arabalar WHERE durumu IN ('müsait', 'kiralandı')")
        return self.cursor.fetchall()

    def arac_kirala(self):
        selected_item = self.tree_araclar.selection()
        if selected_item:
            arac_id = self.tree_araclar.item(selected_item, "values")[0]
            arac_durumu = self.tree_araclar.item(selected_item, "values")[5]                                        # Assuming status column is the sixth index

            if arac_durumu == 'kiralandı':
                messagebox.showwarning("Uyarı", "Bu araç zaten kiralanmış!")
                return

            kiralama_tipi = self.show_kiralama_tipi_dialog()
            if kiralama_tipi:
                sure = self.show_kiralama_sure_dialog(kiralama_tipi)

                if sure:
                    arac = self.get_arac_by_id(arac_id)

                    # Aracın bakım durumu GUI'de gösteriliyor
                    self.show_arac_bakim_durumu(arac)

                    # Aracın durumunu güncelle
                    self.update_arac_durumu(arac_id)

                    # Kiralama bilgilerini veritabanına ekle
                    kiralama = Kiralama(self.musteri_id, arac, kiralama_tipi, sure)
                    self.add_kiralama_bilgisi(kiralama)

                    ucret = kiralama.hesapla_ucret()
                    if ucret != -1:
                        messagebox.showinfo("Başarılı", f"Araç kiralandı! Ücret: {ucret} TL")
                        self.root.destroy()

    def update_arac_durumu(self, arac_id):
        self.cursor.execute("UPDATE arabalar SET durumu = 'kiralandı' WHERE id = ?", (arac_id,))
        self.baglanti.commit()

    def add_kiralama_bilgisi(self, kiralama):
        ucret = kiralama.hesapla_ucret()  # Calculate the rental fee

        self.cursor.execute(
            "INSERT INTO kiralama (musteri_id, araba_id, kiralama_tipi, sure, ucret, durumu) VALUES ( ?, ?, ?, ?, ?, ?)",
            (kiralama.musteri, kiralama.araba.id, kiralama.kiralama_tipi, kiralama.sure, ucret, 'kiralandı'))
        self.baglanti.commit()

    def show_arac_bakim_durumu(self, arac):
        bakim_durumu = arac.bakim()
        messagebox.showinfo("Bakım Durumu", bakim_durumu)

    def show_kiralama_tipi_dialog(self):
        while True:
            kiralama_tipi = simpledialog.askstring("Kiralama Tipi", "Kiralama Tipini Seçiniz (günlük/saatlik)")

            if kiralama_tipi is None:
                return None  # Eğer kullanıcı iptal ederse

            kiralama_tipi_lower = kiralama_tipi.lower()
            if kiralama_tipi_lower not in ["günlük", "saatlik"]:
                messagebox.showwarning("Uyarı", "Lütfen 'günlük' veya 'saatlik' olarak girin.")
            else:
                return kiralama_tipi_lower

    def show_kiralama_sure_dialog(self, kiralama_tip):
        while True:
            if kiralama_tip == "günlük":
                message = "Günlük Kiralama Süresini Giriniz (gün)"
            elif kiralama_tip == "saatlik":
                message = "Saatlik Kiralama Süresini Giriniz (saat)"

            kiralama_suresi = simpledialog.askinteger("Kiralama Süresi", message)

            if kiralama_suresi is None:
                return None  # Eğer kullanıcı iptal ederse

            if kiralama_suresi <= 0:
                messagebox.showwarning("Uyarı", "Lütfen pozitif bir değer girin.")
            else:
                return kiralama_suresi

    def get_arac_by_id(self, arac_id):
        self.cursor.execute("SELECT * FROM arabalar WHERE id = ?", (arac_id,))
        arac_data = self.cursor.fetchone()

        if arac_data:
            arac_id, marka, model, yil, tip, durumu,kilometre = arac_data
            if tip == 'Elektrikli':
                elektrikli_arac = ElektrikliAraba(marka, model, yil, batarya_durumu="Yüksek")
                elektrikli_arac.id = arac_id  # Set the id attribute
                return elektrikli_arac
            elif tip == 'Benzinli':
                benzinli_arac = BenzinliAraba(marka, model, yil, yakit_durumu="Doluluk Oranı: %100")
                benzinli_arac.id = arac_id  # Set the id attribute
                return benzinli_arac
        else:
            return None


if __name__ == "__main__":
    root = tk.Tk()
    app = AracKiralamaUygulamasi(root)
    root.mainloop()
