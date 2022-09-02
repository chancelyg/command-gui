import os
import sys
import argparse
from window import Window
from PyQt6.QtWidgets import QApplication

CONST_PROGRAMS = 'command-gui'
CONST_VERSION = 'v0.9'

parser = argparse.ArgumentParser(description='command gui')
parser.add_argument('--data', '-d', help='data file', default='./command-gui-data')
args = parser.parse_args()

if args.data == './command-gui-data':
    args.data = os.path.join(os.getcwd(), 'command-gui-data')

app = QApplication(sys.argv)
window = Window(cache_path=args.data)
window.setWindowTitle('%s - %s' % (CONST_PROGRAMS, CONST_VERSION))
window.show()

sys.exit(app.exec())