from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QFrame, QHBoxLayout
)
from PyQt6.QtCore import Qt
from core.auth_service import login


class LoginUI(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ===== CARD =====
        container = QFrame()
        container.setObjectName("card")
        container.setMinimumWidth(360)
        container.setMaximumWidth(420)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(18)

        # ===== TITLE =====
        title = QLabel("🔐 Đăng nhập")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("title")

        subtitle = QLabel("Chào mừng bạn quay lại")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setObjectName("subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ===== INPUT STYLE =====
        input_style = """
            QLineEdit {
                padding: 12px;
                border-radius: 12px;
                border: 1px solid #ddd;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #6C63FF;
                background-color: #f9f9ff;
            }
        """

        def input_box(placeholder, password=False):
            w = QLineEdit()
            w.setPlaceholderText(placeholder)
            w.setStyleSheet(input_style)
            if password:
                w.setEchoMode(QLineEdit.EchoMode.Password)
            return w

        # ===== INPUT =====
        self.user = input_box("👤 Username")
        self.passwd = input_box("🔒 Password", True)

        layout.addWidget(self.user)
        layout.addWidget(self.passwd)

        # ===== MESSAGE =====
        self.msg = QLabel()
        self.msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msg.setObjectName("message")
        layout.addWidget(self.msg)

        # ===== BUTTON LOGIN =====
        btn_login = QPushButton("Đăng nhập")
        btn_login.setObjectName("btnLogin")
        btn_login.clicked.connect(self.handle_login)
        layout.addWidget(btn_login)

        # ===== REGISTER LINK =====
        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("Chưa có tài khoản?")
        btn_register = QPushButton("Đăng ký")
        btn_register.setObjectName("btnRegister")
        btn_register.clicked.connect(lambda: self.app.setCurrentIndex(1))

        bottom_layout.addWidget(label)
        bottom_layout.addWidget(btn_register)

        layout.addLayout(bottom_layout)

        main_layout.addWidget(container)
        self.setLayout(main_layout)

        # ===== STYLE =====
        self.setStyleSheet("""
            QWidget {
                background-color: #f3f2ff;
                font-family: Segoe UI;
            }

            #card {
                background-color: white;
                border-radius: 20px;
            }

            #title {
                font-size: 24px;
                font-weight: bold;
                color: #6C63FF;
            }

            #subtitle {
                font-size: 13px;
                color: #888;
            }

            #message {
                font-size: 13px;
                min-height: 18px;
                color: red;
            }

            QPushButton#btnLogin {
                background-color: #6C63FF;
                color: white;
                padding: 12px;
                border-radius: 12px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton#btnLogin:hover {
                background-color: #574fd6;
            }

            QPushButton#btnRegister {
                background-color: transparent;
                color: #6C63FF;
                border: none;
                font-size: 13px;
                font-weight: bold;
            }

            QPushButton#btnRegister:hover {
                text-decoration: underline;
            }
        """)

    # ===== LOGIC =====
    def handle_login(self):
        username = self.user.text().strip()
        password = self.passwd.text()

        if not username or not password:
            self.show_msg("❌ Không được để trống!")
            return

        user = login(username, password)

        if user:
            self.app.current_user = user["username"]
            self.app.setCurrentIndex(2)
        else:
            self.show_msg("❌ Sai tài khoản hoặc mật khẩu!")

    def show_msg(self, text):
        self.msg.setText(text)