import sqlite3

class Cart:

    def __init__(self):
        sample = ""

    def __init__(self, databaseName):
        databaseName = "methods.db"
        self.databaseName = databaseName   

    def viewCart(self, userID):
        self.connection = sqlite3.connect(self.databaseName)
        self.cursor = self.connection.cursor()

        self.cursor.execute("""SELECT Inventory.Title, Inventory.Author, Inventory.Genre, Inventory.Price, Cart.Quantity 
                               FROM Cart INNER JOIN Inventory ON Cart.ISBN = Inventory.ISBN WHERE Cart.userID = ?""", (userID,))
        cartItems = self.cursor.fetchall()

        if cartItems:
            print("\nYour Cart:")
            count = 1
            for Title, Author, Genre, Price, Quantity in cartItems:
                print(f"Item: {count}")
                print(f"Title: {Title}, Author: {Author}, Genre: {Genre}, Price: ${Price}, Quantity in Cart: {Quantity}\n")
                count += 1
        else:
            print("Cart is empty")

        self.cursor.close()
        self.connection.close()

    def addToCart(self,userID, ISBN, quantity):
        pass

    def removeFromCart(self, userID, ISBN):
        pass

    def checkOut(self, userID):
        pass

cart = Cart("methods.db")
cart.viewCart("12-3456")