from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class ResultWindow(QWidget):
    def __init__(self, result_text, image_path, on_retry, on_home):
        super().__init__()
        self.setWindowTitle("نتيجة القراءة")
        self.setGeometry(450, 250, 500, 500)
        self.setStyleSheet("background-color: #2e2e2e; color: white;")

        layout = QVBoxLayout()

        title = QLabel("تم التشخيص عن الرائحة")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        result = QLabel(f"الرائحة المكتشفة هي {result_text}")
        result.setFont(QFont("Arial", 16))
        result.setAlignment(Qt.AlignCenter)

        img_label = QLabel()
        pixmap = QPixmap(image_path)
        img_label.setPixmap(pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        img_label.setAlignment(Qt.AlignCenter)

        btn_home = QPushButton("العودة الى القائمة الرئيسية")
        btn_retry = QPushButton("إعادة المحاولة")

        for btn in (btn_retry, btn_home):
            btn.setFont(QFont("Arial", 12))
            btn.setFixedHeight(40)
            btn.setStyleSheet("background-color: #444; color: white; border-radius: 10px;")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_retry)
        btn_layout.addWidget(btn_home)

        btn_home.clicked.connect(on_home)
        btn_retry.clicked.connect(on_retry)

        layout.addWidget(title)
        layout.addWidget(result)
        layout.addWidget(img_label)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
