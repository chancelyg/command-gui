import subprocess
from PyQt6 import QtWidgets
from PyQt6.QtGui import QFont, QIcon, QAction
from diskcache import Cache

from utils import get_resource


class _AddDialog(QtWidgets.QDialog):

    def __init__(self, name: str = '', command: str = '') -> None:
        super().__init__()
        self.setWindowTitle("command-gui")
        self.setFixedSize(500, 200)
        self.layout = QtWidgets.QVBoxLayout()

        self._name_label = QtWidgets.QLabel(text='Command Name')
        self._name_label.setFont(QFont("Noto Sans", 10))
        self.layout.addWidget(self._name_label)

        self.name_line = QtWidgets.QLineEdit()
        self.name_line.setFont(QFont("Noto Sans", 14))
        self.name_line.setText(name)
        self.layout.addWidget(self.name_line)

        self._command_label = QtWidgets.QLabel(text='Command Value')
        self._command_label.setFont(QFont("Noto Sans", 10))
        self.layout.addWidget(self._command_label)

        self.command_line = QtWidgets.QLineEdit()
        self.command_line.setFont(QFont("Noto Sans", 14))
        self.command_line.setText(command)
        self.layout.addWidget(self.command_line)

        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok
                                                    | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class Window(QtWidgets.QWidget):

    def __init__(self, cache_path: str):
        super().__init__()
        self.setWindowTitle("command-gui")
        self.setWindowIcon(QIcon(get_resource("command-gui.ico")))
        self.setFixedSize(450, 900)

        self._vbox_main_layout = QtWidgets.QVBoxLayout()

        self._label_commands = QtWidgets.QLabel(text='Commands')
        self._label_commands.setFont(QFont("Noto Sans", 18))
        self._vbox_main_layout.addWidget(self._label_commands)

        self._list_widget = QtWidgets.QListWidget()
        self._list_widget.doubleClicked.connect(self._excute_command)
        self._list_widget.setToolTip('double click run this command')
        self.setFont(QFont("Noto Sans", 16))
        self._vbox_main_layout.addWidget(self._list_widget)

        self._run_button = QtWidgets.QPushButton(text='Run')
        self._run_button.clicked.connect(self._excute_command)
        self._run_button.setStyleSheet("background-color: green")
        self._run_button.setFont(QFont("Noto Sans", 14))
        self._vbox_main_layout.addWidget(self._run_button)

        self._form_layout = QtWidgets.QHBoxLayout()
        self._add_button = QtWidgets.QPushButton(text='add')
        self._add_button.setStyleSheet("background-color: blue")
        self._add_button.setFont(QFont("Noto Sans", 10))
        self._add_button.clicked.connect(self._add_click)
        self._edit_button = QtWidgets.QPushButton(text='edit')
        self._edit_button.setStyleSheet("background-color: blue")
        self._edit_button.setFont(QFont("Noto Sans", 10))
        self._edit_button.clicked.connect(self._edit_click)
        self._remove_button = QtWidgets.QPushButton(text='remove')
        self._remove_button.setStyleSheet("background-color: red")
        self._remove_button.setFont(QFont("Noto Sans", 10))
        self._remove_button.clicked.connect(self._delete_click)
        self._form_layout.addWidget(self._add_button)
        self._form_layout.addWidget(self._edit_button)
        self._form_layout.addWidget(self._remove_button)
        self._vbox_main_layout.addLayout(self._form_layout)

        # set the layout for the main window
        self.setLayout(self._vbox_main_layout)

        # set tray
        self._tray = QtWidgets.QSystemTrayIcon()
        self._tray.setIcon(QIcon(get_resource('command-gui.ico')))
        self._tray.setVisible(True)
        self._tray.setToolTip('command-gui')
        self._tray_menu = QtWidgets.QMenu()
        self._tray_menu.setFont(QFont("Noto Sans", 18))
        self._qt_action = QAction('Quit command-gui')
        self._qt_action.triggered.connect(self.quit)
        self._tray_menu.addAction(self._qt_action)
        self._tray.setContextMenu(self._tray_menu)
        self._tray.activated.connect(self.show)

        self._cache = Cache(cache_path)
        self._update_list_widget()

        self._exit_flag = False

    def _excute_command(self):
        item = self._list_widget.currentItem()
        try:
            command = [_ for _ in self._cache.get(item.text()).split(' ')]
            subprocess.Popen(command)
        except Exception:
            pass

    def _add_click(self):
        add_dialog = _AddDialog()
        if add_dialog.exec() and add_dialog.name_line.text() and add_dialog.command_line.text():
            self._cache.set(add_dialog.name_line.text(), add_dialog.command_line.text())
            self._update_list_widget()

    def _edit_click(self):
        item = self._list_widget.currentItem()
        if item:
            add_dialog = _AddDialog(name=item.text(), command=self._cache.get(item.text()))
            if add_dialog.exec() and add_dialog.name_line.text() and add_dialog.command_line.text():
                self._cache.set(add_dialog.name_line.text(), add_dialog.command_line.text())
                self._update_list_widget()

    def _delete_click(self):
        if self._list_widget.currentItem():
            self._cache.delete(self._list_widget.currentItem().text())
        self._update_list_widget()

    def _update_list_widget(self):
        self._list_widget.clear()
        for key in self._cache.iterkeys():
            self._list_widget.addItem(key)

    def closeEvent(self, event):
        if not self._exit_flag:
            self.setVisible(False)
            event.ignore()
        if self._exit_flag:
            event.accept()

    def quit(self):
        self._exit_flag = True
        self.close()