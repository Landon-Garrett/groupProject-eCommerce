import sqlite3
import random

class OrderHistory:

    def __init__(self, database_name = "orders.db"):
        self.database_name = database_name
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()

    def viewHistory(self, userID):
        query = "SELECT * FROM Orders WHERE UserID = ?"
        self.cursor.execute(query, (userID,))
        orders = self.cursor.fetchall()
        if orders:
            print("Order History:")
            count = 1
            for order in orders:
                orderID = order[0]
                orderDate = order[1]
                print(f"Order {count}: Order ID {orderID}, Date: {orderDate}")
                self.cursor.execute("SELECT ISBN, Quantity FROM OrderItems WHERE OrderID = ?", (orderID,))
                order_items = self.cursor.fetchall()

                if order_items:
                    print("Items in this order:")
                    for item in order_items:
                        ISBN, Quantity = item
                        print(f"ISBN: {ISBN}, Quantity: {Quantity}")
                else:
                    print("No items found for this order.")
                
                count += 1
        else:
            print("No orders found for this user.")

    def viewOrder(self, userID, orderID):
        self.cursor.execute("SELECT * FROM Orders WHERE UserID = ? AND OrderNumber = ?", (userID, orderID))
        order = self.cursor.fetchone()

        if order:
            orderDate = order[1]
            print(f"\nOrder ID: {orderID}, Date: {orderDate}")
            
            self.cursor.execute("SELECT ISBN, Quantity FROM OrderItems WHERE OrderID = ?", (orderID,))
            order_items = self.cursor.fetchall()

            if order_items:
                print("Items in this order:")
                for item in order_items:
                    ISBN, Quantity = item
                   self.cursor.execute("SELECT Title, Author, Price FROM Inventory WHERE ISBN = ?", (ISBN,))
                    inventory_item = self.cursor.fetchone()

                    if inventory_item:
                        title, author, price = inventory_item
                        print(f"ISBN: {ISBN}, Title: {title}, Author: {author}, Price: {price}, Quantity: {Quantity}")
                    else:
                        print(f"Item with ISBN {ISBN} not found in inventory.")
            else:
                print("No items found for this order.")
        else:
            print(f"Order {orderID} not found or does not belong to user {userID}.")
    def createOrder(self, userID, quantity, cost, date):
        orderID = str(random.randint(1000, 9999))
        self.cursor.execute("""
            INSERT INTO Orders (UserID, OrderNumber, Quantity, TotalCost, Date)
            VALUES (?, ?, ?, ?, ?)
        """, (userID, orderID, quantity, cost, date))
        self.connection.commit()
        print(f"Order {orderID} created successfully.")
        return orderID

    def addOrderItems(self, userID, orderID):
        self.cursor.execute("SELECT ISBN, Quantity FROM Cart WHERE UserID = ?", (userID,))
        cartItems = self.cursor.fetchall()
        
        if cartItems:
            for ISBN, Quantity in cartItems:
                self.cursor.execute("SELECT * FROM Inventory WHERE ISBN = ?", (ISBN,))
                item = self.cursor.fetchone()
                if item:
                    title = item[1]  
                    self.cursor.execute("""
                        INSERT INTO OrderItems (OrderNumber, ISBN, Quantity)
                        VALUES (?, ?, ?)
                    """, (orderID, ISBN, Quantity))
                    print(f"Added {Quantity} of {title} (ISBN: {ISBN}) to order {orderID}.")
                else:
                    print(f"Item with ISBN {ISBN} not found in inventory.")
            self.cursor.execute("DELETE FROM Cart WHERE UserID = ?", (userID,))
            self.connection.commit()
