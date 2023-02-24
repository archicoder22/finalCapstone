# ===== import section =====
import os


# ===== global variables =====
shoe_list = []  # a list to store shoes objects

YELLOW = '\033[93m'
PINK = '\033[91m'
WHITE = '\033[0m'


# ===== Class definition =====
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):  # function that returns the cost of a shoe
        print(f"The cost of {self.product} is {self.cost}.")

    def get_quantity(self):  # function that returns the quantity of shoes
        print(f"The quantity of {self.product} is {self.quantity}.")

    def __str__(self):
        print(f"Made in: {self.country}, product code: {self.code}, product name: {self.product}, "
              f"shoe cost: {self.cost}, shoe quantity: {self.quantity}")

    def shoe_detail(self):
        item = f"Made in: {self.country}, product code: {self.code}, product name: {self.product}, " \
              f"shoe cost: {self.cost}, shoe quantity: {self.quantity}"
        return item


# ===== functions =====

# define a function that reads inventory data from a file
def read_shoes_data():
    inventory_path = "./inventory.txt"

    try:
        os.path.isfile(inventory_path)

        with open("inventory.txt", "r", encoding="utf-8") as shoe_file:

            for lines in shoe_file:
                temp = lines.strip("\n").split(",")

                shoe_list.append(Shoe(temp[0], temp[1], temp[2], temp[3], temp[4]))
            shoe_list.pop(0)  # remove the title line from the list

    except FileNotFoundError:
        print(f"{PINK}Inventory file does not exist.{WHITE}")


# define a function that captures shoe data from the user, use it to create a shoe object and adds to shoe list
def capture_shoes():
    #  check if shoe details have been saved into the list
    if len(shoe_list) == 0:  # list is empty
        read_shoes_data()  # get shoe details from the file

    input_country = input("\nWhat country was a shoe made in?")
    input_code = input("What is the shoe code?")
    input_product = input("What is the product name?")
    input_cost = input("What is the shoe cost?")
    input_quantity = int(input("What is the shoe quantity?"))

    new_shoe = Shoe(input_country, input_code, input_product, input_cost, input_quantity)

    shoe_list.append(new_shoe)

    update_file()


def view_all():
    #  check if shoe details have been saved into the list
    if len(shoe_list) == 0:  # list is empty
        read_shoes_data()  # get shoe details from the file

    print(f"\n{YELLOW}Shoe inventory details:{WHITE}\n")

    for x in range(len(shoe_list)):
        shoe_list[x].__str__()


# define a function that returns a list of shoe quantities
def shoe_quantities():
    quantities = []  # create a list for item quantities

    #  check if shoe details have been saved into the list
    if len(shoe_list) == 0:  # list is empty
        read_shoes_data()  # get shoe details from the file

    # add all items quantities to the list
    for x in range(len(shoe_list)):
        quantities.append(int(shoe_list[x].quantity))  # cast to integer to allow for number operations

    return quantities


