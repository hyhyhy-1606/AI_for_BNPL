from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QComboBox,
    QFrame, QGridLayout
)
from PyQt6.QtCore import Qt
from core.customer_service import save_customer


class CustomerUI(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ===== CARD =====
        container = QFrame()
        container.setObjectName("card")
        container.setMinimumWidth(600)   # rộng hơn
        container.setMaximumWidth(750)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # ===== TITLE =====
        title = QLabel("📊 Nhập thông tin khách hàng")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("title")
        layout.addWidget(title)

        # ===== GRID FORM =====
        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(12)

        # ===== STYLE =====
        input_style = """
            QLineEdit, QComboBox {
                padding: 10px;
                border-radius: 10px;
                border: 1px solid #ddd;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #6C63FF;
                background-color: #f9f9ff;
            }
        """

        def input_box(placeholder):
            w = QLineEdit()
            w.setPlaceholderText(placeholder)
            w.setStyleSheet(input_style)
            return w

        def combo_box(items):
            w = QComboBox()
            w.addItems(items)
            w.setStyleSheet(input_style)
            return w

        # ===== INPUT =====
        self.age = input_box("Tuổi")
        self.income = input_box("Thu nhập")
        self.score = input_box("Credit Score")
        self.amount = input_box("Số tiền mua hàng hàng ngày")
        self.checkout = input_box("Checkout (s)")

        self.gender = combo_box(["Nam", "Nữ"])
        self.category = combo_box(["Electronics", "Fashion", "Home"])
        self.provider = combo_box(["Klarna", "Afterpay", "Affirm"])
        self.device = combo_box(["Mobile", "Desktop"])
        self.connection = combo_box(["WiFi", "4G/5G"])
        self.browser = combo_box(["Chrome", "Firefox", "Safari"])

        # ===== ADD TO GRID (2 CỘT) =====
        fields = [
            ("Tuổi", self.age),
            ("Thu nhập", self.income),
            ("Credit Score", self.score),
            ("Số tiền", self.amount),
            ("Checkout", self.checkout),
            ("Giới tính", self.gender),
            ("Danh mục", self.category),
            ("Provider", self.provider),
            ("Thiết bị", self.device),
            ("Kết nối", self.connection),
            ("Browser", self.browser),
        ]

        for i, (label_text, widget) in enumerate(fields):
            row = i // 2
            col = (i % 2) * 2

            label = QLabel(label_text)
            label.setObjectName("label")

            grid.addWidget(label, row, col)
            grid.addWidget(widget, row, col + 1)

        layout.addLayout(grid)

        # ===== MESSAGE =====
        self.msg = QLabel()
        self.msg.setObjectName("message")
        layout.addWidget(self.msg)

        # ===== BUTTON =====
        btn = QPushButton("Next →")
        btn.setObjectName("btnNext")
        btn.clicked.connect(self.next)
        layout.addWidget(btn)

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
                border-radius: 18px;
            }

            #title {
                font-size: 22px;
                font-weight: bold;
                color: #6C63FF;
            }

            #label {
                font-size: 13px;
                font-weight: 500;
                color: #333;
            }

            #message {
                color: red;
                font-size: 13px;
            }

            QPushButton#btnNext {
                background-color: #6C63FF;
                color: white;
                padding: 12px;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton#btnNext:hover {
                background-color: #574fd6;
            }
        """)

    # ===== LOGIC GIỮ NGUYÊN =====
    def next(self):
        try:
            age = int(self.age.text())
            income = float(self.income.text())
            score = int(self.score.text())
            amount = float(self.amount.text())
            checkout = int(self.checkout.text())
        except:
            self.msg.setText("❌ Nhập sai định dạng!")
            return

        if age < 18 or age > 100:
            self.msg.setText("❌ Tuổi không hợp lệ!")
            return

        if income <= 0:
            self.msg.setText("❌ Thu nhập phải > 0!")
            return

        if score < 300 or score > 900:
            self.msg.setText("❌ Credit score không hợp lệ!")
            return

        if amount <= 0:
            self.msg.setText("❌ Số tiền phải > 0!")
            return

        if checkout <= 0:
            self.msg.setText("❌ Thời gian checkout không hợp lệ!")
            return

        customer = {
            'Customer_Age': age,
            'Annual_Income': income,
            'Credit_Score': score,
            'Purchase_Amount': amount,
            'Checkout_Time_Seconds': checkout,

            'Gender': self.gender.currentIndex(),
            'Purchase_Category': self.category.currentIndex(),
            'BNPL_Provider': self.provider.currentIndex(),
            'Device_Type': self.device.currentIndex(),
            'Connection_Type': self.connection.currentIndex(),
            'Browser': self.browser.currentIndex()
        }

        save_customer(self.app.current_user, customer)

        self.app.customer_data = customer
        self.app.setCurrentIndex(3)