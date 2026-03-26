from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QTextEdit, QLabel,
    QFrame, QHBoxLayout
)
from PyQt6.QtCore import Qt

from core.predict_service import run_prediction


class AnalyzeUI(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ===== CARD =====
        container = QFrame()
        container.setObjectName("card")
        container.setMinimumWidth(500)
        container.setMaximumWidth(650)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        # ===== TITLE =====
        title = QLabel("💰 Phân tích trả góp")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("title")

        subtitle = QLabel("AI đề xuất phương án thanh toán tối ưu")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setObjectName("subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ===== INPUT ROW (PRO STYLE) =====
        input_row = QHBoxLayout()

        self.amount = QLineEdit()
        self.amount.setPlaceholderText("Nhập số tiền (VD: 5,000)")
        self.amount.setObjectName("input")

        btn = QPushButton("Phân tích")
        btn.setObjectName("btnAnalyze")
        btn.clicked.connect(self.run)

        input_row.addWidget(self.amount)
        input_row.addWidget(btn)

        layout.addLayout(input_row)

        # ===== RESULT =====
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setObjectName("result")
        layout.addWidget(self.result)

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

            QLineEdit#input {
                padding: 12px;
                border-radius: 12px;
                border: 1px solid #ddd;
                font-size: 14px;
            }

            QLineEdit#input:focus {
                border: 2px solid #6C63FF;
                background-color: #f9f9ff;
            }

            QPushButton#btnAnalyze {
                background-color: #6C63FF;
                color: white;
                padding: 12px 18px;
                border-radius: 12px;
                font-weight: bold;
            }

            QPushButton#btnAnalyze:hover {
                background-color: #574fd6;
            }

            QTextEdit#result {
                background-color: #f8f8ff;
                border-radius: 12px;
                padding: 12px;
                font-size: 13px;
                border: 1px solid #eee;
            }
        """)

    # ===== LOGIC =====
    def run(self):
        text_input = self.amount.text().strip()

        if not text_input:
            self.show_result("❌ Bạn chưa nhập số tiền!")
            return

        try:
            amount = float(text_input.replace(",", ""))
        except ValueError:
            self.show_result("❌ Số tiền không hợp lệ!")
            return

        if not hasattr(self.app, "customer_data") or not self.app.customer_data:
            self.show_result("❌ Chưa có dữ liệu khách hàng!")
            return

        try:
            results = run_prediction(
                self.app.current_user,
                self.app.customer_data,
                amount
            )

            if not results:
                self.show_result("❌ Không có kết quả!")
                return

            text = "📊 TOP PHƯƠNG ÁN TỐT NHẤT\n\n"

            for i, r in enumerate(results[:5], 1):
                text += (
                    f"{i}. {r['months']} tháng\n"
                    f"   💵 {r['monthly']:,.0f} USD / tháng\n"
                    f"   ⚠️ Risk: {r['risk']:.4f}\n\n"
                )

            self.show_result(text)

        except Exception as e:
            print("DEBUG ERROR:", e)
            self.show_result(f"❌ Lỗi hệ thống:\n{str(e)}")

    def show_result(self, text):
        self.result.setText(text)