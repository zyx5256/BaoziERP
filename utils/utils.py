import csv
from utils.log import logger, func_trace

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class FileExporter:
    @staticmethod
    @func_trace
    def export_to_csv(path, headers, data):
        try:
            with open(path, mode="w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                writer.writerow(headers)

                for row in range(data.rowCount()):
                    row_data = [data.item(row, i).text() for i in range(len(headers))]
                    writer.writerow(row_data)
        except Exception as e:
            logger.error(f"Try open and write data to {path} failed: {e}")
