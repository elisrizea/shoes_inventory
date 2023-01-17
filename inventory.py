# import module
from tabulate import tabulate

# Save colors in constants to decorate the console output
BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[91m'
END = '\033[0m'
MAG = '\u001b[35m'


# ========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return float(self.cost)

    def get_quantity(self):
        return int(self.quantity)

    def __str__(self):
        table = [[f'{BLUE}Product{END}', f'{BLUE}Code{END}', f'{BLUE}Country of origin{END}', f'{BLUE}Cost{END}',
                  f'{BLUE}Quantity{END}'],
                 [f'{GREEN}{str(self.product).title()}{END}', self.code, self.country, self.cost, self.quantity]]
        print(tabulate(table, tablefmt="rounded_grid", ))

    def __repr__(self):
        return f'{self.country},{self.code},{self.product},{self.cost},{self.quantity}\n'


# =============Shoe list===========
# The list will be used to store a list of objects of shoes.
shoe_list = []

# ==========Functions outside the class==============


# -----------------------------
# Load shoe_list from file inventory.txt
def read_shoes_data():
    # Initialise a var to know if line contain shoe details

    # Open and read inventory.txt
    with open("inventory.txt", "r") as inventory_txt:
        inventory_lines = inventory_txt.read().splitlines()
    for inventory_line in inventory_lines:
        inventory_item = inventory_line.split(",")

        # Check if line in the file is corrupt
        # or line does not contain shoe data and skip it
        if len(inventory_item) == 5:

            line_is_ok = True
            # Check if line contain shoe data
            # Last 2 must be cost and quantity both numbers
            try:
                cost = float(inventory_item[3])
                quantity = int(inventory_item[4])
            except ValueError:
                line_is_ok = False

            if line_is_ok:
                country = inventory_item[0]
                code = inventory_item[1]
                product = inventory_item[2]
                cost = inventory_item[3]
                quantity = inventory_item[4]
                # Create object and append it to the shoe_list
                shoe = Shoe(country, code, product, cost, quantity)
                shoe_list.append(shoe)


# -----------------------------
# Request user input, create a new product and add it to the list
def capture_shoes():
    # Initialise local vars
    country = ""
    code = ""
    product = ""
    cost = 0
    quantity = 0

    # Request and check user input
    print(f'{BLUE}\nAdd new shoe to the inventory:{END}')
    while True:
        if country == "":
            country = input('\nPlease enter the country of origin: ').capitalize()
        elif code == "":
            code = input('\nPlease enter the product SKU code: ').upper()
            for shoe in shoe_list:
                if shoe.code == code:
                    print(f'{RED} {code} already exist in inventory, Please choose a different SKU code.{END}')
                    code = ""
                    continue
        elif product == "":
            product = input('\nPlease enter the product name: ').capitalize()
        elif cost == 0:
            try:
                cost = round(float(input('\nPlease enter the product price: ')), 2)
            except ValueError:
                print(f'{RED} Please enter a number not text.{END}')
                continue
        elif quantity == 0:
            try:
                quantity = int(input('\nPlease enter the product quantity: '))
            except ValueError:
                print(f'{RED} Please enter a number not text.{END}')
                continue
        else:
            # Create object and append it to the shoe_list
            shoe_txt = Shoe(country, code, product, cost, quantity)
            shoe_list.append(shoe_txt)
            break

    return update_txt()


# -----------------------------
# Print all product
def view_all():
    for i in range(len(shoe_list)):
        shoe = shoe_list[i]
        shoe.__str__()


# -----------------------------
# Print the lowest stock product
def re_stock():
    # Assign to low_stock the quantity from the first product
    # Set index to first product index
    low_stock = shoe_list[0].get_quantity()
    index = 0

    # Compare every product quantity and get
    # the index of the first product with the lowest
    for i in range(1, len(shoe_list)):
        if int(low_stock) > int(shoe_list[i].get_quantity()):
            index = i
            low_stock = shoe_list[i].get_quantity()

    print(f'{RED}************ Low on stock alert ************')
    shoe_list[index].__str__()
    print(f'{RED}************ Low on stock alert ************\n{END}')

    # Ask if update is require and check user input
    while True:
        update_stock = input(f' {BLUE}Update the stock? Type {GREEN}yes{END} or {RED}no{END}:  ').strip().lower()
        if update_stock == "yes" or update_stock == "y":
            try:
                u_stock = int(input("How many items you want to add? "))
            except ValueError:
                print(f'{RED} Please enter a number not text.{END}')
                continue
        elif update_stock == "no" or update_stock == "n":
            return f"{RED} Stock remain critical.\n{END}"
        else:
            continue
        # Update shoe_list and rewrite the file
        shoe_list[index].quantity = str(u_stock + shoe_list[index].get_quantity())
        break
    return update_txt()


# -----------------------------
# Search and print a product with entered SKU code
def search_shoe():
    # Request and verify user input
    sku = ""
    while True:
        if len(sku) < 4:
            sku = input("\nPlease enter the SKU cod: ").strip().upper()
            print()
        else:
            break

        # Search the list and return the result
        for shoe in shoe_list:
            if shoe.code == sku:
                return shoe.__str__()
        return print(f'{RED} No products found with {END}"{sku}"{RED} code.{END}')


# -----------------------------
# Search and delete a product with entered SKU code
def delete_shoe():
    # Request and verify user input
    sku = ""
    while True:
        if len(sku) < 4:
            sku = input("\nPlease enter the SKU cod: ").strip().upper()
        else:
            break

        # Search using SKU code and remove the product found
        for shoe_d in shoe_list:
            if shoe_d.code == sku:
                index = shoe_list.index(shoe_d)
                shoe_list.pop(index)
                update_txt()
                return print(
                    f'{GREEN}The shoe with  code: {END}{shoe_d.code}{GREEN} and'
                    f' name: {END}{shoe_d.product}{GREEN} has been deleted from the shoe list and file.{END}')
        return print(f'{RED} No products found with {END}"{sku}"{RED} code.{END}')


# -----------------------------
# Return a table containing "Product name", "SKU code" and "Total item value"= cost*quantity
def value_per_item():
    table = [[f'{BLUE}Product{END}', f'{BLUE}Code{END}', f'{BLUE}Total item value{END}']]

    for shoe in shoe_list:
        table.append(
            [f'{GREEN}{str(shoe.product).title()}{END}', shoe.code, round(shoe.get_cost() * shoe.get_quantity(), 2)])

    return print(tabulate(table, tablefmt="rounded_grid", ))


# -----------------------------
# Print the highest stock product
def highest_qty():
    # Assign to low_stock the quantity from the first product
    # Set index to first product index
    high_stock = shoe_list[0].get_quantity()
    index = 0

    # Compare every product quantity and get
    # the index of the first product with the lowest
    for i in range(1, len(shoe_list)):
        if int(high_stock) < int(shoe_list[i].get_quantity()):
            index = i
            high_stock = shoe_list[i].get_quantity()

    print(f'{GREEN}\n*************************** ON SALE ***************************{END}')
    shoe_list[index].__str__()
    print(f'{GREEN}*************************** ON SALE ***************************{END}')
    return


# -----------------------------
# Update inventory.txt with items from shoe_list
def update_txt():
    shoe_str = 'Product, Code, Country, Cost, Quantity\n'
    for i in range(len(shoe_list)):
        shoe_str += shoe_list[i].__repr__()
    with open("inventory.txt", "w+") as txt:
        txt.write(shoe_str)
    return print(f'{GREEN}Inventory update successfully.{END}')


# ==========Main Menu=============
# Read all products from file and load them in the shoe_list
read_shoes_data()

# Display main menu
while True:
    print(f' {BLUE}********************** Main Menu **********************\n')

    menu = input(f'''Select one of the following Options below:
                {MAG}v{BLUE}    - {MAG}V{BLUE}iew all stock
                {MAG}a{BLUE}    - {MAG}A{BLUE}dd a new product
                {MAG}d{BLUE}    - {MAG}D{BLUE}elete a product using SKU code
                {MAG}l{BLUE}    - View {MAG}l{BLUE}ow stock item and update stock
                {MAG}h{BLUE}    - View {MAG}h{BLUE}ighest stock item and put this on sale
                {MAG}s{BLUE}    - {MAG}S{BLUE}earch for a product using SKU code
                {MAG}e{BLUE}    - Save and {MAG}e{BLUE}xit
{MAG}Enter your choice: {END}''').strip().lower()

    # Request input and call the necessary function
    if menu == 'v':
        print(f"""
{BLUE}================ View all stock =========================={END}""")
        view_all()
        continue
    elif menu == 'a':
        print(f"""
{BLUE}================ Add a new product: =========================={END}""")
        capture_shoes()
        continue
    elif menu == 'd':
        print(f"""
{BLUE}================ Delete a product: =========================={END}""")
        delete_shoe()
        continue
    elif menu == 'l':
        print(f"""
{BLUE}================ Lowest item in stock: =========================={END}""")
        print(re_stock())
        continue
    elif menu == 'h':
        print(f"""
{BLUE}================ Heighest item in stock: =========================={END}""")
        highest_qty()
        continue
    elif menu == 's':
        print(f"""
{BLUE}================ Search using SKU code: =========================={END}""")
        search_shoe()
        continue
    elif menu == 'e':
        print(f"""
{BLUE}================ Save and exit: =========================={END}""")
        update_txt()
        print('Goodbye!!!')
        exit()
    else:
        print(
            f'{RED}Please try again and type: '
            f'{GREEN}v{END} or {GREEN}a{END} or {GREEN}l{END} or {GREEN}h{END} or {GREEN}s{END} or {GREEN}e{END}')
        continue
