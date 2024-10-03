import csv

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class FileExporter:
    @staticmethod
    def export_to_csv(path, headers, data):
        with open(path, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(headers)

            for row in range(data.rowCount()):
                row_data = [data.item(row, i).text() for i in range(len(headers))]
                writer.writerow(row_data)
