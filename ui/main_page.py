from PyQt5 import QtWidgets
from utils.log import logger, func_trace


class MainPage(QtWidgets.QMainWindow):
    def __init__(self, history_table, history_stats, columns, entries, buttons):
        super().__init__()
        self.title = "Inventory Management System"
        self.ax = 300
        self.ay = 300
        self.aw = 800
        self.ah = 600

        # data
        self.history_table = history_table
        self.history_stats = history_stats
        self.columns = columns
        self.entries = entries
        self.buttons = buttons

        self.setWindowTitle(self.title)
        self.setCentralWidget(QtWidgets.QWidget(self))
        self.init_layout()
        self.setGeometry(self.ax, self.ay, self.aw, self.ah)

        self.show()

    @func_trace
    def init_layout(self):
        layout = QtWidgets.QVBoxLayout(self.centralWidget())
        layout.addLayout(self.create_entry_layout())
        layout.addLayout(self.create_button_layout())
        layout.addWidget(self.history_stats)
        layout.addWidget(self.history_table)

    @func_trace
    def create_entry_layout(self):
        form_layout = QtWidgets.QFormLayout()
        entry_dict = dict(zip(self.columns, self.entries))

        for name, data in entry_dict.items():
            form_layout.addRow(name, data)

        logger.info("<-")
        return form_layout

    @func_trace
    def create_button_layout(self):
        button_layout = QtWidgets.QHBoxLayout()

        for button in self.buttons:
            button_layout.addWidget(button)

        logger.info("<-")
        return button_layout
