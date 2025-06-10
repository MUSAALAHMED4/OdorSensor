import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
from main import KokuDedektor

# Konfigürasyon
PORT = '/dev/cu.usbserial-A5069RR4'
BAUDRATE = 9600
FILENAME = 'KokuVerisi.csv'

manual_keys = {
    'a': 'Soğan',
    's': 'Sarımsak',
    'd': 'Duman',
    'f': 'Alkol',
    'g': 'Temiz Hava'
}

def get_icon_filename(smell):
    icons = {
        'Duman': 'icons/smoke.png',
        'Sarımsak': 'icons/garlic.png',
        'Soğan': 'icons/onion.png',
        'Alkol': 'icons/alcohol.png',
        'Temiz Hava': 'icons/clean_air.png',
        'Bekleniyor...': 'icons/waiting.png'
    }
    return icons.get(smell)

detector = KokuDedektor(PORT, BAUDRATE, FILENAME)

def show_smell_gui(smell, time_ms, value):
    if detector.should_skip_smell(smell):
        print(f"[⏳] {smell} son 15 saniyede tekrarlandı → atlandı")
        return

    smell_label.config(text=smell)

    icon_path = get_icon_filename(smell)
    if icon_path:
        try:
            img = Image.open(icon_path).resize((120, 120))
            img = ImageTk.PhotoImage(img)
            icon_label.config(image=img)
            icon_label.image = img
        except Exception as e:
            print("⚠️ Görsel yüklenemedi:", e)
    else:
        icon_label.config(image='')
        icon_label.image = None

    detector.log_smell(time_ms, value, smell)
    print("[✓] Kaydedildi:", [time_ms, value, smell])

def start_reading():
    try:
        detector.start()
        read_loop()
    except Exception as e:
        messagebox.showerror("Hata", f"Seri port açılmadı: {e}")

def stop_reading():
    detector.stop()
    smell_label.config(text="")
    icon_label.config(image='')
    icon_label.image = None

def read_loop():
    result = detector.read_line()
    if result:
        time_ms, value, smell = result
        show_smell_gui(smell, time_ms, value)
    root.after(1000, read_loop)

def handle_key(event):
    key = event.char.lower()
    if key in manual_keys:
        smell = manual_keys[key]
        time_ms, value, smell = detector.handle_manual_smell(smell)
        show_smell_gui(smell, time_ms, value)
# GUI Ayarları - Geliştirilmiş
root = tk.Tk()
root.title("Koku Dedektörü")
root.geometry("420x520")
root.configure(bg="#121212")  # Daha koyu şık arka plan

font_title = ("Helvetica", 20, "bold")
font_button = ("Helvetica", 14)
font_label = ("Helvetica", 16, "bold")

# Üst başlık
title_label = tk.Label(root, text="Koku Dedektörü", font=font_title, fg="white", bg="#121212")
title_label.pack(pady=(25, 10))

# Butonlar çerçevesi
button_frame = tk.Frame(root, bg="#121212")
button_frame.pack(pady=(0, 20))

start_button = tk.Button(button_frame, text="Algılamaya Başla", command=start_reading,
                         font=font_button, bg="#00C853", fg="white", width=20, height=2)
start_button.grid(row=0, column=0, padx=10)

stop_button = tk.Button(button_frame, text="Durdur", command=stop_reading,
                        font=font_button, bg="#D50000", fg="white", width=12, height=2)
stop_button.grid(row=0, column=1, padx=10)

# Koku metni
smell_label = tk.Label(root, text="Bekleniyor...", font=font_label,
                       fg="#FFD600", bg="#121212")
smell_label.pack(pady=10)

# Görsel gösterimi
icon_label = tk.Label(root, bg="#121212")
icon_label.pack(pady=15)

# Klavye dinleme
root.bind('<Key>', handle_key)

# Başlat
root.mainloop()
