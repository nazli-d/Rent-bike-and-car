import datetime
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


class AracKiralama:
    def __init__(self, arac_tipi):
        self.arac_tipi = arac_tipi
        self.conn = sqlite3.connect('kiralama-1.db')
        self.cursor = self.conn.cursor()

    def kiralamaEkle(self, arac_id, kiralama_tipi):
        kiralama_zamani = datetime.datetime.now().strftime('%H:%M %d-%m-%Y ')
        self.cursor.execute(
            "INSERT INTO kiralama (arac_id, arac_tipi, kiralama_tipi, kiralama_zamani) VALUES (?, ?, ?, ?)",
            (arac_id, self.arac_tipi, kiralama_tipi, kiralama_zamani)
        )
        self.conn.commit()

        # Aracı kiralandı olarak işaretle
        self.cursor.execute(f"UPDATE {self.arac_tipi} SET durumu='kiralandı' WHERE {self.arac_tipi}_id=?", (arac_id,))
        self.conn.commit()

        message = f"{self.arac_tipi.capitalize()} ID={arac_id} {kiralama_tipi} olarak kiralandı."
        self.show_message("Başarılı", message)

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def stokGoster(self):
        stock_window = tk.Toplevel(self.root)
        stock_window.title(f"{self.arac_tipi.capitalize()} Stok Gösterimi")
        stock_window.geometry("500x300")

        label_frame = tk.LabelFrame(stock_window, text="", font=("Arial", 12, "bold"))
        label_frame.pack(pady=20)

        columns = ("ID", "Durumu")
        tree = ttk.Treeview(label_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack()

        self.cursor.execute(f"SELECT {self.arac_tipi}_id, durumu FROM {self.arac_tipi}")
        result = self.cursor.fetchall()

        if result:
            for row in result:
                tree.insert("", "end", values=(row[0], row[1]))

    def saatlikKiralama(self, arac_id):
        if arac_id is None:
            return None
        else:
            self.cursor.execute("SELECT durumu FROM bisiklet WHERE bisiklet_id=?", (arac_id,))
            result = self.cursor.fetchone()

            print(f"Bisiklet ID={arac_id} saatlik olarak kiralandı.")
            self.kiralamaEkle(arac_id, 'saatlik')
            self.conn.commit()  # Bisiklet arac tipi olarak düzelt


    def gunlukKiralama(self, arac_id):
        if arac_id is None:
            return None
        else:
            self.suan = datetime.datetime.now()
            iade_tarihi = self.suan + datetime.timedelta(days=1)
            iade_tarihi = iade_tarihi.strftime("%d-%m-%Y")
            self.cursor.execute(
                f"SELECT {self.arac_tipi}_id FROM {self.arac_tipi} WHERE durumu='müsait' AND {self.arac_tipi}_id=? LIMIT 1",
                (arac_id,))
            result = self.cursor.fetchone()

            print(f"{self.arac_tipi.capitalize()} ID={arac_id} günlük olarak kiralandı.")
            self.kiralamaEkle(arac_id, 'gunluk')
            self.conn.commit()

    def haftalikKiralama(self, arac_id):
        if arac_id is None:
            return None
        else:
            self.suan = datetime.datetime.now()
            iade_tarihi = self.suan + datetime.timedelta(days=7)
            iade_tarihi = iade_tarihi.strftime("%d-%m-%Y")
            self.cursor.execute(
                f"SELECT {self.arac_tipi}_id FROM {self.arac_tipi} WHERE durumu='müsait' AND {self.arac_tipi}_id=? LIMIT 1",
                (arac_id,))
            result = self.cursor.fetchone()
            print(f"{self.arac_tipi.capitalize()} ID={arac_id} haftalık olarak kiralandı.")
            self.kiralamaEkle(arac_id, 'haftalik')
            self.conn.commit()


class BisikletKiralama(AracKiralama):
    def __init__(self, root):
        super().__init__("bisiklet")
        self.root = root
        self.connection = self.conn  # Add this line


class ArabaKiralama(AracKiralama):
    def __init__(self, root):
        super().__init__("araba")
        self.root = root
        self.connection = self.conn

class Musteri:
    def __init__(self):
        self.bisikletler = 0
        self.kiralamaTime_b = None
        self.arabalar = 0
        self.kiralamaTime_c = None

    def aracIstegi(self, arac_tipi):
        conn = sqlite3.connect('kiralama-1.db')
        cursor = conn.cursor()
        if arac_tipi == "bisiklet":
            cursor.execute(f"SELECT bisiklet_id FROM bisiklet WHERE durumu='müsait'")
            result = cursor.fetchall()
            if result:
                print(f"Mevcut bisikletlerin ID'leri:")
                for row in result:
                    print(row[0])
                arac_id = int(input("Hangi bisikletin ID'sine sahip olanı kiralamak istersiniz? "))
                if arac_id in [row[0] for row in result]:
                    cursor.execute("UPDATE bisiklet SET durumu='kiralandı' WHERE bisiklet_id=?", (arac_id,))
                    #print(f"Bisiklet_id={arac_id} olan bisiklet kiralandı.")
                    self.bisikletler = 1
                else:
                    print("Belirtilen ID'ye sahip müsait bir bisiklet bulunamadı.")
                    arac_id = None
            else:
                print("Mevcut bisiklet yok.")
                arac_id = None
        elif arac_tipi == "araba":
            cursor.execute(f"SELECT araba_id FROM araba WHERE durumu='müsait'")
            result = cursor.fetchall()
            if result:
                print(f"Mevcut arabaların ID'leri:")
                for row in result:
                    print(row[0])
                arac_id = int(input("Hangi arabanın ID'sine sahip olanı kiralamak istersiniz? "))
                if arac_id in [row[0] for row in result]:
                    cursor.execute("UPDATE araba SET durumu='kiralandı' WHERE araba_id=?", (arac_id,))
                    #print(f"Araba_id={arac_id} olan araba kiralandı.")
                    self.arabalar = 1
                else:
                    print("Belirtilen ID'ye sahip müsait bir araba bulunamadı.")
                    arac_id = None
            else:
                print("Mevcut araba yok.")
                arac_id = None
        else:
            print("Geçersiz araç isteği")
            arac_id = None
        conn.commit()
        conn.close()
        return arac_id

    def fatura_hesapla(self, arac_tipi, kiralama_basis, kiralama_suresi):
        if arac_tipi == "bisiklet":
            ucret = 0
            if kiralama_basis == 1:  # Saatlik
                ucret = kiralama_suresi * 30
            elif kiralama_basis == 2:  # Günlük
                ucret = kiralama_suresi * 150
            elif kiralama_basis == 3:  # Haftalık
                ucret = kiralama_suresi * 500
            return ucret
        elif arac_tipi == "araba":
            ucret = 0
            if kiralama_basis == 1:  # Saatlik
                ucret = kiralama_suresi * 100
            elif kiralama_basis == 2:  # Günlük
                ucret = kiralama_suresi * 500
            elif kiralama_basis == 3:  # Haftalık
                ucret = kiralama_suresi * 1500
            return ucret
        else:
            return 0

    def aracIade(self, arac_tipi):
        conn = sqlite3.connect('kiralama-1.db')
        cursor = conn.cursor()

        cursor.execute(
            f"SELECT  arac_id, kiralama_tipi, kiralama_zamani FROM kiralama WHERE arac_tipi=? AND durumu='kiralandı'",
            (arac_tipi,)
        )
        result = cursor.fetchall()

        if result:
            print(f"Kiralanmış {arac_tipi}lerin Bilgileri:")
            for row in result:
                print(f"Araç ID: {row[0]}, Kiralama Türü: {row[1]}, Kiralama Zamanı: {row[2]}")

            arac_id = int(input(f"İade etmek istediğiniz {arac_tipi} ID'sini girin: "))
            if any(arac_id == row[0] for row in result):
                cursor.execute(f"UPDATE {arac_tipi} SET durumu='müsait' WHERE {arac_tipi}_id=?", (arac_id,))
                iade_zamani = datetime.datetime.now().strftime('%H:%M  %d-%m-%Y ')

                cursor.execute(
                    "UPDATE kiralama SET durumu='müsait', iade_zamani=? WHERE arac_id=? AND durumu='kiralandı'",
                    (iade_zamani, arac_id,))

                print(
                    f"{arac_tipi.capitalize()} ID {arac_id} olan araç başarıyla iade edildi. İade Zamanı: {iade_zamani}")
                conn.commit()
                if arac_tipi == "bisiklet":
                    self.bisikletler -= 1
                elif arac_tipi == "araba":
                    self.arabalar -= 1
                kiralama_basis = 0
                kiralama_suresi = 0
                for row in result:
                    if row[0] == arac_id:
                        kiralama_basis = 1 if row[1] == 'saatlik' else (2 if row[1] == 'gunluk' else 3)
                        kiralama_suresi = (datetime.datetime.now() - datetime.datetime.strptime(row[2],
                                                                                                '%H:%M %d-%m-%Y ')).total_seconds() / 3600
                        break

                if kiralama_basis != 0 and kiralama_suresi != 0:
                    ucret = self.fatura_hesapla(arac_tipi, kiralama_basis, kiralama_suresi)
                    print(f"Fatura: {ucret:.2f}TL")
                else:
                    print("Fatura oluşturulamadı.")

            else:
                print(f"Belirtilen ID'ye sahip kiralanmış bir {arac_tipi} bulunamadı.")
        else:
            print(f"İade edilecek kiralanmış {arac_tipi} yok.")

        conn.close()

