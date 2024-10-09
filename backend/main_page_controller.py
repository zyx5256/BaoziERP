from backend.day_stats_mgr import DayStatsMgr
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog
from datetime import datetime, timedelta
from utils.utils import *
from utils.log import logger, func_trace
import logging


class MainPageCtrl:
    def __init__(self, main_page_ui, db_manager, history_table, history_stats):
        self.ui = main_page_ui
        self.db_manager = db_manager
        self.current_date = datetime.now().date()
        logger.info(f"Current date: {self.current_date}")
        self.day_stats_mgr = DayStatsMgr(history_table, history_stats)
        self.day_stats_mgr.update_statistics(self.current_date, self.db_manager.fetch_all_records())

    @func_trace
    def add_record(self, checked=None):
        logger.info("User operation")
        input_lists = self.ui.get_string_of_inputs()
        if not input_lists:
            logger.error("Fail to get input strings.")
            logger.info("<-")
            return

        logger.info(f"User input received: {input_lists}")

        try:
            self.db_manager.add_record(*input_lists)
            logger.info("AddRecord added to DB")
            self.ui.show_message(logging.INFO, "成功", "物品已成功添加!")
            self.day_stats_mgr.update_statistics(self.current_date, self.db_manager.fetch_all_records())
        except Exception as e:
            logger.error("Add AddRecord to DB failed")
            self.ui.show_message(logging.ERROR, "错误", f"添加物品时出错: {e}")

    @func_trace
    def remove_record(self, checked=None):
        logger.info("User operation")
        input_lists = self.ui.get_string_of_inputs()
        if not input_lists:
            logger.info("Fail to get input strings.")
            logger.info("<-")
            return

        input_lists[4] = -input_lists[4]  # neg the amount
        logger.info(f"New record received: {input_lists}")

        try:
            self.db_manager.add_record(*input_lists)
            logger.info("RemoveRecord added to DB")
            self.ui.show_message(logging.INFO, "成功", "物品已成功出库!")
            self.day_stats_mgr.update_statistics(self.current_date, self.db_manager.fetch_all_records())
        except Exception as e:
            logger.error("Add RemoveRecord to DB failed")
            self.ui.show_message(logging.ERROR, "错误", f"出库时出错: {e}")

    @func_trace
    def modify_record(self, checked=None):
        logger.info("User operation")
        selected_row = self.ui.history_table.currentRow()
        if selected_row < 0:
            self.ui.show_message(logging.ERROR, "选择错误", "请选择要修改的条目!")
            logger.info("<-")
            return

        input_lists = self.ui.get_string_of_inputs()
        if not input_lists:
            logger.error("Fail to get input strings.")
            logger.info("<-")
            return

        input_lists[-1] = self.ui.history_table.item(selected_row, 6).text()  # Keep original time
        logger.info(f"User input received for updating: {input_lists}")

        try:
            self.db_manager.update_record(*input_lists)  # TODO: add last modify time
            logger.info("ModifyRecord added to DB")
            self.ui.show_message(logging.INFO, "成功", "条目已修改!")
            self.day_stats_mgr.update_statistics(self.current_date, self.db_manager.fetch_all_records())
        except Exception as e:
            logger.error("Add ModifyRecord to DB failed")
            self.ui.show_message(logging.ERROR, "错误", f"修改条目时出错: {e}")

    @func_trace
    def show_previous_day(self, checked=None):
        logger.info("User operation")
        self.current_date = self.current_date - timedelta(days=1)
        logger.info(f"After delta, current date: {self.current_date}")
        self.ui.date_selector.setDate(QtCore.QDate(self.current_date))
        self.day_stats_mgr.update_statistics(self.current_date, self.db_manager.fetch_all_records())

    @func_trace
    def show_next_day(self, checked=None):
        logger.info("User operation")
        self.current_date = self.current_date + timedelta(days=1)
        logger.info(f"After delta, current date: {self.current_date}")
        self.ui.date_selector.setDate(QtCore.QDate(self.current_date))
        self.day_stats_mgr.update_statistics(self.current_date, self.db_manager.fetch_all_records())

    @func_trace
    def on_date_changed(self, checked=None):
        logger.info("User operation")
        selected_date = self.ui.date_selector.date().toPyDate()
        self.current_date = selected_date  # Update the current date
        logger.info(f"After delta, current date: {self.current_date}")
        self.day_stats_mgr.update_statistics(selected_date, self.db_manager.fetch_all_records())

    @func_trace
    def show_statistics_page(self, checked=None):
        logger.info("User operation")
        self.ui.stat_window.show()

    @func_trace
    def export_to_csv(self, checked=None):
        logger.info("User operation")
        try:
            path, _ = QFileDialog.getSaveFileName(self.ui.main_page, "导出CSV", "", "CSV Files (*.csv)")
            logger.info(f"Got path = {path}")
            if not path:
                logger.info("<-")
                return

            FileExporter.export_to_csv(path, self.ui.columns, self.ui.history_table)
            logger.info(f"CSV exported to {path}")
            self.ui.show_message(logging.INFO, "成功", f"历史条目已导出到 {path}")
        except Exception as e:
            logger.info(f"CSV export failed")
            self.ui.show_message(logging.ERROR, "错误", f"导出 CSV 时出错: {e}")
