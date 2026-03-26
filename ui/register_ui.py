from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QFrame, QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer
from core.auth_service import register


class RegisterUI(QWidget):
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
        title = QLabel("📝 Đăng ký tài khoản")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("title")

        subtitle = QLabel("Tạo tài khoản để tiếp tục")
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
        self.username = input_box("👤 Username")
        self.password = input_box("🔒 Password", True)
        self.confirm = input_box("🔒 Confirm Password", True)

        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.confirm)

        # ===== MESSAGE =====
        self.msg = QLabel()
        self.msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msg.setObjectName("message")
        layout.addWidget(self.msg)

        # ===== BUTTON REGISTER =====
        btn_register = QPushButton("Tạo tài khoản")
        btn_register.setObjectName("btnRegister")
        btn_register.clicked.connect(self.handle_register)
        layout.addWidget(btn_register)

        # ===== BACK LINK =====
        back_layout = QHBoxLayout()
        back_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        back_label = QLabel("Đã có tài khoản?")
        btn_back = QPushButton("Đăng nhập")
        btn_back.setObjectName("btnBack")
        btn_back.clicked.connect(self.go_back)

        back_layout.addWidget(back_label)
        back_layout.addWidget(btn_back)

        layout.addLayout(back_layout)

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
            }

            QPushButton#btnRegister {
                background-color: #6C63FF;
                color: white;
                padding: 12px;
                border-radius: 12px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton#btnRegister:hover {
                background-color: #574fd6;
            }

            QPushButton#btnBack {
                background-color: transparent;
                color: #6C63FF;
                border: none;
                font-size: 13px;
                font-weight: bold;
            }

            QPushButton#btnBack:hover {
                text-decoration: underline;
            }
        """)

    # ===== LOGIC =====
    def handle_register(self):
        username = self.username.text().strip()
        password = self.password.text()
        confirm = self.confirm.text()

        if not username or not password:
            self.show_msg("❌ Không được để trống!", "red")
            return

        if len(password) < 4:
            self.show_msg("❌ Password phải >= 4 ký tự!", "red")
            return

        if password != confirm:
            self.show_msg("❌ Mật khẩu không khớp!", "red")
            return

        success = register(username, password)

        if success:
            self.show_msg("✅ Đăng ký thành công!", "green")
            self.clear_form()
            QTimer.singleShot(1000, lambda: self.app.setCurrentIndex(0))
        else:
            self.show_msg("❌ Username đã tồn tại!", "red")

    def show_msg(self, text, color):
        self.msg.setText(text)
        self.msg.setStyleSheet(f"color: {color};")

    def clear_form(self):
        self.username.clear()
        self.password.clear()
        self.confirm.clear()

    def go_back(self):
        self.app.setCurrentIndex(0)