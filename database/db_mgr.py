import sqlite3


class DatabaseManager:
    def __init__(self, db_name='inventory.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

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

    def add_item(self, name, category, quantity_per_unit, unit, amount, price, first_add_time):
        add_query = """
                    INSERT INTO inventory (name, category, quantity_per_unit, unit, amount, price, first_add_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """

        self.cursor.execute(add_query, (name, category, quantity_per_unit, unit, amount, price, first_add_time))
        self.conn.commit()
        print("New record input updated to DB")

    def update_item(self, name, category, quantity_per_unit, unit, amount, price, first_add_time):
        # Update the item in the database
        update_query = """
                       UPDATE inventory 
                       SET category = ?, quantity_per_unit = ?, unit = ?, amount = ?, price = ?
                       WHERE name = ? AND first_add_time = ?
                       """
        self.cursor.execute(update_query, (category, quantity_per_unit, unit, amount, price, name, first_add_time))
        self.conn.commit()

        if self.cursor.rowcount == 0:
            print("New record modify updated to DB failed")
            return
        print("New record modify updated to DB")

    def fetch_all_items(self):
        fetch_query = 'SELECT name, category, quantity_per_unit, unit, amount, price, first_add_time FROM inventory'
        self.cursor.execute(fetch_query)
        return self.cursor.fetchall()
