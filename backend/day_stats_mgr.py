from datetime import datetime, timedelta
from PyQt5 import QtWidgets
from utils.utils import TIME_FORMAT
from utils.log import logger, func_trace


class DayStatsMgr:
    def __init__(self, history_table, history_stats):
        self.history_table = history_table
        self.history_stats = history_stats
        return

    @func_trace
    def update_cur_prod_stats(self, records):
        logger.info(f"Got records size = {len(records)}")

        input_amount = {}
        output_amount = {}
        name_unit = {}

        for record in records:
            logger.info(f"Record: {record}")
            name, category, _, unit, amount, _, _ = record

            if not category == "成品":
                logger.info("Not a record of product, skip")
                continue

            name_unit[name] = unit

            if name not in input_amount:
                input_amount[name] = 0
                output_amount[name] = 0

            if amount > 0:
                logger.info(f"Add {amount} to current input amount {input_amount[name]} of product {name}")
                input_amount[name] += amount
            else:
                logger.info(f"Add {-amount} to current output amount {output_amount[name]} of product {name}")
                output_amount[name] -= amount

        result = f"该日成品统计:\n"
        for name in input_amount:
            result += f"{name} - Input: {input_amount[name]} {name_unit[name]}, " \
                      f"Output: {output_amount[name]} {name_unit[name]}\n"

        self.history_stats.setText(result)
        logger.info(f"Display history stats: \n{result}")

    @func_trace
    def update_history_table(self, records):
        logger.info(f"Got records size = {len(records)}")
        for record in records:
            next_row_pos = self.history_table.rowCount()
            self.history_table.insertRow(next_row_pos)
            for i in range(len(record)):
                self.history_table.setItem(next_row_pos, i, QtWidgets.QTableWidgetItem(str(record[i])))
            logger.info(f"Insert record {record} to history table at {next_row_pos}")

    @func_trace
    def update_statistics(self, selected_date, records):
        from_date = datetime.combine(selected_date, datetime.min.time())
        to_date = from_date + timedelta(days=1)
        logger.info(f"Selected date {selected_date}, filtering {len(records)} records in [{from_date}, {to_date}]")
        records = [record for record in records if from_date <= datetime.strptime(record[6], TIME_FORMAT) < to_date]
        logger.info(f"{len(records)} records after filtering: \n{records}")

        self.history_table.setRowCount(0)
        self.update_cur_prod_stats(records)
        self.update_history_table(records)
