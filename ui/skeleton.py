from database.db_mgr import DatabaseManager
from ui.stat_page import StatWindow
from ui.main_page import MainPage
from backend.main_page_controller import MainPageCtrl
from utils.utils import *
from utils.log import *
from PyQt5 import QtWidgets, QtCore
from datetime import datetime


class Skeleton:
    def __init__(self):
        # constants
        self.columns = ["物品名", "种类", "规格", "单位", "数量", "单价", "日期"]
        self.category_list = ["成品", "商品", "原辅料"]
        self.unit_list = ["kg", "g", "l", "ml", "个"]

        # database
        self.db_manager = DatabaseManager()

        # displays
        self.history_stats = QtWidgets.QLabel("")
        self.history_table = QtWidgets.QTableWidget()
        self.set_history_table()
        self.history_table.itemSelectionChanged.connect(self.populate_fields)

        # helpers
        self.controller = MainPageCtrl(self, self.db_manager, self.history_table, self.history_stats)

        # entries
        self.item_name = QtWidgets.QLineEdit()
        self.category = QtWidgets.QComboBox()
        self.quantity_entry = QtWidgets.QLineEdit()
        self.unit = QtWidgets.QComboBox()
        self.amount_entry = QtWidgets.QLineEdit()
        self.price_entry = QtWidgets.QLineEdit()
        self.date_selector = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.date_selector.setCalendarPopup(True)
        self.date_selector.dateChanged.connect(self.controller.on_date_changed)
        self.entries = [self.item_name, self.category, self.quantity_entry, self.unit, self.amount_entry,
                        self.price_entry, self.date_selector]

        # buttons
        self.add_record = self.add_button("进库", self.controller.add_record)
        self.remove_record = self.add_button("出库", self.controller.remove_record)
        self.modify_record = self.add_button("修改条目", self.controller.modify_record)
        self.export_to_csv = self.add_button("导出CSV", self.controller.export_to_csv)
        self.show_previous_day = self.add_button("前一天", self.controller.show_previous_day)
        self.show_next_day = self.add_button("后一天", self.controller.show_next_day)
        self.show_statistics_page = self.add_button("统计页面", self.controller.show_statistics_page)
        self.buttons = [self.add_record, self.remove_record, self.modify_record, self.export_to_csv,
                        self.show_previous_day, self.show_next_day, self.show_statistics_page]

        # pages
        self.main_page = MainPage(self.history_table, self.history_stats, self.columns, self.entries, self.buttons)
        self.stat_window = StatWindow(self.db_manager, self.columns)

        # init data
        self.category.addItems(self.category_list)
        self.unit.addItems(self.unit_list)

    @func_trace
    def set_history_table(self):
        self.history_table.setColumnCount(len(self.columns))
        self.history_table.setHorizontalHeaderLabels(self.columns)
        self.history_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.history_table.setSortingEnabled(True)

    @func_trace
    def add_button(self, name, action):
        button = QtWidgets.QPushButton(name)
        button.clicked.connect(action)
        return button

    @func_trace
    def show_message(self, level, title, msg):
        logger.info(f"Show message {title}:{msg}")
        msg_func = None
        if level == logging.INFO:
            msg_func = QtWidgets.QMessageBox.information
        elif level == logging.WARN:
            msg_func = QtWidgets.QMessageBox.warning
        elif level == logging.ERROR:
            msg_func = QtWidgets.QMessageBox.critical
        else:
            logger.error(f"level not exist: {level}")
            logger.info("<-")
            return
        msg_func(self.main_page, title, msg)

    @func_trace
    def validate_inputs(self):
        if not self.item_name.text():
            self.show_message(logging.WARN, "输入错误", "物品名不能为空!")
            logger.info("<-")
            return False

        try:
            float(self.quantity_entry.text())
            float(self.amount_entry.text())
            float(self.price_entry.text())
        except ValueError:
            self.show_message(logging.WARN, "输入错误", "规格, 数量, 价格必须为有效数字!")
            logger.info("<-")
            return False
        return True

    @func_trace
    def get_string_of_inputs(self):
        if not self.validate_inputs():
            logger.info("<-")
            return None

        name = self.item_name.text()
        category = self.category.currentText()
        quantity_per_unit = float(self.quantity_entry.text())
        unit = self.unit.currentText()
        amount = float(self.amount_entry.text())
        price = float(self.price_entry.text())
        first_add_time = datetime.now().strftime(TIME_FORMAT)

        logger.info("<-")
        return [name, category, quantity_per_unit, unit, amount, price, first_add_time]

    @func_trace
    def populate_fields(self):
        selected_row = self.history_table.currentRow()
        if selected_row < 0:
            logger.info("<-")
            return

        self.item_name.setText(self.history_table.item(selected_row, 0).text())
        self.category.setCurrentText(self.history_table.item(selected_row, 1).text())
        self.quantity_entry.setText(self.history_table.item(selected_row, 2).text())
        self.unit.setCurrentText(self.history_table.item(selected_row, 3).text())
        self.amount_entry.setText(self.history_table.item(selected_row, 4).text())
        self.price_entry.setText(self.history_table.item(selected_row, 5).text())
        # TODO: Add last modify time
