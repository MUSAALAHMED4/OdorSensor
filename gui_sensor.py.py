import serial
import csv
import time
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Seri bağlantı ayarları
port = '/dev/cu.usbserial-A5069RR4'  # ← Cihaza göre değiştir
baudrate = 9600
filename = 'KokuVerisi.csv'

ser = None
running = False
writer = None
file = None

# Tekrar engelleme için zaman izleyici
recent_smells = {}
REPEAT_TIMEOUT = 15  # saniye

# Klavye kısayolları → Koku isimleri
manual_keys = {
    'a': 'Soğan',
    's': 'Sarımsak',
    'd': 'Duman',
    'f': 'Alkol',
    'g': 'Temiz Hava'
}

# Koku isimleri → İkon dosyaları
def get_icon_filename(smell):
    icons = {
        'Duman': 'smoke.png',
        'Sarımsak': 'garlic.png',
        'Soğan': 'onion.png',
        'Alkol': 'alcohol.png',
        'Temiz Hava': 'clean_air.png',
        'Bekleniyor...': 'waiting.png'
    }
    return icons.get(smell, None)

# Koku göster ve dosyaya yaz (tekrar kontrolü dahil)
def show_smell(smell, time_ms, value):
    now = time.time()

    # Son 15 saniyede tekrarlandıysa atla
    last_time = recent_smells.get(smell)
    if last_time is not None and (now - last_time) < REPEAT_TIMEOUT:
        print(f"[⏳] {smell} son {REPEAT_TIMEOUT} saniyede tekrarlandı → atlandı")
        return

    # Zaman güncelle
    recent_smells[smell] = now

    # Ekranda göster
    smell_label.config(text=smell)

    icon_file = get_icon_filename(smell)
    if icon_file:
        try:
            img = Image.open(icon_file).resize((120, 120))
            img = ImageTk.PhotoImage(img)
            icon_label.config(image=img)
            icon_label.image = img
        except Exception as e:
            print("⚠️ Görsel yüklenemedi:", e)
    else:
        icon_label.config(image='')
        icon_label.image = None

    # CSV dosyasına yaz
    if writer:
        writer.writerow([time_ms, value, smell])
        print("[✓] Kaydedildi:", [time_ms, value, smell])

# Seri bağlantıyı başlat
def start_reading():
    global running, ser, writer, file
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)
        running = True

        file = open(filename, 'w', newline='', encoding='utf-8')
        writer = csv.writer(file)
        writer.writerow(["Zaman(ms)", "MQ135 Değeri", "Koku"])

        read_serial()
    except Exception as e:
        messagebox.showerror("Hata", f"Seri port açılmadı: {e}")

# Seri veriyi oku
def read_serial():
    global running
    if not running:
        return

    line = ser.readline().decode('utf-8').strip()
    if line:
        parts = line.split(',')
        if len(parts) == 3:
            time_ms, value, smell = parts
            show_smell(smell, time_ms, value)

    root.after(1000, read_serial)

# Klavyeden manuel koku gir
def handle_key(event):
    key = event.char.lower()
    if key in manual_keys:
        smell = manual_keys[key]
        current_time = int(time.time() * 1000)
        value = 0
        show_smell(smell, current_time, value)

# Okumayı durdur
def stop_reading():
    global running, ser, file
    running = False
    if ser:
        ser.close()
    if file:
        file.close()
    smell_label.config(text="")
    icon_label.config(image='')
    icon_label.image = None

# Kullanıcı arayüzü
root = tk.Tk()
root.title("Koku Dedektörü")
root.geometry("400x500")
root.configure(bg="#1e1e1e")

font_title = ("Arial", 18, "bold")
font_button = ("Arial", 14)
font_label = ("Arial", 16)

# Başlat butonu
start_button = tk.Button(root, text="Algılamaya Başla", command=start_reading,
                         font=font_button, bg="#4CAF50", fg="white", width=30)
start_button.pack(pady=20)

# Durdur butonu
stop_button = tk.Button(root, text="Durdur", command=stop_reading,
                        font=font_button, bg="#f44336", fg="white", width=15)
stop_button.pack(pady=5)

# Koku etiketi
smell_label = tk.Label(root, text="", font=font_label, fg="white", bg="#1e1e1e")
smell_label.pack(pady=20)

# İkon etiketi
icon_label = tk.Label(root, bg="#1e1e1e")
icon_label.pack(pady=10)


# Klavye dinleme
root.bind('<Key>', handle_key)

# Başlat
root.mainloop()
