import csv
from PyQt5 import QtWidgets, QtCore
from database.db_mgr import DatabaseManager
from datetime import datetime, timedelta
from ui.stat_page import StatWindow
from PyQt5.QtWidgets import QFileDialog

class MainPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.current_date = datetime.now().date()  # Track the current displayed date
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Inventory Management System")
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        form_layout = self.addEntries()
        button_layout = self.addButtons()
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.addHistoryTable()
        layout.addWidget(self.history_stats)
        layout.addWidget(self.history_table)

        self.setGeometry(300, 300, 800, 600)
        self.show()

        self.update_statistics(self.current_date)

    def addEntries(self):
        form_layout = QtWidgets.QFormLayout()

        self.item_name = QtWidgets.QLineEdit()
        form_layout.addRow("物品名:", self.item_name)

        self.unit = QtWidgets.QComboBox()
        self.unit.addItems(["kg", "ml"])
        form_layout.addRow("单位:", self.unit)

        self.quantity_entry = QtWidgets.QLineEdit()
        form_layout.addRow("规格:", self.quantity_entry)

        self.amount_entry = QtWidgets.QLineEdit()
        form_layout.addRow("数量:", self.amount_entry)

        self.price_entry = QtWidgets.QLineEdit()
        form_layout.addRow("价格:", self.price_entry)

        # Date picker for selecting specific dates
        self.date_selector = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.date_selector.setCalendarPopup(True)
        self.date_selector.dateChanged.connect(self.on_date_changed)
        form_layout.addRow("选择日期:", self.date_selector)

        return form_layout

    def addButtons(self):
        button_layout = QtWidgets.QHBoxLayout()

        self.add_button = QtWidgets.QPushButton("进库")
        self.add_button.clicked.connect(self.add_item)
        button_layout.addWidget(self.add_button)

        self.remove_button = QtWidgets.QPushButton("出库")
        self.remove_button.clicked.connect(self.remove_item)
        button_layout.addWidget(self.remove_button)

        # Modify selected item
        self.modify_button = QtWidgets.QPushButton("修改条目")
        self.modify_button.clicked.connect(self.modify_item)
        button_layout.addWidget(self.modify_button)

        # Export table to CSV
        self.export_button = QtWidgets.QPushButton("导出 CSV")
        self.export_button.clicked.connect(self.export_to_csv)
        button_layout.addWidget(self.export_button)

        self.previous_button = QtWidgets.QPushButton("前一天")
        self.previous_button.clicked.connect(self.show_previous_day)
        button_layout.addWidget(self.previous_button)

        self.next_button = QtWidgets.QPushButton("后一天")
        self.next_button.clicked.connect(self.show_next_day)
        button_layout.addWidget(self.next_button)

        self.stats_button = QtWidgets.QPushButton("统计")
        self.stats_button.clicked.connect(self.show_statistics_page)
        button_layout.addWidget(self.stats_button)

        return button_layout

    def addHistoryTable(self):
        self.history_stats = QtWidgets.QLabel("")
        self.history_table = QtWidgets.QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels(["物品名", "单位", "规格", "数量", "价格", "添加时间"])
        self.history_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.history_table.setSortingEnabled(True)
        self.history_table.itemSelectionChanged.connect(self.populate_fields)

    def add_item(self):
        if not self.validate_inputs():
            return

        try:
            name = self.item_name.text()
            unit = self.unit.currentText()
            quantity_per_unit = float(self.quantity_entry.text())
            amount = float(self.amount_entry.text())
            price = float(self.price_entry.text())
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.db_manager.add_item(name, unit, quantity_per_unit, amount, price, date_time)
            QtWidgets.QMessageBox.information(self, "成功", "物品已成功添加!")
            self.update_statistics(self.current_date)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "错误", f"添加物品时出错: {e}")

    def remove_item(self):
        if not self.validate_inputs():
            return

        try:
            name = self.item_name.text()
            unit = self.unit.currentText()
            quantity_per_unit = float(self.quantity_entry.text())
            amount = float(self.amount_entry.text())
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.db_manager.log_removal(name, unit, quantity_per_unit, amount, date_time)
            QtWidgets.QMessageBox.information(self, "成功", "物品已成功出库!")
            self.update_statistics(self.current_date)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "错误", f"出库时出错: {e}")

    def modify_item(self):
        selected_row = self.history_table.currentRow()
        if selected_row < 0:
            QtWidgets.QMessageBox.warning(self, "选择错误", "请选择要修改的条目!")
            return

        try:
            name = self.item_name.text()
            unit = self.unit.currentText()
            quantity_per_unit = float(self.quantity_entry.text())
            amount = float(self.amount_entry.text())
            price = float(self.price_entry.text())
            date_time = self.history_table.item(selected_row, 5).text()  # Keep original time

            self.db_manager.update_item(name, unit, quantity_per_unit, amount, price, date_time)
            QtWidgets.QMessageBox.information(self, "成功", "条目已修改!")
            self.update_statistics(self.current_date)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "错误", f"修改条目时出错: {e}")

    def validate_inputs(self):
        if not self.item_name.text():
            QtWidgets.QMessageBox.warning(self, "输入错误", "物品名不能为空!")
            return False

        try:
            float(self.quantity_entry.text())
            float(self.amount_entry.text())
            float(self.price_entry.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "输入错误", "规格, 数量, 价格必须为有效数字!")
            return False

        return True

    def populate_fields(self):
        selected_row = self.history_table.currentRow()
        if selected_row < 0:
            return

        self.item_name.setText(self.history_table.item(selected_row, 0).text())
        self.unit.setCurrentText(self.history_table.item(selected_row, 1).text())
        self.quantity_entry.setText(self.history_table.item(selected_row, 2).text())
        self.amount_entry.setText(self.history_table.item(selected_row, 3).text())
        self.price_entry.setText(self.history_table.item(selected_row, 4).text())

    def export_to_csv(self):
        try:
            path, _ = QFileDialog.getSaveFileName(self, "导出 CSV", "", "CSV Files (*.csv)")
            if not path:
                return

            with open(path, mode="w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                headers = ["物品名", "单位", "规格", "数量", "价格", "添加时间"]
                writer.writerow(headers)

                for row in range(self.history_table.rowCount()):
                    row_data = [
                        self.history_table.item(row, 0).text(),
                        self.history_table.item(row, 1).text(),
                        self.history_table.item(row, 2).text(),
                        self.history_table.item(row, 3).text(),
                        self.history_table.item(row, 4).text(),
                        self.history_table.item(row, 5).text()
                    ]
                    writer.writerow(row_data)

            QtWidgets.QMessageBox.information(self, "成功", "历史条目已导出到 CSV 文件!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "错误", f"导出 CSV 时出错: {e}")

    def update_statistics(self, selected_date):
        try:
            from_date = datetime.combine(selected_date, datetime.min.time())
            to_date = from_date + timedelta(days=1)

            input_amount = {}
            output_amount = {}

            items = self.db_manager.fetch_all_items()
            self.history_table.setRowCount(0)

            for item in items:
                name, unit, quantity_per_unit, amount, price, date_time = item
                date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")

                if from_date <= date_time < to_date:
                    if name not in input_amount:
                        input_amount[name] = 0
                        output_amount[name] = 0

                    if amount > 0:
                        input_amount[name] += amount
                    else:
                        output_amount[name] -= amount

                    row_position = self.history_table.rowCount()
                    self.history_table.insertRow(row_position)
                    self.history_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(name))
                    self.history_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(unit))
                    self.history_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(quantity_per_unit)))
                    self.history_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(amount)))
                    self.history_table.setItem(row_position, 4, QtWidgets.QTableWidgetItem(str(price)))
                    self.history_table.setItem(row_position, 5, QtWidgets.QTableWidgetItem(date_time.strftime("%Y-%m-%d %H:%M:%S")))

            result = f"{selected_date.strftime('%Y-%m-%d')}的记录:\n"
            for name in input_amount:
                result += "{} - Input: {} {}, Output: {} {}\n".format(name, input_amount[name], self.unit.currentText(), output_amount[name], self.unit.currentText())

            self.history_stats.setText(result)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "错误", f"更新统计时出错: {e}")

    def on_date_changed(self):
        selected_date = self.date_selector.date().toPyDate()
        self.current_date = selected_date  # Update the current date
        self.update_statistics(selected_date)

    def show_previous_day(self):
        self.current_date = self.current_date - timedelta(days=1)
        self.date_selector.setDate(QtCore.QDate(self.current_date))
        self.update_statistics(self.current_date)

    def show_next_day(self):
        self.current_date = self.current_date + timedelta(days=1)
        self.date_selector.setDate(QtCore.QDate(self.current_date))
        self.update_statistics(self.current_date)

    def show_statistics_page(self):
        self.stat_window = StatWindow(self.db_manager)
        self.stat_window.show()
