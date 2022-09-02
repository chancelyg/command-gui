import subprocess
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QLineEdit, QLabel, QDialog, QDialogButtonBox
from PyQt6.QtGui import QFont, QIcon
from diskcache import Cache


class _AddDialog(QDialog):

    def __init__(self, name: str = '', command: str = '') -> None:
        super().__init__()
        self.setWindowTitle("command-gui")
        self.setFixedSize(500, 200)
        self.layout = QVBoxLayout()

        self.name_label = QLabel(text='Command Name')
        self.layout.addWidget(self.name_label)

        self.name_line = QLineEdit()
        self.name_line.setText(name)
        self.layout.addWidget(self.name_line)

        self.command_label = QLabel(text='Command Value')
        self.layout.addWidget(self.command_label)

        self.command_line = QLineEdit()
        self.command_line.setText(command)
        self.layout.addWidget(self.command_line)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("command-gui")
        self.setWindowIcon(QIcon("command-gui.ico"))
        self.setGeometry(500, 200, 500, 400)

        # create vbox layout object
        vbox = QVBoxLayout()
        # create object of list_widget
        self.list_widget = QListWidget()
        # add items to the listwidget
        # self.list_widget.setStyleSheet('background-color:yellow')
        self.list_widget.doubleClicked.connect(self.item_clicked)
        self.setFont(QFont("Noto Sans", 12))
        # self.setStyleSheet('color:brown')

        # add widgets to the vboxlyaout
        vbox.addWidget(self.list_widget)

        self.add_button = QPushButton(text='Add Command')
        self.add_button.clicked.connect(self.add_click)
        self.edit_button = QPushButton(text='Edit Command')
        self.edit_button.clicked.connect(self.edit_click)
        self.remove_button = QPushButton(text='Remove Command')
        self.remove_button.clicked.connect(self.delete_click)
        vbox.addWidget(self.add_button)
        vbox.addWidget(self.edit_button)
        vbox.addWidget(self.remove_button)

        # set the layout for the main window
        self.setLayout(vbox)

        self._cache = Cache('command-gui')
        self._update_list_widget()

    def item_clicked(self):
        item = self.list_widget.currentItem()
        try:
            command = [_ for _ in self._cache.get(item.text()).split(' ')]
            subprocess.Popen(command)
        except Exception:
            pass

    def add_click(self):
        add_dialog = _AddDialog()
        if add_dialog.exec() and add_dialog.name_line.text() and add_dialog.command_line.text():
            self._cache.set(add_dialog.name_line.text(), add_dialog.command_line.text())
            self._update_list_widget()

    def edit_click(self):
        item = self.list_widget.currentItem()
        if item:
            add_dialog = _AddDialog(name=item.text(), command=self._cache.get(item.text()))
            if add_dialog.exec() and add_dialog.name_line.text() and add_dialog.command_line.text():
                self._cache.set(add_dialog.name_line.text(), add_dialog.command_line.text())
                self._update_list_widget()

    def delete_click(self):
        if self.list_widget.currentItem():
            self._cache.delete(self.list_widget.currentItem().text())
        self._update_list_widget()

    def _update_list_widget(self):
        self.list_widget.clear()
        for key in self._cache.iterkeys():
            self.list_widget.addItem(key)