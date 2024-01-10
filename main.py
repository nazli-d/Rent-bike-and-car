import tkinter as tk
from tkinter import ttk, messagebox
from rent import BisikletKiralama, ArabaKiralama, Musteri
import datetime

class AracKiralamaUygulamasi:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ARAÇ KİRALAMA SİSTEMİ")
        self.root.geometry("600x250")

        self.bike_rental = BisikletKiralama(self.root)
        self.car_rental = ArabaKiralama(self.root)
        self.customer = Musteri()
        self.selected_bike_id = None

        self.create_main_menu()

    def create_main_menu(self):
        main_label = tk.Label(self.root, text="ARAÇ KİRALAMA SİSTEMİ", font=("Arial", 24, "bold", "italic"))
        main_label.pack(pady=20)

        frame = tk.Frame(self.root)
        frame.pack()

        bisiklet_button = tk.Button(frame, text="Bisiklet Kiralama", command=self.show_bike_menu, width=20, height=2,
                                    bg="purple", fg="white", font=("Arial", 12))
        bisiklet_button.grid(row=0, column=0, padx=20, pady=10)

        araba_button = tk.Button(frame, text="Araba Kiralama", command=self.show_car_menu, width=20, height=2,
                                 bg="purple", fg="white", font=("Arial", 12))
        araba_button.grid(row=0, column=1, padx=20, pady=10)

        exit_button = tk.Button(self.root, text="Çıkış", command=self.root.destroy, font=("Helvetica", 12), width=10, bg="gray")
        exit_button.pack(pady=20)

    def show_bike_menu(self):
        bike_menu_window = tk.Toplevel(self.root)
        bike_menu_window.title("BİSİKLET KİRALAMA MENÜSÜ")
        bike_menu_window.geometry("500x450")

        bike_label = tk.Label(bike_menu_window, text="BİSİKLET KİRALAMA MENÜSÜ", font=("Arial", 20, "bold"))
        bike_label.pack(pady=20)

        show_bike_button = tk.Button(bike_menu_window, text="Mevcut Bisikletleri Göster",
                                     command=self.bike_rental.stokGoster, width=30, height=2)

        show_bike_button.pack(pady=10)

        hourly_bike_button = tk.Button(bike_menu_window, text="Saatlik bisiklet iste (30 TL)", command=self.request_bike_hourly, width=30, height=2)
        hourly_bike_button.pack(pady=10)

        daily_bike_button = tk.Button(bike_menu_window, text="Günlük Bisiklet İste (150 TL)", command=self.request_bike_daily, width=30, height=2)
        daily_bike_button.pack(pady=10)

        weekly_bike_button = tk.Button(bike_menu_window, text="Haftalık Bisiklet İste (500 TL)", command=self.request_bike_weekly, width=30, height=2)
        weekly_bike_button.pack(pady=10)

        return_bike_button = tk.Button(bike_menu_window, text="Bisiklet İade Et", command=self.return_bike, width=30, height=2)
        return_bike_button.pack(pady=10)

        back_button = tk.Button(bike_menu_window, text="Ana Menü", command=bike_menu_window.destroy, width=30, height=2)
        back_button.pack(pady=10)

    def show_car_menu(self):
        car_menu_window = tk.Toplevel(self.root)
        car_menu_window.title("ARABA KİRALAMA MENÜSÜ")
        car_menu_window.geometry("500x450")

        car_label = tk.Label(car_menu_window, text="ARABA KİRALAMA MENÜSÜ", font=("Arial", 20, "bold"))
        car_label.pack(pady=20)

        show_car_button = tk.Button(car_menu_window, text="Mevcut Arabaları Göster", command=self.car_rental.stokGoster, width=30, height=2)
        show_car_button.pack(pady=10)

        hourly_car_button = tk.Button(car_menu_window, text="Saatlik Araba İste (100 TL)", command=self.request_car_hourly, width=30, height=2)
        hourly_car_button.pack(pady=10)

        daily_car_button = tk.Button(car_menu_window, text="Günlük Araba İste (500 TL)", command=self.request_car_daily, width=30, height=2)
        daily_car_button.pack(pady=10)

        weekly_car_button = tk.Button(car_menu_window, text="Haftalık Araba İste (1500 TL)", command=self.request_car_weekly, width=30, height=2)
        weekly_car_button.pack(pady=10)

        return_car_button = tk.Button(car_menu_window, text="Araba İade Et", command=self.return_car, width=30, height=2)
        return_car_button.pack(pady=10)

        back_button = tk.Button(car_menu_window, text="Ana Menü", command=car_menu_window.destroy, width=30, height=2)
        back_button.pack(pady=10)

    def request_bike_hourly(self):
        hourly_bike_window = tk.Toplevel(self.root)
        hourly_bike_window.title("Saatlik Bisiklet İste")
        hourly_bike_window.geometry("650x300")

        label_frame = tk.LabelFrame(hourly_bike_window, text="", font=("Arial", 12, "bold"))
        label_frame.pack(pady=20)

        columns = ("ID", "Durumu", "Seçim")
        tree = ttk.Treeview(label_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack()

        self.bike_rental.cursor.execute(
            f"SELECT {self.bike_rental.arac_tipi}_id, durumu FROM {self.bike_rental.arac_tipi} WHERE durumu='müsait'")
        result = self.bike_rental.cursor.fetchall()

        if result:
            for row in result:
                tree.insert("", "end", values=(row[0], row[1], "Seç"), tags="button")

            def select_bike(event):
                item = tree.item(tree.focus())
                if item['values'] and item['values'][2] == "Seç":
                    # Update the instance variable
                    self.selected_bike_id = item['values'][0]
                    self.confirm_hourly_bike(self.selected_bike_id, hourly_bike_window)

            tree.tag_bind("button", "<ButtonRelease-1>", select_bike)

        else:
            no_data_label = tk.Label(label_frame, text=f"Mevcut {self.bike_rental.arac_tipi} yok.", font=("Arial", 12),
                                     pady=5)
            no_data_label.grid(row=1, column=0, sticky="w", padx=10)

    def confirm_hourly_bike(self, selected_bike_id, window):
        # İkinci pencereyi kapat
        window.destroy()

        # Saatlik bisiklet kiralama işlemini gerçekleştir
        self.customer.kiralamaTime_b = self.bike_rental.saatlikKiralama(selected_bike_id)
        self.customer.kiralamaBasis_b = 1

    def request_bike_daily(self):
        daily_bike_window = tk.Toplevel(self.root)
        daily_bike_window.title("Günlük Bisiklet İste")
        daily_bike_window.geometry("650x300")

        label_frame = tk.LabelFrame(daily_bike_window, text="", font=("Arial", 12, "bold"))
        label_frame.pack(pady=20)

        columns = ("ID", "Durumu", "Seçim")
        tree = ttk.Treeview(label_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack()

        self.bike_rental.cursor.execute(
            f"SELECT {self.bike_rental.arac_tipi}_id, durumu FROM {self.bike_rental.arac_tipi} WHERE durumu='müsait'")
        result = self.bike_rental.cursor.fetchall()

        if result:
            for row in result:
                tree.insert("", "end", values=(row[0], row[1], "Seç"), tags="button")

            def select_bike(event):
                item = tree.item(tree.focus())
                if item['values'] and item['values'][2] == "Seç":
                    selected_bike_id = item['values'][0]
                    self.confirm_daily_bike(selected_bike_id, daily_bike_window)

            tree.tag_bind("button", "<ButtonRelease-1>", select_bike)

        else:
            no_data_label = tk.Label(label_frame, text=f"Mevcut {self.bike_rental.arac_tipi} yok.", font=("Arial", 12),
                                     pady=5)
            no_data_label.grid(row=1, column=0, sticky="w", padx=10)

    def confirm_daily_bike(self, selected_bike_id, window):
        window.destroy()

        self.customer.kiralamaTime_b = self.bike_rental.gunlukKiralama(selected_bike_id)
        self.customer.kiralamaBasis_b = 2

    def request_bike_weekly(self):
        weekly_bike_window = tk.Toplevel(self.root)
        weekly_bike_window.title("Haftalık Bisiklet İste")
        weekly_bike_window.geometry("650x300")

        label_frame = tk.LabelFrame(weekly_bike_window, text="", font=("Arial", 12, "bold"))
        label_frame.pack(pady=20)

        columns = ("ID", "Durumu", "Seçim")
        tree = ttk.Treeview(label_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack()

        self.bike_rental.cursor.execute(
            f"SELECT {self.bike_rental.arac_tipi}_id, durumu FROM {self.bike_rental.arac_tipi} WHERE durumu='müsait'")
        result = self.bike_rental.cursor.fetchall()

        if result:
            for row in result:
                tree.insert("", "end", values=(row[0], row[1], "Seç"), tags="button")

            def select_bike(event):
                item = tree.item(tree.focus())
                if item['values'] and item['values'][2] == "Seç":
                    selected_bike_id = item['values'][0]
                    self.confirm_weekly_bike(selected_bike_id, weekly_bike_window)

            tree.tag_bind("button", "<ButtonRelease-1>", select_bike)

        else:
            no_data_label = tk.Label(label_frame, text=f"Mevcut {self.bike_rental.arac_tipi} yok.", font=("Arial", 12),
                                     pady=5)
            no_data_label.grid(row=1, column=0, sticky="w", padx=10)

    def confirm_weekly_bike(self, selected_bike_id, window):
        window.destroy()

        self.customer.kiralamaTime_b = self.bike_rental.haftalikKiralama(selected_bike_id)
        self.customer.kiralamaBasis_b = 3

    def request_car_hourly(self):
        hourly_car_window = tk.Toplevel(self.root)
        hourly_car_window.title("Saatlik Araba İste")
        hourly_car_window.geometry("650x300")

        label_frame = tk.LabelFrame(hourly_car_window, text="", font=("Arial", 12, "bold"))
        label_frame.pack(pady=20)

        columns = ("ID", "Durumu", "Seçim")
        tree = ttk.Treeview(label_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack()

        self.car_rental.cursor.execute(
            f"SELECT {self.car_rental.arac_tipi}_id, durumu FROM {self.car_rental.arac_tipi} WHERE durumu='müsait'")
        result = self.car_rental.cursor.fetchall()

        if result:
            for row in result:
                tree.insert("", "end", values=(row[0], row[1], "Seç"), tags="button")

            def select_car(event):
                item = tree.item(tree.focus())
                if item['values'] and item['values'][2] == "Seç":
                    selected_car_id = item['values'][0]
                    self.confirm_hourly_car(selected_car_id, hourly_car_window)

            tree.tag_bind("button", "<ButtonRelease-1>", select_car)

        else:
            no_data_label = tk.Label(label_frame, text=f"Mevcut {self.car_rental.arac_tipi} yok.", font=("Arial", 12),
                                     pady=5)
            no_data_label.grid(row=1, column=0, sticky="w", padx=10)

    def confirm_hourly_car(self, selected_car_id, window):
        window.destroy()

        self.customer.kiralamaTime_c = self.car_rental.saatlikKiralama(selected_car_id)
        self.customer.kiralamaBasis_c = 1

    def request_car_daily(self):
        daily_car_window = tk.Toplevel(self.root)
        daily_car_window.title("Günlük Araba İste")
        daily_car_window.geometry("650x300")

        label_frame = tk.LabelFrame(daily_car_window, text="", font=("Arial", 12, "bold"))
        label_frame.pack(pady=20)

        columns = ("ID", "Durumu", "Seçim")
        tree = ttk.Treeview(label_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack()

        self.car_rental.cursor.execute(
            f"SELECT {self.car_rental.arac_tipi}_id, durumu FROM {self.car_rental.arac_tipi} WHERE durumu='müsait'")
        result = self.car_rental.cursor.fetchall()

        if result:
            for row in result:
                tree.insert("", "end", values=(row[0], row[1], "Seç"), tags="button")

            def select_car(event):
                item = tree.item(tree.focus())
                if item['values'] and item['values'][2] == "Seç":
                    selected_car_id = item['values'][0]
                    self.confirm_daily_car(selected_car_id, daily_car_window)

            tree.tag_bind("button", "<ButtonRelease-1>", select_car)

        else:
            no_data_label = tk.Label(label_frame, text=f"Mevcut {self.car_rental.arac_tipi} yok.", font=("Arial", 12),
                                     pady=5)
            no_data_label.grid(row=1, column=0, sticky="w", padx=10)

    def confirm_daily_car(self, selected_car_id, window):
        window.destroy()

        self.customer.kiralamaTime_c = self.car_rental.gunlukKiralama(selected_car_id)
        self.customer.kiralamaBasis_c = 2

    def request_car_weekly(self):
        weekly_car_window = tk.Toplevel(self.root)
        weekly_car_window.title("Haftalık Araba İste")
        weekly_car_window.geometry("650x300")

        label_frame = tk.LabelFrame(weekly_car_window, text="", font=("Arial", 12, "bold"))
        label_frame.pack(pady=20)

        columns = ("ID", "Durumu", "Seçim")
        tree = ttk.Treeview(label_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack()

        self.car_rental.cursor.execute(
            f"SELECT {self.car_rental.arac_tipi}_id, durumu FROM {self.car_rental.arac_tipi} WHERE durumu='müsait'")
        result = self.car_rental.cursor.fetchall()

        if result:
            for row in result:
                tree.insert("", "end", values=(row[0], row[1], "Seç"), tags="button")

            def select_car(event):
                item = tree.item(tree.focus())
                if item['values'] and item['values'][2] == "Seç":
                    selected_car_id = item['values'][0]
                    self.confirm_weekly_car(selected_car_id, weekly_car_window)

            tree.tag_bind("button", "<ButtonRelease-1>", select_car)

        else:
            no_data_label = tk.Label(label_frame, text=f"Mevcut {self.car_rental.arac_tipi} yok.", font=("Arial", 12),
                                     pady=5)
            no_data_label.grid(row=1, column=0, sticky="w", padx=10)

    def confirm_weekly_car(self, selected_car_id, window):
        window.destroy()

        self.customer.kiralamaTime_c = self.car_rental.haftalikKiralama(selected_car_id)
        self.customer.kiralamaBasis_c = 3

    # AracKiralamaUygulamasi sınıfında iade fonksiyonları
    def return_bike(self):
        return_window = tk.Toplevel(self.root)
        return_window.title("Bisiklet İade")
        return_window.geometry("950x300")

        label_frame = tk.LabelFrame(return_window, text="", font=("Arial", 12, "bold"))
        label_frame.pack(pady=20)

        columns = ("ID", "Durumu", "Kiralama Tipi", "Kiralama zamanı", "Seçim")
        tree = ttk.Treeview(label_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack()

        self.bike_rental.cursor.execute(
            f"SELECT k.arac_id, b.durumu, k.kiralama_tipi, k.kiralama_zamani FROM kiralama k JOIN bisiklet b ON k.arac_id = b.bisiklet_id WHERE b.durumu='kiralandı'"
        )

        result = self.bike_rental.cursor.fetchall()

        if result:
            for row in result:
                tree.insert("", "end", values=(row[0], row[1], row[2],row[3], "Seç"), tags="button")

            def select_bike_for_return(event):
                item = tree.item(tree.focus())
                if item['values'] and item['values'][4] == "Seç":
                    selected_bike_id = item['values'][0]
                    self.confirm_return_bike(selected_bike_id, return_window)

            tree.tag_bind("button", "<ButtonRelease-1>", select_bike_for_return)
        else:
            no_data_label = tk.Label(label_frame, text=f"İade edilecek bisiklet bulunamadı.",
                                     font=("Arial", 12), pady=5)
            no_data_label.pack()  # Change here

    def confirm_return_bike(self, selected_bike_id, window):
        window.destroy()

        # İade işlemi gerçekleştir
        cursor = self.bike_rental.cursor

        # Fetching kiralama_tipi and durumu based on bisiklet_id
        cursor.execute("SELECT id, kiralama_tipi, durumu FROM kiralama WHERE arac_id=? AND durumu='kiralandı'",
                       (selected_bike_id,))
        result = cursor.fetchone()

        if result:
            kiralama_id, kiralama_tipi, durumu = result

            # Bisiklet durumunu müsait olarak güncelle
            cursor.execute(f"UPDATE bisiklet SET durumu='müsait' WHERE bisiklet_id=?", (selected_bike_id,))

            # İade zamanını güncelle
            iade_zamani = datetime.datetime.now().strftime('%H:%M %d-%m-%Y ')
            cursor.execute(
                f"UPDATE kiralama SET durumu='müsait', iade_zamani=? WHERE arac_id=? AND durumu='kiralandı'",
                (iade_zamani, selected_bike_id)
            )

            # Bu değişiklikleri kaydet
            self.bike_rental.connection.commit()

            # Display confirmation message with kiralama_id, kiralama_tipi, and durumu
            messagebox.showinfo("Başarılı",
                                f"Bisiklet ID: {selected_bike_id}, Kiralama ID: {kiralama_id}, Kiralama Tipi: {kiralama_tipi}, Durumu: {durumu}, İade Zamanı: {iade_zamani}")
            self.root.update()
        else:
            # Handle the case where information is not found (you can show an error message)
            messagebox.showerror("Hata", f"Seçili bisiklet için kiralama bilgisi bulunamadı.")

    def return_car(self):
        return_window = tk.Toplevel(self.root)
        return_window.title("Araba İade")
        return_window.geometry("950x300")

        label_frame = tk.LabelFrame(return_window, text="", font=("Arial", 12, "bold"))
        label_frame.pack(pady=20)

        columns = ("ID", "Durumu", "Kiralama Tipi", "Kiralama zamanı", "Seçim")
        tree = ttk.Treeview(label_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack()

        self.car_rental.cursor.execute(
            f"SELECT k.arac_id, a.durumu, k.kiralama_tipi, k.kiralama_zamani FROM kiralama k JOIN araba a ON k.arac_id = a.araba_id WHERE a.durumu='kiralandı'"
        )

        result = self.car_rental.cursor.fetchall()

        if result:
            for row in result:
                tree.insert("", "end", values=(row[0], row[1], row[2], row[3], "Seç"), tags="button")

            def select_car_for_return(event):
                item = tree.item(tree.focus())
                if item['values'] and item['values'][4] == "Seç":
                    selected_car_id = item['values'][0]
                    self.confirm_return_car(selected_car_id, return_window)

            tree.tag_bind("button", "<ButtonRelease-1>", select_car_for_return)
        else:
            no_data_label = tk.Label(label_frame, text=f"İade edilecek {self.car_rental.arac_tipi} bulunamadı.",
                                     font=("Arial", 12), pady=5)
            no_data_label.pack()

    def confirm_return_car(self, selected_car_id, window):
        window.destroy()

        # İade işlemi gerçekleştir
        cursor = self.car_rental.cursor
        cursor.execute(f"UPDATE araba SET durumu='müsait' WHERE araba_id=?", (selected_car_id,))

        # İade zamanını güncelle
        iade_zamani = datetime.datetime.now().strftime('%H:%M %d-%m-%Y ')
        cursor.execute(
            f"UPDATE kiralama SET durumu='müsait', iade_zamani=? WHERE arac_id=? AND durumu='kiralandı'",
            (iade_zamani, selected_car_id)
        )

        # Bu değişiklikleri kaydet
        self.car_rental.connection.commit()

        messagebox.showinfo("Başarılı",
                            f"Araba ID {selected_car_id} olan araç başarıyla iade edildi. İade Zamanı: {iade_zamani}")
        self.root.update()


if __name__ == "__main__":
    app = AracKiralamaUygulamasi()
    app.root.mainloop()
