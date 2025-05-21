import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from reading_window import ReadingWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("مستكشف الروائح الذكي")
        self.setGeometry(300, 100, 700, 500)
        self.setStyleSheet("background-color: #2e2e2e; color: white;")

        content_layout = QHBoxLayout()

        # صورة جانبية
        self.image_label = QLabel()
        pixmap = QPixmap("person.png")  # تأكد أن الصورة موجودة
        self.image_label.setPixmap(pixmap.scaled(250, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignCenter)

        # عنوان
        self.title_label = QLabel("مستشعر\nالروائح الذكي")
        self.title_label.setFont(QFont("Arial", 28, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)

        content_layout.addWidget(self.image_label)
        content_layout.addWidget(self.title_label)

        # زر بدء القراءة
        self.toggle_btn = QPushButton("بدء القراءة")
        self.toggle_btn.setFont(QFont("Arial", 18, QFont.Bold))
        self.toggle_btn.setFixedSize(300, 60)
        self.toggle_btn.setStyleSheet("background-color: #444; color: white; border-radius: 10px;")
        self.toggle_btn.clicked.connect(self.open_reading_window)

        main_layout = QVBoxLayout()
        main_layout.addLayout(content_layout)
        main_layout.addStretch()
        main_layout.addWidget(self.toggle_btn, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)
        self.reading_window = None

    def open_reading_window(self):
        if self.reading_window is None:
            self.reading_window = ReadingWindow()
        self.reading_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
