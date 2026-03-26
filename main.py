from PyQt6.QtWidgets import QApplication, QStackedWidget
import sys

from ui.login_ui import LoginUI
from ui.customer_ui import CustomerUI
from ui.analyze_ui import AnalyzeUI
from ui.register_ui import RegisterUI


class App(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.current_user = None
        self.customer_data = None

        self.addWidget(LoginUI(self))      # index 0
        self.addWidget(RegisterUI(self))   # index 1
        self.addWidget(CustomerUI(self))   # index 2
        self.addWidget(AnalyzeUI(self))    # index 3


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())