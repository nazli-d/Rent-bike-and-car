import sqlite3

# Veritabanı bağlantısını oluştur
conn = sqlite3.connect('kiralama-1.db')
cursor = conn.cursor()

# Araba tablosunu güncelle
cursor.execute('''
    CREATE TABLE IF NOT EXISTS araba (
        araba_id INTEGER PRIMARY KEY AUTOINCREMENT,
        durumu TEXT DEFAULT 'müsait'
    )
''')

# Bisiklet tablosunu güncelle
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bisiklet (
        bisiklet_id INTEGER PRIMARY KEY AUTOINCREMENT,
        durumu TEXT DEFAULT 'müsait'    
    )
''')

# Kiralama tablosunu güncelle
cursor.execute('''
    CREATE TABLE IF NOT EXISTS kiralama (
        id INTEGER PRIMARY KEY,
        arac_id INTEGER,
        arac_tipi TEXT,
        kiralama_tipi TEXT,
        kiralama_zamani DATETIME,
        iade_zamani DATETIME ,
        durumu TEXT DEFAULT 'kiralandı' ,
        FOREIGN KEY (arac_id, arac_tipi) REFERENCES araba(araba_id, 'araba') 
                                              ON DELETE CASCADE
                                              ON UPDATE CASCADE,
        FOREIGN KEY (arac_id, arac_tipi) REFERENCES bisiklet(bisiklet_id, 'bisiklet') 
                                              ON DELETE CASCADE
                                              ON UPDATE CASCADE,
        CHECK (arac_tipi IN ('bisiklet', 'araba')),
        CHECK (kiralama_tipi IN ('saatlik', 'gunluk', 'haftalik'))
    )
''')


# Araba verilerini ekle

cursor.execute("INSERT INTO araba (durumu) VALUES ('müsait')")
cursor.execute("INSERT INTO araba (durumu) VALUES ('müsait')")
cursor.execute("INSERT INTO araba (durumu) VALUES ('müsait')")
cursor.execute("INSERT INTO araba (durumu) VALUES ('müsait')")
cursor.execute("INSERT INTO araba (durumu) VALUES ('müsait')")
cursor.execute("INSERT INTO araba (durumu) VALUES ('müsait')")
cursor.execute("INSERT INTO araba (durumu) VALUES ('müsait')")
cursor.execute("INSERT INTO araba (durumu) VALUES ('müsait')")
cursor.execute("INSERT INTO araba (durumu) VALUES ('müsait')")
cursor.execute("INSERT INTO araba (durumu) VALUES ('müsait')")


# Bisiklet verilerini ekle
cursor.execute("INSERT INTO bisiklet (durumu) VALUES ('müsait')")
cursor.execute("INSERT INTO bisiklet (durumu) VALUES ('müsait')")
cursor.execute("INSERT INTO bisiklet (durumu) VALUES ('müsait')")
cursor.execute("INSERT INTO bisiklet (durumu) VALUES ('müsait')")
cursor.execute("INSERT INTO bisiklet (durumu) VALUES ('müsait')")
cursor.execute("INSERT INTO bisiklet (durumu) VALUES ('müsait')")
cursor.execute("INSERT INTO bisiklet (durumu) VALUES ('müsait')")
cursor.execute("INSERT INTO bisiklet (durumu) VALUES ('müsait')")
cursor.execute("INSERT INTO bisiklet (durumu) VALUES ('müsait')")
cursor.execute("INSERT INTO bisiklet (durumu) VALUES ('müsait')")



# Veritabanı bağlantısını kaydet
conn.commit()

# Veritabanı bağlantısını kapat
conn.close()
