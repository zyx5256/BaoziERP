from backend.day_stats_mgr import DayStatsMgr
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog
from datetime import datetime, timedelta
from utils.log import *
from utils.utils import *


class MainPageCtrl:
    def __init__(self, main_page_ui, db_manager, history_table, history_stats):
        self.ui = main_page_ui
        self.db_manager = db_manager
        self.current_date = datetime.now().date()
        self.day_stats_mgr = DayStatsMgr(history_table, history_stats)

    def update_statistics(self, items):
        self.day_stats_mgr.update_statistics(self.current_date, items)

    def add_item(self):
        input_lists = self.ui.get_string_of_inputs()
        if not input_lists:
            print("Error, fail to get input strings.")
            return

        print(f"New record received: {input_lists}")

        try:
            self.db_manager.add_item(*input_lists)
            self.ui.show_message(MsgLevel.INFO, "成功", "物品已成功添加!")
            print("Record added to DB")
            self.day_stats_mgr.update_statistics(self.current_date, self.db_manager.fetch_all_items())
        except Exception as e:
            self.ui.show_message(MsgLevel.ERROR, "错误", f"添加物品时出错: {e}")
            print("Add record to DB failed")

    def remove_item(self):
        input_lists = self.ui.get_string_of_inputs()
        if not input_lists:
            print("Error, fail to get input strings.")
            return

        input_lists[4] = -input_lists[4]  # neg the amount
        print(f"New record received: {input_lists}")

        try:
            self.db_manager.add_item(*input_lists)
            self.ui.show_message(MsgLevel.INFO, "成功", "物品已成功出库!")
            self.day_stats_mgr.update_statistics(self.current_date, self.db_manager.fetch_all_items())
        except Exception as e:
            self.ui.show_message(MsgLevel.ERROR, "错误", f"出库时出错: {e}")

    def modify_item(self):
        selected_row = self.ui.history_table.currentRow()
        if selected_row < 0:
            self.ui.show_message(MsgLevel.ERROR, "选择错误", "请选择要修改的条目!")
            return

        input_lists = self.ui.get_string_of_inputs()
        if not input_lists:
            print("Error, fail to get input strings.")
            return

        input_lists[-1] = self.ui.history_table.item(selected_row, 6).text()  # Keep original time
        print(f"New record received: {input_lists}")

        try:
            self.db_manager.update_item(*input_lists)  # TODO: add last modify time
            self.ui.show_message(MsgLevel.INFO, "成功", "条目已修改!")
            self.day_stats_mgr.update_statistics(self.current_date, self.db_manager.fetch_all_items())
        except Exception as e:
            self.ui.show_message(MsgLevel.ERROR, "错误", f"修改条目时出错: {e}")

    def show_previous_day(self):
        self.current_date = self.current_date - timedelta(days=1)
        self.ui.date_selector.setDate(QtCore.QDate(self.current_date))
        self.day_stats_mgr.update_statistics(self.current_date, self.db_manager.fetch_all_items())

    def show_next_day(self):
        self.current_date = self.current_date + timedelta(days=1)
        self.ui.date_selector.setDate(QtCore.QDate(self.current_date))
        self.day_stats_mgr.update_statistics(self.current_date, self.db_manager.fetch_all_items())

    def on_date_changed(self):
        selected_date = self.ui.date_selector.date().toPyDate()
        self.current_date = selected_date  # Update the current date
        self.day_stats_mgr.update_statistics(selected_date, self.db_manager.fetch_all_items())

    def show_statistics_page(self):
        self.ui.stat_window.show()

    def export_to_csv(self):
        try:
            path, _ = QFileDialog.getSaveFileName(self.ui.main_page, "导出CSV", "", "CSV Files (*.csv)")
            if not path:
                return

            FileExporter.export_to_csv(path, self.ui.columns, self.ui.history_table)
            self.ui.show_message(MsgLevel.INFO, "成功", "历史条目已导出到 CSV 文件!")
        except Exception as e:
            self.ui.show_message(MsgLevel.ERROR, "错误", f"导出 CSV 时出错: {e}")
