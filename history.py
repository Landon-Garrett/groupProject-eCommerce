import sqlite3
import random
import sys

class OrderHistory:

    def __init__(self, databaseName = "methods.db"):
        self.databaseName = databaseName

    def viewHistory(self, userID):
        ## setup database and query the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        ## cursor to send queries through
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Orders WHERE UserID = ?", (userID,))
        orders = cursor.fetchall()

        if orders:
            print("Order History:")
            for order in orders:
                print(f"Order ID: {order[0]}, User ID: {order[1]}, Item Number: {order[2]}, Cost: {order[3]}, Date: {order[4]}")
        else:
            print(f"No orders found for User ID {userID}.")
        
        ## closes connection
        cursor.close()
        connection.close()

    def viewOrder(self, userID, orderID):
        ## setup database and query the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        # Cursor to send queries through
        cursor = connection.cursor()

        # Query specific order details
        query = "SELECT * FROM Orders WHERE UserID = ? AND OrderNumber = ?"
        cursor.execute(query, (userID, orderID))
        order = cursor.fetchone()

        if order:
            print("Order Details:")
            print(f"Order ID: {order[0]}, User ID: {order[1]}, Item Number: {order[2]}, Cost: {order[3]}, Date: {order[4]}")

            # Query for the items in the order
            cursor.execute("SELECT ISBN, Quantity FROM OrderItems WHERE OrderNumber = ?", (orderID,))
            items = cursor.fetchall()

            if items:
                print("\nOrder Items:")
                for item in items:
                    isbn, quantity = item
                    cursor.execute("SELECT Title FROM Inventory WHERE ISBN = ?", (isbn,))
                    title = cursor.fetchone()
                    print(f"- {title[0]} (ISBN: {isbn}), Quantity: {quantity}")
            else:
                print("\nNo items found for this order.")
        else:
            print(f"No order found for User ID {userID} with Order ID {orderID}.")

        # Closes connection
        cursor.close()
        connection.close()


    def createOrder(self, userID, quantity, cost, date):
        ## setup database and query the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        ## cursor to send queries through
        cursor = connection.cursor()

        orderID = str(random.randint(1000, 9999))
        cursor.execute("""
            INSERT INTO Orders (UserID, OrderNumber, ItemNumber, Cost, Date)
            VALUES (?, ?, ?, ?, ?)
        """, (userID, orderID, quantity, cost, date))
        connection.commit()
        print(f"Order {orderID} created successfully.")

        ## closes connection
        cursor.close()
        connection.close()

        return orderID

    def addOrderItems(self, userID, orderID):
        ## setup database and query the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        ## cursor to send queries through
        cursor = connection.cursor()

        cursor.execute("SELECT ISBN, Quantity FROM Cart WHERE UserID = ?", (userID,))
        cartItems = cursor.fetchall()
        
        if cartItems:
            for ISBN, Quantity in cartItems:
                cursor.execute("SELECT * FROM Inventory WHERE ISBN = ?", (ISBN,))
                item = cursor.fetchone()
                if item:
                    title = item[1]  
                    cursor.execute("""
                        INSERT INTO OrderItems (OrderNumber, ISBN, Quantity)
                        VALUES (?, ?, ?)
                    """, (orderID, ISBN, Quantity))
                    print(f"Added {Quantity} of {title} (ISBN: {ISBN}) to order {orderID}.")
                else:
                    print(f"Item with ISBN {ISBN} not found in inventory.")
            cursor.execute("DELETE FROM Cart WHERE UserID = ?", (userID,))
            connection.commit()

        ## closes connection
        cursor.close()
        connection.close()

