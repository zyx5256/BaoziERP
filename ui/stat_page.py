from PyQt5 import QtWidgets, QtCore
from datetime import datetime
from utils.utils import TIME_FORMAT
from utils.log import logger, func_trace


class StatWindow(QtWidgets.QWidget):
    def __init__(self, db_manager, columns):
        super().__init__()
        self.title = "Statistics"
        self.db_manager = db_manager

        self.setWindowTitle(self.title)
        self.init_ui(columns)

    @func_trace
    def init_ui(self, columns):
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
        self.result_table.setColumnCount(len(columns))
        self.result_table.setHorizontalHeaderLabels(columns)
        self.result_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.result_table.setSortingEnabled(True)
        layout.addWidget(self.result_table)

        self.setGeometry(300, 300, 800, 400)

    @func_trace
    def calculate_stats(self, checked=None):
        try:
            from_date = self.from_entry.dateTime().toPyDateTime().replace(hour=0, minute=0, second=0, microsecond=0)
            to_date = self.to_entry.dateTime().toPyDateTime().replace(hour=23, minute=59, second=59, microsecond=999999)

            self.result_table.setRowCount(0)  # Clear the table

            records = self.db_manager.fetch_all_records()
            logger.info(f"Filtering {len(records)} records in [{from_date}, {to_date}]")
            records = [record for record in records if from_date <= datetime.strptime(record[6], TIME_FORMAT) < to_date]
            logger.info(f"{len(records)} records after filtering: \n{records}")
            for record in records:
                row_position = self.result_table.rowCount()
                self.result_table.insertRow(row_position)
                for i in range(len(record)):
                    self.result_table.setItem(row_position, i, QtWidgets.QTableWidgetItem(str(record[i])))
                logger.info(f"Insert record {record} to result table at {row_position}")
        except Exception as e:
            logger.error(f"Calculate stats failed: {e}")
