import sqlite3
import sys

class Inventory:
    def __init__(self, databaseName= "methods.db"):
        self.databaseName = databaseName

    def view_inventory(self):
        # setup database and query the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        ## cursor to send queries through
        cursor = connection.cursor()

        query = "SELECT * FROM inventory"  
        cursor.execute(query)
        items = cursor.fetchall()

        print("Current Inventory:")
        for item in items:
            print(item)  

        ## closes connection
        cursor.close()
        connection.close()

    def search_inventory(self):
        # setup database and query the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        ## cursor to send queries through
        cursor = connection.cursor()

        title = input("Enter the title to search: ")
        query = "SELECT * FROM inventory WHERE title LIKE ?"
        cursor.execute(query, ('%' + title + '%',))
        results = cursor.fetchall()

        if results:
            print("Search Results:")
            for result in results:
                print(result)  # 
        else:
            print("No items found with that title.")

        ## closes connection
        cursor.close()
        connection.close()

    def decrease_stock(self, isbn, quantity=1):
        # setup database and query the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        ## cursor to send queries through
        cursor = connection.cursor()

        query = "UPDATE inventory SET stock = stock - ? WHERE ISBN = ?"
        cursor.execute(query, (quantity, isbn))
        connection.commit()

        if cursor.rowcount > 0:
            print(f"Decreased stock for ISBN {isbn} by {quantity}.")
        else:
            print("ISBN not found or insufficient stock.")

        ## closes connection
        cursor.close()
        connection.close()