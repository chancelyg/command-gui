import sys
import sys
from window import Window
from PyQt6.QtWidgets import QApplication

CONST_VERSION = 'V1.0.0'

app = QApplication(sys.argv)
window = Window()
window.show()

sys.exit(app.exec())