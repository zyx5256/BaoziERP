from PyQt5 import QtWidgets, QtCore
from datetime import datetime


class StatWindow(QtWidgets.QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Statistics")

        layout = QtWidgets.QVBoxLayout(self)

        form_layout = QtWidgets.QFormLayout()
        layout.addLayout(form_layout)

        self.from_entry = QtWidgets.QDateEdit(calendarPopup=True)
        self.from_entry.setDateTime(QtCore.QDateTime.currentDateTime())
        form_layout.addRow("From Date:", self.from_entry)

        self.to_entry = QtWidgets.QDateEdit(calendarPopup=True)
        self.to_entry.setDateTime(QtCore.QDateTime.currentDateTime())
        form_layout.addRow("To Date:", self.to_entry)

        self.calculate_button = QtWidgets.QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_stats)
        layout.addWidget(self.calculate_button)

        self.result_table = QtWidgets.QTableWidget()
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels(["物品名", "单位", "规格", "数量", "价格", "添加时间"])
        self.result_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.result_table.setSortingEnabled(True)
        layout.addWidget(self.result_table)

        self.setGeometry(300, 300, 800, 400)
        self.show()

    def calculate_stats(self):
        try:
            from_date = self.from_entry.dateTime().toPyDateTime().replace(hour=0, minute=0, second=0, microsecond=0)
            to_date = self.to_entry.dateTime().toPyDateTime().replace(hour=23, minute=59, second=59, microsecond=999999)

            input_amount = {}
            output_amount = {}

            self.result_table.setRowCount(0)  # Clear the table

            items = self.db_manager.fetch_all_items()
            for item in items:
                name, unit, quantity_per_unit, amount, price, date_time = item
                date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")

                if from_date <= date_time <= to_date:
                    if name not in input_amount:
                        input_amount[name] = 0
                        output_amount[name] = 0

                    if amount > 0:
                        input_amount[name] += amount
                    else:
                        output_amount[name] -= amount

                    row_position = self.result_table.rowCount()
                    self.result_table.insertRow(row_position)
                    self.result_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(name))
                    self.result_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(unit))
                    self.result_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(quantity_per_unit)))
                    self.result_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(amount)))
                    self.result_table.setItem(row_position, 4, QtWidgets.QTableWidgetItem(str(price)))
                    self.result_table.setItem(row_position, 5, QtWidgets.QTableWidgetItem(date_time.strftime("%Y-%m-%d %H:%M:%S")))

            result = "Statistics from {} to {}:\n".format(from_date.date(), to_date.date())
            for name in input_amount:
                result += "{} - Input: {} {}, Output: {} {}\n".format(name, input_amount[name], unit, output_amount[name], unit)

            print(result)  # Debug print
        except Exception as e:
            print(f"Error occurred: {e}")