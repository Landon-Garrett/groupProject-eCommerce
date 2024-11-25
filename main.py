from user import *
from cart import *
from inventory import *
from history import *


## COMPLETE initial pre-login menu
def initialMenu():
    ## objects for the classes
    user = User()
    cart = Cart()
    inventory = Inventory()
    history = OrderHistory()

    ## initial menu
    while(1):
        print("Pre-Login Menu:")
        print("0. Login")
        print("1. Create Account")
        print("2. Exit Program")
        initial = input("Enter your menu choice: ")
        print()

        if(initial == "0"):
            user.login()

        elif(initial == "1"):
            user.createAccount()

        ## exit program
        elif(initial == "2"):
            print("Good-bye!")
            break

        ## incorrect menu option
        else:
            print("That's not a menu option. Please try again.")

        print()

        ## checks status after one menu loop...
        ## goes into main menu if applicable
        if(user.getLoggedIn()):
            mainMenu(user, cart, inventory, history)


## incomplete main menu...
def mainMenu(user, cart, inventory, history):
    while(user.getLoggedIn()):
        print("Main Menu:")
        print("0. Logout")
        print("1. View Account Information")
        print("2. Inventory Information")
        print("3. Cart Information")
        print("4. Order Information")
        option = input("Enter your menu choice: ")
        print()

        ## logging out
        if(option == "0"):
            user.logout()

            print("Successful logout.")

        #View account information
        elif option == "1":
            user.viewAccountInformation()

        #View inventory information
        elif option == "2":
            pass

        #View cart information
        elif option == "3":
            while True:
                print("\nCart Menu")
                print("0. Return to Main Menu")
                print("1. View Cart")
                print("2. Add to Cart")
                print("3. Remove from Cart")
                print("4. Checkout")
                cartOption = input("Enter in your menu choice: ")
                print()

                #Goes back to the main menu
                if cartOption == "0":
                    break

                #View the cart
                elif cartOption == "1":
                    cart.viewCart(user.getUserID())

                #Add to the cart
                elif cartOption == "2":
                    ISBN = input("Enter in the ISBN of the book you want to add to the cart: ")
                    quantity = int(input("Enter in the quantity: "))
                    print()
                    
                    cart.addToCart(user.getUserID(), ISBN, quantity)

                #Remove from the cart
                elif cartOption == "3":
                    ISBN = input("Enter in the ISBN of the item you want to remove: ")
                    print()

                    cart.removeFromCart(user.getUserID(), ISBN)

                #Checkout
                elif cartOption == "4":
                    cart.checkOut(user.getUserID())
                    
        #View order information
        elif option == "4":
            pass

        ## incorrect menu option
        else:
            print("That's not a menu option. Please try again.")

        print()


def main():
    print("Welcome to the online bookstore!\n")

    initialMenu()

main()
