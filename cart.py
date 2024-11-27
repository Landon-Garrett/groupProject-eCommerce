import sqlite3
import sys
from inventory import *
from history import *
import datetime

class Cart:
    def __init__(self, databaseName = "methods.db"):
        self.databaseName = databaseName  

    def viewCart(self, userID):
        ## setup database and query the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        ## cursor to send queries through
        cursor = connection.cursor()

        #gets everything in the cart to view
        cursor.execute("""SELECT Inventory.Title, Inventory.Author, Inventory.Genre, Inventory.Price, Cart.Quantity 
                                FROM Cart INNER JOIN Inventory ON Cart.ISBN = Inventory.ISBN WHERE Cart.userID = ?""", (userID,))
        cartItems = cursor.fetchall()

        #if there is items is the cart view it, if not say the cart is empty
        if cartItems:
            print("\nYour Cart:")
            count = 1
            for Title, Author, Genre, Price, Quantity in cartItems:
                print(f"Item: {count}")
                print(f"Title: {Title}, Author: {Author}, Genre: {Genre}, Price: ${Price}, Quantity in Cart: {Quantity}\n")
                count += 1
        else:
            print("Cart is empty")

        #Closes connection
        cursor.close()
        connection.close()

    def addToCart(self, userID, ISBN, quantity = 1):

        ## setup database and query the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        ## cursor to send queries through
        cursor = connection.cursor()

        #Trys for a valid quantity
        try:
            quantity = int(quantity)
            if quantity < 1:
                print("Invalid quantity, must be a positive integer.")
                return
        except ValueError:
            print("Invalid quantity, must be a positive integer.")
            return


        #selects the ISBN and its quantity to check if the ISBN and quantity is valid
        cursor.execute("SELECT Stock FROM Inventory WHERE ISBN = ?", (ISBN,))
        available = cursor.fetchone()

        #if the ISBN does not exist
        if available is None: 
            print(f"Error: ISBN {ISBN} does not exist.")
            return

        #gets the total stock for that item
        stockAvailable = available[0]

        #checks if the ISBN is already in the cart
        cursor.execute("SELECT Quantity FROM Cart WHERE UserID = ? AND ISBN = ?" ,(userID, ISBN,))
        cartItem = cursor.fetchone()

        #if the ISBN exist already it adds the new quantity onto the existing quantity
        if cartItem:
            currentQuantity = cartItem[0]
            newQuantity = currentQuantity + quantity

            #checks if new quantity exceeds the max quantity
            if newQuantity > stockAvailable:
                print(f"Error: adding {quantity} exceeds available stock of {stockAvailable}.")
                return
            
            #updates it to the new quantity
            cursor.execute("UPDATE Cart SET Quantity = ? WHERE UserID = ? AND ISBN = ?", (newQuantity, userID, ISBN,))
            print(f"Updated the quantity of ISBN {ISBN} for the userID {userID}, to the new quantity {newQuantity}.")
        
        #if the ISBN does not exist it creates a new entry
        else:
            #checking stock to make sure it does not exceed the available stock
            if quantity > stockAvailable:
                print(f"Error: only {stockAvailable} is available for the ISBN {ISBN}.")
                return
        
            #if everything is valid then the item is added to the cart
            cursor.execute("INSERT INTO Cart (userID, ISBN, quantity) VALUES (?, ?, ?)", (userID, ISBN, quantity,))
            print(f"Added {quantity} of ISBN {ISBN} to the cart for the userID {userID}.")

        connection.commit()

        ## closes connection
        cursor.close()
        connection.close()

    def removeFromCart(self, userID, ISBN):
        ## setup database and query the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        ## cursor to send queries through
        cursor = connection.cursor()

        #deletes from cart
        cursor.execute("DELETE FROM Cart WHERE UserID = ? AND ISBN = ?", (userID, ISBN,))
        
        #checks to make sure there is something there to delete
        if cursor.rowcount > 0:
            connection.commit()
            print(f"Removed ISBN {ISBN} from cart for userID {userID}.")
        else:
            print(f"Item with ISBN {ISBN} was not found in the cart for the userID {userID}.")

        ## closes connection
        cursor.close()
        connection.close()

    def checkOut(self, userID):
        ## setup database and query the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        ## cursor to send queries through
        cursor = connection.cursor()

        #Fetches CartItems
        cursor.execute("SELECT ISBN, Quantity FROM Cart WHERE userID = ?", (userID,))
        cartItems = cursor.fetchall()

        #if there are no items in the cart
        if not cartItems:
            print("There are not items in your cart cannot checkout.")
            return
        
        #Calculates the total cost of the cart, as well as the total quantity of items in the cart
        totalCost = 0
        totalQuantity = 0
        for ISBN, Quantity in cartItems:
            cursor.execute("SELECT Price FROM Inventory WHERE ISBN = ?", (ISBN,))
            results = cursor.fetchone()

            totalCost += results[0] * Quantity #Gets total cost of the cart
            totalQuantity += Quantity   #Gets the total quantity of the cart

        #decrease the stock from the inventory
        for ISBN, Quantity in cartItems:
            Inventory.decrease_stock(self, ISBN, Quantity)

        #Gets the current date
        currentDate = datetime.date.today().strftime("%m/%d/%y")

        #creates an order for the cart items
        orderID = OrderHistory.createOrder(self, userID, totalQuantity, totalCost, currentDate)
        OrderHistory.addOrderItems(self, userID, orderID)

        #Clears the cart
        cursor.execute("DELETE FROM Cart WHERE userID = ?", (userID,))
        connection.commit()

        ## closes connection
        cursor.close()
        connection.close()