import sqlite3

class Inventory:
    def __init__(self, database_name=None):
        self.database_name = database_name
        self.connection = None
        if self.database_name:
            self.connect_to_database()

    def connect_to_database(self):
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()

    def view_inventory(self):
        if not self.connection:
            print("No database connected.")
            return

        query = "SELECT * FROM inventory"  
        self.cursor.execute(query)
        items = self.cursor.fetchall()

        print("Current Inventory:")
        for item in items:
            print(item)  

    def search_inventory(self):
        if not self.connection:
            print("No database connected.")
            return

        title = input("Enter the title to search: ")
        query = "SELECT * FROM inventory WHERE title LIKE ?"
        self.cursor.execute(query, ('%' + title + '%',))
        results = self.cursor.fetchall()

        if results:
            print("Search Results:")
            for result in results:
                print(result)  # 
        else:
            print("No items found with that title.")

    def decrease_stock(self, isbn, quantity=1):
        if not self.connection:
            print("No database connected.")
            return

        query = "UPDATE inventory SET stock = stock - ? WHERE ISBN = ?"
        self.cursor.execute(query, (quantity, isbn))
        self.connection.commit()

        if self.cursor.rowcount > 0:
            print(f"Decreased stock for ISBN {isbn} by {quantity}.")
        else:
            print("ISBN not found or insufficient stock.")

    def close(self):
        if self.connection:
            self.connection.close()