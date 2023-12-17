import sqlite3

baglanti = sqlite3.connect("rent-a.db")
cursor = baglanti.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS musteri (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ad_soyad TEXT
    )
''')

# Araba tablosunu oluştur
cursor.execute('''
    CREATE TABLE IF NOT EXISTS arabalar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        marka TEXT,
        model TEXT,
        yil INTEGER,
        tip TEXT,
        durumu TEXT DEFAULT 'müsait'
    )
''')

# Kiralama tablosunu oluştur
cursor.execute('''
    CREATE TABLE IF NOT EXISTS kiralama (
        musteri_id TEXT,
        araba_id INTEGER,
        kiralama_tipi TEXT,
        sure INTEGER,
        ucret INTEGER,
        durumu TEXT DEFAULT 'kiralandı',
        FOREIGN KEY (araba_id) REFERENCES arabalar (id),
        FOREIGN KEY (musteri_id) REFERENCES musteri(id)
       
    )
''')



# Elektrikli Arabalar
cursor.execute("INSERT INTO arabalar (marka, model, yil, tip) VALUES ('Tesla', 'Model S', 2023, 'Elektrikli')")
cursor.execute("INSERT INTO arabalar (marka, model, yil, tip) VALUES ('Porsche', 'Taycan', 2023, 'Elektrikli')")
cursor.execute("INSERT INTO arabalar (marka, model, yil, tip) VALUES ('Audi', 'e-tron', 2023, 'Elektrikli')")
cursor.execute("INSERT INTO arabalar (marka, model, yil, tip) VALUES ('Mercedes-Benz', 'EQC', 2023, 'Elektrikli')")
cursor.execute("INSERT INTO arabalar (marka, model, yil, tip) VALUES ('Jaguar', 'I-PACE', 2023, 'Elektrikli')")

# Benzinli Arabalar
cursor.execute("INSERT INTO arabalar (marka, model, yil, tip) VALUES ('Mercedes-Benz', 'S-Class', 2023, 'Benzinli')")
cursor.execute("INSERT INTO arabalar (marka, model, yil, tip) VALUES ('BMW', '7 Series', 2023, 'Benzinli')")
cursor.execute("INSERT INTO arabalar (marka, model, yil, tip) VALUES ('Lexus', 'LS', 2023, 'Benzinli')")
cursor.execute("INSERT INTO arabalar (marka, model, yil, tip) VALUES ('Audi', 'A8', 2023, 'Benzinli')")
cursor.execute("INSERT INTO arabalar (marka, model, yil, tip) VALUES ('Porsche', 'Panamera', 2023, 'Benzinli')")

baglanti.commit()
# Veritabanı bağlantısını kapat
baglanti.close()


