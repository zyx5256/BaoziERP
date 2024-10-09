import sqlite3
from utils.log import logger, func_trace


class DatabaseManager:
    def __init__(self, db_name='inventory.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    @func_trace
    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                quantity_per_unit REAL,
                unit TEXT,
                amount REAL,
                price REAL,
                first_add_time TEXT
            )
        ''')
        self.conn.commit()

    @func_trace
    def add_record(self, name, category, quantity_per_unit, unit, amount, price, first_add_time):
        add_query = """
                    INSERT INTO inventory (name, category, quantity_per_unit, unit, amount, price, first_add_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """
        logger.info(f"Query: {add_query}")
        self.cursor.execute(add_query, (name, category, quantity_per_unit, unit, amount, price, first_add_time))
        self.conn.commit()
        logger.info("New record input updated to DB")

    @func_trace
    def update_record(self, name, category, quantity_per_unit, unit, amount, price, first_add_time):
        # Update the record in the database
        update_query = """
                       UPDATE inventory 
                       SET category = ?, quantity_per_unit = ?, unit = ?, amount = ?, price = ?
                       WHERE name = ? AND first_add_time = ?
                       """
        logger.info(f"Query: {update_query}")
        self.cursor.execute(update_query, (category, quantity_per_unit, unit, amount, price, name, first_add_time))
        self.conn.commit()

        if self.cursor.rowcount == 0:
            logger.info("New record modify updated to DB failed")
            logger.info("<-")
            return
        logger.info("New record modify updated to DB")

    @func_trace
    def fetch_all_records(self):
        fetch_query = 'SELECT name, category, quantity_per_unit, unit, amount, price, first_add_time FROM inventory'
        logger.info(f"Query: {fetch_query}")
        self.cursor.execute(fetch_query)
        record = self.cursor.fetchall()
        logger.info(f"Find record: {record}")
        return record
