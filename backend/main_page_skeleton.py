import csv
from database.db_mgr import DatabaseManager
from datetime import datetime, timedelta
from ui.stat_page import StatWindow, TIME_FORMAT
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog
from enum import Enum


class MsgLevel(Enum):
    INFO = 1
    WARN = 2
    ERROR = 3


# Qt Encapsulation
def add_button(name, action):
    button = QtWidgets.QPushButton(name)
    button.clicked.connect(action)
    return button


class MainPageSkeleton:
    def __init__(self, main_page):
        # constants
        self.columns = ["物品名", "种类", "规格", "单位", "数量", "单价", "日期"]
        self.category_list = ["成品", "商品", "原辅料"]
        self.unit_list = ["kg", "g", "l", "ml", "个"]

        # main page
        self.main_page = main_page

        # database
        self.db_manager = DatabaseManager()

        # displays
        self.current_date = datetime.now().date()
        self.history_stats = QtWidgets.QLabel("")
        self.history_table = QtWidgets.QTableWidget()
        self.stat_window = StatWindow(self.db_manager, self.columns)

        # entries
        self.item_name = QtWidgets.QLineEdit()
        self.category = QtWidgets.QComboBox()
        self.quantity_entry = QtWidgets.QLineEdit()
        self.unit = QtWidgets.QComboBox()
        self.amount_entry = QtWidgets.QLineEdit()
        self.price_entry = QtWidgets.QLineEdit()

        self.date_selector = QtWidgets.QDateEdit(QtCore.QDate.currentDate())

        # buttons
        self.add_item = add_button("进库", self.add_item)
        self.remove_item = add_button("出库", self.remove_item)
        self.modify_item = add_button("修改条目", self.modify_item)
        self.export_to_csv = add_button("导出CSV", self.export_to_csv)
        self.show_previous_day = add_button("前一天", self.show_previous_day)
        self.show_next_day = add_button("后一天", self.show_next_day)
        self.show_statistics_page = add_button("统计页面", self.show_statistics_page)

        # init data
        self.init_data()
        self.entries = [self.item_name, self.category, self.quantity_entry, self.unit, self.amount_entry,
                        self.price_entry, self.date_selector]
        self.buttons = [self.add_item, self.remove_item, self.modify_item, self.export_to_csv, self.show_previous_day,
                        self.show_next_day, self.show_statistics_page]

        self.update_statistics(self.current_date)

    def init_data(self):
        self.category.addItems(self.category_list)
        self.unit.addItems(self.unit_list)

        self.date_selector.setCalendarPopup(True)
        self.date_selector.dateChanged.connect(self.on_date_changed)

        self.history_table.setColumnCount(len(self.columns))
        self.history_table.setHorizontalHeaderLabels(self.columns)
        self.history_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.history_table.setSortingEnabled(True)
        self.history_table.itemSelectionChanged.connect(self.populate_fields)

    def pop_up_msg(self, level, title, msg):
        msg_func = None
        if level == MsgLevel.INFO:
            msg_func = QtWidgets.QMessageBox.information
        elif level == MsgLevel.WARN:
            msg_func = QtWidgets.QMessageBox.warning
        elif level == MsgLevel.ERROR:
            msg_func = QtWidgets.QMessageBox.critical
        else:
            print(f"level not exist: {level}")
            return
        msg_func(self.main_page, title, msg)

    def validate_inputs(self):
        if not self.item_name.text():
            self.pop_up_msg(MsgLevel.WARN, "输入错误", "物品名不能为空!")
            return False

        try:
            float(self.quantity_entry.text())
            float(self.amount_entry.text())
            float(self.price_entry.text())
        except ValueError:
            self.pop_up_msg(MsgLevel.WARN, "输入错误", "规格, 数量, 价格必须为有效数字!")
            return False

        return True

    def get_string_of_inputs(self):
        if not self.validate_inputs():
            return None

        name = self.item_name.text()
        category = self.category.currentText()
        quantity_per_unit = float(self.quantity_entry.text())
        unit = self.unit.currentText()
        amount = float(self.amount_entry.text())
        price = float(self.price_entry.text())
        first_add_time = datetime.now().strftime(TIME_FORMAT)

        return [name, category, quantity_per_unit, unit, amount, price, first_add_time]

    def add_item(self):
        input_lists = self.get_string_of_inputs()
        if not input_lists:
            print("Error, fail to get input strings.")
            return

        print(f"New record received: {input_lists}")

        try:
            self.db_manager.add_item(*input_lists)
            self.pop_up_msg(MsgLevel.INFO, "成功", "物品已成功添加!")
            print("Record added to DB")
            self.update_statistics(self.current_date)
        except Exception as e:
            self.pop_up_msg(MsgLevel.ERROR, "错误", f"添加物品时出错: {e}")
            print("Add record to DB failed")

    def remove_item(self):
        input_lists = self.get_string_of_inputs()
        if not input_lists:
            print("Error, fail to get input strings.")
            return

        input_lists[4] = -input_lists[4]  # neg the amount
        print(f"New record received: {input_lists}")

        try:
            self.db_manager.add_item(*input_lists)
            self.pop_up_msg(MsgLevel.INFO, "成功", "物品已成功出库!")
            self.update_statistics(self.current_date)
        except Exception as e:
            self.pop_up_msg(MsgLevel.ERROR, "错误", f"出库时出错: {e}")

    def modify_item(self):
        selected_row = self.history_table.currentRow()
        if selected_row < 0:
            self.pop_up_msg(MsgLevel.ERROR, "选择错误", "请选择要修改的条目!")
            return

        input_lists = self.get_string_of_inputs()
        if not input_lists:
            print("Error, fail to get input strings.")
            return

        input_lists[-1] = self.history_table.item(selected_row, 6).text()  # Keep original time
        print(f"New record received: {input_lists}")

        try:
            self.db_manager.update_item(*input_lists)  # TODO: add last modify time
            self.pop_up_msg(MsgLevel.INFO, "成功", "条目已修改!")
            self.update_statistics(self.current_date)
        except Exception as e:
            self.pop_up_msg(MsgLevel.ERROR, "错误", f"修改条目时出错: {e}")

    def show_previous_day(self):
        self.current_date = self.current_date - timedelta(days=1)
        self.date_selector.setDate(QtCore.QDate(self.current_date))
        self.update_statistics(self.current_date)

    def show_next_day(self):
        self.current_date = self.current_date + timedelta(days=1)
        self.date_selector.setDate(QtCore.QDate(self.current_date))
        self.update_statistics(self.current_date)

    def on_date_changed(self):
        selected_date = self.date_selector.date().toPyDate()
        self.current_date = selected_date  # Update the current date
        self.update_statistics(selected_date)

    def show_statistics_page(self):
        self.stat_window.show()

    def export_to_csv(self):
        try:
            path, _ = QFileDialog.getSaveFileName(self.main_page, "导出CSV", "", "CSV Files (*.csv)")
            if not path:
                return

            with open(path, mode="w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                writer.writerow(self.columns)

                for row in range(self.history_table.rowCount()):
                    row_data = [self.history_table.item(row, i).text() for i in range(len(self.columns))]
                    writer.writerow(row_data)

            self.pop_up_msg(MsgLevel.INFO, "成功", "历史条目已导出到 CSV 文件!")
        except Exception as e:
            self.pop_up_msg(MsgLevel.ERROR, "错误", f"导出 CSV 时出错: {e}")

    def populate_fields(self):
        selected_row = self.history_table.currentRow()
        if selected_row < 0:
            return

        self.item_name.setText(self.history_table.item(selected_row, 0).text())
        self.category.setCurrentText(self.history_table.item(selected_row, 1).text())
        self.quantity_entry.setText(self.history_table.item(selected_row, 2).text())
        self.unit.setCurrentText(self.history_table.item(selected_row, 3).text())
        self.amount_entry.setText(self.history_table.item(selected_row, 4).text())
        self.price_entry.setText(self.history_table.item(selected_row, 5).text())
        # TODO: Add last modify time

    def update_cur_prod_stats(self, items):
        input_amount = {}
        output_amount = {}
        name_unit = {}

        for item in items:
            name, category, _, unit, amount, _, _ = item

            if not category == "成品":
                continue

            name_unit[name] = unit

            if name not in input_amount:
                input_amount[name] = 0
                output_amount[name] = 0

            if amount > 0:
                input_amount[name] += amount
            else:
                output_amount[name] -= amount

        result = f"该日成品统计:\n"
        for name in input_amount:
            result += f"{name} - Input: {input_amount[name]} {name_unit[name]}, " \
                      f"Output: {output_amount[name]} {name_unit[name]}\n"

        self.history_stats.setText(result)

    def update_history_table(self, items):
        for item in items:
            next_row_pos = self.history_table.rowCount()
            self.history_table.insertRow(next_row_pos)
            for i in range(len(item)):
                self.history_table.setItem(next_row_pos, i, QtWidgets.QTableWidgetItem(str(item[i])))

    def update_statistics(self, selected_date):
        items = self.db_manager.fetch_all_items()

        from_date = datetime.combine(selected_date, datetime.min.time())
        to_date = from_date + timedelta(days=1)
        items = [item for item in items if from_date <= datetime.strptime(item[6], TIME_FORMAT) < to_date]

        self.history_table.setRowCount(0)
        self.update_cur_prod_stats(items)
        self.update_history_table(items)

