from datetime import datetime, timedelta
from PyQt5 import QtWidgets
from utils.utils import TIME_FORMAT


class DayStatsMgr:
    def __init__(self, history_table, history_stats):
        self.history_table = history_table
        self.history_stats = history_stats
        return

    def update_cur_prod_stats(self, records):
        input_amount = {}
        output_amount = {}
        name_unit = {}

        for record in records:
            name, category, _, unit, amount, _, _ = record

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

    def update_history_table(self, records):
        for record in records:
            next_row_pos = self.history_table.rowCount()
            self.history_table.insertRow(next_row_pos)
            for i in range(len(record)):
                self.history_table.setItem(next_row_pos, i, QtWidgets.QTableWidgetItem(str(record[i])))

    def update_statistics(self, selected_date, records):
        from_date = datetime.combine(selected_date, datetime.min.time())
        to_date = from_date + timedelta(days=1)
        records = [record for record in records if from_date <= datetime.strptime(record[6], TIME_FORMAT) < to_date]

        self.history_table.setRowCount(0)
        self.update_cur_prod_stats(records)
        self.update_history_table(records)
