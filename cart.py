import sqlite3

class Cart:

    def __init__(self):
        sample = ""

    def __init__(self, databaseName = "methods.db"):
        self.databaseName = databaseName  

        self.connection = sqlite3.connect(self.databaseName)
        self.cursor = self.connection.cursor() 

    def viewCart(self, userID):

        #gets everything in the cart to view
        self.cursor.execute("""SELECT Inventory.Title, Inventory.Author, Inventory.Genre, Inventory.Price, Cart.Quantity 
                                FROM Cart INNER JOIN Inventory ON Cart.ISBN = Inventory.ISBN WHERE Cart.userID = ?""", (userID,))
        cartItems = self.cursor.fetchall()

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

    def addToCart(self, userID, ISBN, quantity = 1):

        try:
            quantity = int(quantity)
            if quantity < 1:
                print("Invalid quantity, must be a positive integer.")
                return
        except ValueError:
            print("Invalid quantity, must be a positive integer.")
            return


        #selects the ISBN and its quantity to check if the ISBN and quantity is valid
        self.cursor.execute("SELECT Stock FROM Inventory WHERE ISBN = ?", (ISBN,))
        available = self.cursor.fetchone()

        #if the ISBN does not exist
        if available is None: 
            print(f"Error: ISBN {ISBN} does not exist.")
            return

        #gets the total stock for that item
        stockAvailable = available[0]

        #checks if the ISBN is already in the cart
        self.cursor.execute("SELECT Quantity FROM Cart WHERE UserID = ? AND ISBN = ?" ,(userID, ISBN,))
        cartItem = self.cursor.fetchone()

        #if the ISBN exist already it adds the new quantity onto the existing quantity
        if cartItem:
            currentQuantity = cartItem[0]
            newQuantity = currentQuantity + quantity

            #checks if new quantity exceeds the max quantity
            if newQuantity > stockAvailable:
                print(f"Error: adding {quantity} exceeds available stock of {stockAvailable}.")
                return
            
            self.cursor.execute("UPDATE Cart SET Quantity = ? WHERE UserID = ? AND ISBN = ?", (newQuantity, userID, ISBN,))
            print(f"Updated the quantity of ISBN {ISBN} for the userID {userID}, to the new quantity {newQuantity}.")
        
        #if the ISBN does not exist it creates a new entry
        else:
            #checking stock to make sure it does not exceed the available stock
            if quantity > stockAvailable:
                print(f"Error: only {stockAvailable} is available for the ISBN {ISBN}.")
                return
        
            #if everything is valid then the item is added to the cart
            self.cursor.execute("INSERT INTO Cart (userID, ISBN, quantity) VALUES (?, ?, ?)", (userID, ISBN, quantity,))
            print(f"Added {quantity} of ISBN {ISBN} to the cart for the userID {userID}.")

        self.connection.commit()

    def removeFromCart(self, userID, ISBN):

        #deletes from cart
        self.cursor.execute("DELETE FROM Cart WHERE UserID = ? AND ISBN = ?", (userID, ISBN,))
        
        #checks to make sure there is something there to delete
        if self.cursor.rowcount > 0:
            self.connection.commit()
            print(f"Removed ISBN {ISBN} from cart for userID {userID}.")
        else:
            print(f"Item with ISBN {ISBN} was not found for the userID {userID}.")

    def checkOut(self, userID):
        pass

cart = Cart("methods.db")
cart.viewCart("12-3456")  #view cart at the userID
cart.addToCart("34-342", "4355", 34)  #adds to cart at invalid ISBN
cart.addToCart("34-342", "978-0451524935", 0.5) #adds invalid digit
cart.addToCart("34-342", "978-0451524935", "abc") #adds invalid quantity
cart.addToCart("34-342", "978-0451524935", 1) #adds to cart at valid ISBN
cart.addToCart("34-342", "978-0451524935", 14) #adds to cart at the previous ISBN but too many items
cart.addToCart("34-342", "978-0446310789", 1000) #adds to cart at a new valid ISBN but with too many items
#cart.removeFromCart("34-342", "978-0451524935") #deletes from cart