# define a function that finds the shoe item with the lowest quantity, allow user to update the quantity
def re_stock():
    quantities = []  # create a list for item quantities
    lowest_qty_list = []  # create a list for multiple objects of the lowest quantity
    smallest_index = -1  # create variable to keep track of index of currently the lowest stock item
    index_list = []  # create a list of indices to update

    #  check if shoe details have been saved into the list
    if len(shoe_list) == 0:  # list is empty
        read_shoes_data()  # get shoe details from the file

    # add all items quantities to the list
    for x in range(len(shoe_list)):
        quantities.append(int(shoe_list[x].quantity))  # cast to integer to allow for number operations

    # check if there are more than 1 object at the same lowest quantity
    for m in range(len(shoe_list)):
        if int(shoe_list[m].quantity) == min(quantities):
            # append shoe details and their index to the list
            lowest_qty_list.append(shoe_list[m].shoe_detail())

    if len(lowest_qty_list) > 1:  # if there are multiple items of the lowest quantity
        print("\nThere are multiple items with the lowest quantity:\n")

        for i in range(len(lowest_qty_list)):
            print(f"Shoe item {YELLOW}No.{lowest_qty_list.index(lowest_qty_list[i]) + 1}:{WHITE} {lowest_qty_list[i]}")

        item_choice = input("\nWhat would you like to do?\n"
                            f"- select \"{YELLOW}A{WHITE}\" to update {YELLOW}all{WHITE}\n"
                            f"- select \"{YELLOW}S{WHITE}\" to choose a {YELLOW}single item{WHITE} to update.")
        while True:
            if item_choice.upper() == "A":
                for i in range(len(shoe_list)):
                    for j in range(len(lowest_qty_list)):
                        lowest_item = lowest_qty_list[j]
                        if shoe_list[i].shoe_detail() == lowest_item:
                            index_list.append(shoe_list.index(shoe_list[i]))
                break
            elif item_choice.upper() == "S":
                item_number_choice = input("Please choose item to update:")
                while True:
                    try:  # cast user input into an integer to check if number has been entered
                        value = int(item_number_choice)
                    except ValueError:
                        item_number_choice = input("This is not a number, try again:")
                        continue
                    break
                while True:
                    if int(item_number_choice) in range(1, len(lowest_qty_list) + 1):
                        smallest_item = lowest_qty_list[int(item_number_choice) - 1]
                        for i in range(len(shoe_list)):
                            if shoe_list[i].shoe_detail() == smallest_item:  # find index of chosen item
                                smallest_index = shoe_list.index(shoe_list[i])
                        break
                    else:
                        item_number_choice = input(f"{PINK}Incorrect entry, try again.{WHITE}")
                break
            else:
                item_choice = input(f"{PINK}Incorrect choice, try again.{WHITE}")

    else:  # there is a single item of the lowest quantity
        # find index of the item with the lowest stock
        smallest_index = quantities.index(min(quantities))

        print(f"\nPlease see below details of the {PINK}item with the {PINK}lowest stock{WHITE}:\n")

        # display details of the item with the lowest stock
        shoe_list[smallest_index].__str__()

    # present a menu to the user
    restock_option = input("\nWhat would you like to do?\n"
                           f"select \"{YELLOW}R{WHITE}\" to restock the item "
                           f"with the {YELLOW}same amount{WHITE} of shoes\n"
                           f"select \"{YELLOW}D{WHITE}\" to restock {YELLOW}different amount{WHITE}\n"
                           f"select \"{YELLOW}X{WHITE}\" to {YELLOW}exit{WHITE} to the main menu.")

    while True:
        if restock_option.upper() == "R":
            if smallest_index > -1:  # single item to update
                current_stock = int(shoe_list[smallest_index].quantity)
                shoe_list[smallest_index].quantity = current_stock * 2  # add the same quantity of the item
                print(f"{YELLOW}\nQuantity updated successfully!{WHITE}")
            else:  # multiple items to update
                for i in range(len(shoe_list)):
                    for j in range(len(lowest_qty_list)):
                        lowest_item = lowest_qty_list[j]
                        if shoe_list[i].shoe_detail() == lowest_item:
                            current_stock = int(shoe_list[i].quantity)
                            shoe_list[i].quantity = current_stock * 2  # add the same quantity of the item
                print(f"{YELLOW}\nQuantities updated successfully!{WHITE}")
            break

        elif restock_option.upper() == "D":
            restock_amount = input(f"Give a {YELLOW}number to restock{WHITE}:")  # request quantity
            value = 0
            while True:
                try:  # cast user input into an integer to check if number has been entered
                    value = int(restock_amount)
                except ValueError:
                    restock_amount = input(f"{PINK}This is not a number, try again:{WHITE}")
                    continue
                break

            if smallest_index > -1:  # single item to update
                current_stock = int(shoe_list[smallest_index].quantity)
                shoe_list[smallest_index].quantity = value + current_stock  # add quantity given by the user
                print(f"\n{YELLOW}Quantity updated successfully!{WHITE}")
            else:  # multiple items to update
                for i in range(len(shoe_list)):
                    for j in range(len(lowest_qty_list)):
                        lowest_item = lowest_qty_list[j]
                        if shoe_list[i].shoe_detail() == lowest_item:
                            current_stock = int(shoe_list[i].quantity)
                            shoe_list[i].quantity = value + current_stock  # add the same quantity of the item
                print(f"{YELLOW}\nQuantities updated successfully!{WHITE}")
            break

        elif restock_option.upper() == "X":
            break

        else:
            restock_option = input(f"{PINK}Incorrect choice, try again.{WHITE}")
            continue

    update_file()


