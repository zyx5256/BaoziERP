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
                unit TEXT,
                quantity_per_unit REAL,
                amount REAL,
                price REAL,
                date_time TEXT
            )
        ''')
        self.conn.commit()

    def add_item(self, name, unit, quantity_per_unit, amount, price, date_time):
        self.cursor.execute('''
            INSERT INTO inventory (name, unit, quantity_per_unit, amount, price, date_time)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, unit, quantity_per_unit, amount, price, date_time))
        self.conn.commit()

    def log_removal(self, name, unit, quantity_per_unit, amount, date_time):
        # Log the removal operation with a negative amount to indicate removal
        self.cursor.execute('''
            INSERT INTO inventory (name, unit, quantity_per_unit, amount, price, date_time)
            VALUES (?, ?, ?, ?, 0, ?)
        ''', (name, unit, quantity_per_unit, -amount, date_time))
        self.conn.commit()

    def update_item(self, name, unit, quantity_per_unit, amount, price, date_time):
        try:
            # Update the item in the database
            update_query = """
                   UPDATE inventory 
                   SET unit = ?, quantity_per_unit = ?, amount = ?, price = ?
                   WHERE name = ? AND date_time = ?
               """
            self.cursor.execute(update_query, (unit, quantity_per_unit, amount, price, name, date_time))
            self.conn.commit()

            if self.cursor.rowcount == 0:
                raise ValueError("No matching item found to update")

            print("Item updated successfully")

        except sqlite3.Error as e:
            print(f"Error while updating item: {e}")
            self.conn.rollback()

    def fetch_all_items(self):
        self.cursor.execute('SELECT name, unit, quantity_per_unit, amount, price, date_time FROM inventory')
        return self.cursor.fetchall()