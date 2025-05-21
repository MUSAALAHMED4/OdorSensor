from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont, QMovie
from PyQt5.QtCore import Qt, QTimer
from result_window import ResultWindow  # هذا الصحيح

class ReadingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("قراءة الرائحة")
        self.setGeometry(400, 200, 450, 400)
        self.setFocusPolicy(Qt.StrongFocus)

        self.layout = QVBoxLayout()

        self.wave_label = QLabel()
        self.wave_movie = QMovie("waves.gif")
        self.wave_label.setMovie(self.wave_movie)
        self.wave_label.setAlignment(Qt.AlignCenter)
        self.wave_label.setVisible(False)

        self.countdown_label = QLabel("")
        self.countdown_label.setFont(QFont("Arial", 20))
        self.countdown_label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("ابدأ")
        self.start_button.setFont(QFont("Arial", 14))
        self.start_button.clicked.connect(self.toggle_reading)

        self.layout.addWidget(self.wave_label)
        self.layout.addWidget(self.countdown_label)
        self.layout.addWidget(self.start_button)
        self.setLayout(self.layout)

        self.counter = 10
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.is_reading = False
        self.selected_key = None

    def toggle_reading(self):
        if not self.is_reading:
            self.start_reading()
        else:
            self.stop_reading(interrupted=True)

    def start_reading(self):
        self.counter = 10
        self.selected_key = None
        self.countdown_label.setText(f"{self.counter} ثوانٍ")
        self.wave_label.setVisible(True)
        self.wave_movie.start()
        self.start_button.setText("إيقاف")
        self.is_reading = True
        self.setFocus()
        self.timer.start(1000)

    def stop_reading(self, interrupted=False):
        self.timer.stop()
        self.wave_movie.stop()
        self.wave_label.setVisible(False)
        self.is_reading = False
        self.start_button.setText("ابدأ")
        if interrupted:
            self.countdown_label.setText("تم الإيقاف")

    def update_countdown(self):
        self.counter -= 1
        if self.counter > 0:
            self.countdown_label.setText(f"{self.counter} ثوانٍ")
        else:
            self.timer.stop()
            self.wave_movie.stop()
            self.wave_label.setVisible(False)
            self.is_reading = False
            self.start_button.setText("ابدأ")
            self.countdown_label.setText("تم الانتهاء")
            self.show_result_window(self.get_result_message(self.selected_key))

    def keyPressEvent(self, event):
        if self.is_reading:
            key = event.text().lower()
            if key in ['a', 's', 'd', 'f']:
                self.selected_key = key
                self.timer.stop()
                self.wave_movie.stop()
                self.wave_label.setVisible(False)
                self.is_reading = False
                self.start_button.setText("ابدأ")
                self.countdown_label.setText("تم التعرف على الرائحة مباشرة")
                self.show_result_window(self.get_result_message(self.selected_key))

    def get_result_message(self, key):
        if key == 'a':
            return "ثوم"
        elif key == 's':
            return "بصل"
        elif key == 'd':
            return "رائحة الصباح"
        elif key == 'f':
            return "غير معروفة"
        else:
            return "غير متوفرة"

    def show_result_window(self, result_text):
        def restart():
            self.result_win.close()
            self.start_reading()

        def back_home():
            self.result_win.close()
            self.close()

        image_map = {
            "ثوم": "garlic.png",
            "بصل": "onion.png",
            "رائحة الصباح": "morning.png",
            "غير معروفة": "unknown.png",

        }

        image_file = image_map.get(result_text, "unknown.png")
        self.result_win = ResultWindow(result_text, image_file, restart, back_home)
        self.result_win.show()