# define a function that updates external file
def update_file():
    with open("inventory.txt", "w", encoding="utf-8") as shoe_file:
        output = "Country,Code,Product,Cost,Quantity\n"
        for s in range(len(shoe_list)):
            output += f"{shoe_list[s].country}," \
                      f"{shoe_list[s].code}," \
                      f"{shoe_list[s].product}," \
                      f"{shoe_list[s].cost}," \
                      f"{shoe_list[s].quantity}\n"
        shoe_file.write(output)


# define a function that searches a shoe by shoe code and returns and prints shoe details
def search_shoe():
    #  check if shoe details have been saved into the list
    if len(shoe_list) == 0:  # list is empty
        read_shoes_data()  # get shoe details from the file

    codes_list = []  # create a list of codes to check for entry
    search_index = 0  # index of searched item

    for i in range(len(shoe_list)):
        codes_list.append(shoe_list[i].code)

    input_code = input(f"Please {YELLOW}enter a code{WHITE} of the shoe to display details of:")

    while True:  # check if code exists
        if input_code in codes_list:
            for i in range(len(shoe_list)):
                if shoe_list[i].code == input_code:  # find item index of the item with given code
                    search_index = shoe_list.index(shoe_list[i])
            break
        else:
            input_code = input(f"{PINK}This code does not exist. Please try again.{WHITE}")
    print(f"\nBelow are the {YELLOW}details of the searched shoe:{WHITE}\n")
    search_shoe_details = shoe_list[search_index].__str__()

    return search_shoe_details


# create a function that calculates the total value of each item
def value_per_item():
    #  check if shoe details have been saved into the list
    if len(shoe_list) == 0:  # list is empty
        read_shoes_data()  # get shoe details from the file

    print(f"\nPlease see below {YELLOW}information on the value per item{WHITE} for all shoes in the database "
          f"(calculated as {YELLOW}cost x quantity{WHITE}):\n")

    for i in range(len(shoe_list)):
        item_value = int(shoe_list[i].cost) * int(shoe_list[i].quantity)
        print(f"The value of {shoe_list[i].product} ({shoe_list[i].code}) is: {item_value}")


# define a function that finds a product with the highest quantity and prints that it is for sale
def highest_qty():
    quantities = []  # create a list for item quantities
    highest_qty_list = []  # create a list for multiple objects of the highest quantity

    #  check if shoe details have been saved into the list
    if len(shoe_list) == 0:  # list is empty
        read_shoes_data()  # get shoe details from the file

    # add all items quantities to the list
    for x in range(len(shoe_list)):
        quantities.append(int(shoe_list[x].quantity))  # cast to integer to allow for number operations

    # check if there are more than 1 object at the same highest quantity
    for m in range(len(shoe_list)):
        if int(shoe_list[m].quantity) == max(quantities):
            # append shoe details and their index to the list
            highest_qty_list.append(shoe_list[m].shoe_detail())

    if len(highest_qty_list) > 1:  # there are multiple items of the highest quantity

        print(f"\n{PINK}The following items{YELLOW} are for SALE:{WHITE}")

        for i in range(len(shoe_list)):
            for j in range(len(highest_qty_list)):
                highest_item = highest_qty_list[j]
                if shoe_list[i].shoe_detail() == highest_item:
                    print(f"{shoe_list[i].product}")

    else:  # there is a single item of the highest quantity
        # find index of the item with the highest quantity
        highest_index = quantities.index(max(quantities))

        print(f"\n{PINK}{shoe_list[highest_index].product}{YELLOW} is for SALE!!{WHITE}")


# ==========Main Menu=============
while True:
    menu_select = input(f"\n{PINK}Please select{WHITE} one of the following options:\n\n"
                        f"- \"{YELLOW}VA{WHITE}\" to view details of all shoes in database\n"
                        f"- \"{YELLOW}A{WHITE}\" to add a new shoe product to the database\n"
                        f"- \"{YELLOW}R{WHITE}\" to restock low quantity shoes\n"
                        f"- \"{YELLOW}S{WHITE}\" to search the shoe by the code\n"
                        f"- \"{YELLOW}V{WHITE}\" to see value per item\n"
                        f"- \"{YELLOW}H{WHITE}\" to see the item of highest quality")
    if menu_select.upper() == "VA":
        view_all()
    elif menu_select.upper() == "A":
        capture_shoes()
    elif menu_select.upper() == "R":
        re_stock()
    elif menu_select.upper() == "S":
        search_shoe()
    elif menu_select.upper() == "V":
        value_per_item()
    elif menu_select.upper() == "H":
        highest_qty()
