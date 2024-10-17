# ─── Modules To Import ────────────────────────────────────────────────────────
import mysql.connector as sql
from pwinput import pwinput
import bcrypt
import os
from InquirerPy import inquirer, get_style
import datetime
import time
import csv

from rich.progress import track
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich.theme import Theme
from rich.prompt import IntPrompt, FloatPrompt, Prompt
from rich.columns import Columns
from rich import box
from rich.table import Table
from rich.spinner import Spinner
from rich.live import Live

# ──────────────────────────────────────────────────────────────────────────────

style = get_style(
    {
        "questionmark": "bold red",
        "question": "bold red",
        "answered_question": "red",
        "answer": "green",
        "input": "yellow",
        "options": "yellow",
        "pointer": "blue",
        "amark": "red",
    },
    style_override=False,
)

custom_theme = Theme(
    {
        "success": "bold #76B947",
        "error": "bold #FF004D",
        "border": "#DA0037",
        "heading": "bold #EDEDED",
        "menu": "purple",
        "input": "yellow",
        "background": "#171717",
        "pass": "#DA0037 blink",
        "table": "cyan",
    },
    inherit=False,
)

console = Console(theme=custom_theme)

# ─── Connecting To Mysql Database ──────────────────────────────────────────────────────────────────────────────────────────

try:
    conobj = sql.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        passwd=os.environ.get("DB_PASSWD"),
        database=os.environ.get("DB_DATABASE"),
    )
    cursor = conobj.cursor()
except Exception as e:
    console.print(f"Could not connect to MySQL database \n{e}", style="error")
    spinner = Spinner(
        "point", text=Text("Terminating the Program", style="error"), style="error"
    )
    with Live(spinner, refresh_per_second=20) as live:
        for i in range(7):
            time.sleep(0.2)
    exit()

# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

# ─── Declaring Global Variables ────────────────────────────────────────────────────────────────────────────────────────────

email = ""

cart = []
itemnos_in_cart = []
items_table = []
cart_table = []

items = []
items_no = []

# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────


def sign_in(user: str = "customer" or "employee") -> bool:
    global email
    while True:
        email = console.input("[input]Enter your email : ")
        q = f"SELECT {user}_name, passwd FROM {user}_table WHERE email = %s"
        v = (email,)
        cursor.execute(q, v)
        rec = cursor.fetchall()
        if len(rec) == 0:
            console.print(f"{email} does not exist in our database", style="error")
            ch = inquirer.confirm(
                message="Do you want to register ?", style=style
            ).execute()
            if ch:
                if user == "customer":
                    customer_register()
                    console.print(
                        "\nYou can sign in with your credentials now\n", style="success"
                    )

                elif user == "employee":
                    employee_register()
                    console.print(
                        "\nYou can sign in with your credentials now\n", style="success"
                    )

        else:
            hashed = (rec[0][1]).encode("utf-8")
            c = 3
            while c > 0:
                console.print("Enter your password : ", end="", style="pass")
                password = pwinput(prompt="").encode("utf-8")
                if bcrypt.checkpw(password, hashed):
                    console.print(
                        f"\nWelcome {rec[0][0].title()} !!! \n", style="success"
                    )

                    spinner = Spinner(
                        "point",
                        text=Text(f"Continuing to {user} screen", style="green"),
                        style="green",
                    )
                    with Live(spinner, refresh_per_second=20) as live:
                        for i in range(5):
                            time.sleep(0.2)

                    return (email, True)
                else:
                    c -= 1
                    console.print(
                        "Password Incorrect \nPlease Try again", style="error"
                    )
                    console.print(f"You have {c} more chances", style="error")
            else:
                console.print("Chances Over", style="error")
                return (email, False)


def customer_register():
    try:
        os.system("cls")
        console.print(
            Panel.fit(
                Text("CUSTOMER REGISTRATION", style="heading", justify="center"),
                style="border",
            ),
            justify="center",
        )
        print()
        name = console.input("[input]Enter your name : ")

        cursor.execute("SELECT email FROM customer_table")
        emails = cursor.fetchall()

        while True:
            email = console.input("[input]Enter your email id : ")
            flag = 0
            for i in emails:
                if i[0] == email:
                    flag = 1
            if flag == 1:
                console.print("Email already exists", style="error")
            else:
                break

        while True:
            console.print("Enter your password : ", end="", style="pass")
            password = pwinput(prompt="").encode("utf-8")

            console.print("Confirm your password : ", end="", style="pass")
            con_password = pwinput(prompt="").encode("utf-8")

            if password == con_password:
                console.print("Passwords Match", style="success")
                break
            else:
                console.print("Password are not matching \n", style="error")

        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        q = "INSERT INTO customer_table (customer_name, email, passwd, items) VALUES (%s, %s, %s, '[]')"
        v = (name, email, hashed)
        cursor.execute(q, v)
        conobj.commit()
        console.print("Registered Successfully", style="success")
        console.input("[yellow]Enter a key to continue")

    except Exception as e:
        console.print(
            f"Failed to Register \nPlease try again later \n{e}", style="error"
        )
        console.input("[yellow]Enter a key to continue")


def employee_register():
    try:
        os.system("cls")
        console.print(
            Panel.fit(
                Text("EMPLOYEE REGISTRATION", style="heading", justify="center"),
                style="border",
            ),
            justify="center",
        )
        print()
        name = console.input("[input]Enter your name : ")

        cursor.execute("SELECT email FROM employee_table")
        emails = cursor.fetchall()

        while True:
            email = console.input("[input]Enter your email id : ")
            flag = 0
            for i in emails:
                if i[0] == email:
                    flag = 1
            if flag == 1:
                console.print("Email already exists", style="error")
            else:
                break

        while True:
            console.print("Enter your password : ", end="", style="pass")
            password = pwinput(prompt="").encode("utf-8")

            console.print("Confirm your password : ", end="", style="pass")
            con_password = pwinput(prompt="").encode("utf-8")

            if password == con_password:
                console.print("Passwords Match", style="success")
                break
            else:
                console.print("Password are not matching \n", style="error")

        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        des = console.input("[input]Enter your designation : ")
        sal = FloatPrompt.ask("[yellow]Enter your salary")

        q = "INSERT INTO employee_table (employee_name, email, designation, salary, passwd) VALUES (%s, %s, %s, %s, %s)"
        v = (name, email, des, sal, hashed)
        cursor.execute(q, v)
        conobj.commit()
        console.print("Registered Successfully", style="success")
        console.input("[yellow]Enter a key to continue")

    except Exception as e:
        console.print(
            f"Failed to Register \nPlease try again later \n{e}", style="error"
        )
        console.input("[yellow]Enter a key to continue")


def cart_table_create(cart):
    global cart_table
    cart_table = Table(header_style="bold red", box=box.SIMPLE_HEAD, title="Your Cart")
    cart_table.add_column("Item No", justify="center")
    cart_table.add_column("Item Name", justify="left")
    cart_table.add_column("Category", justify="left")
    cart_table.add_column("Price", justify="right")
    cart_table.add_column("Quantity", justify="right")

    for item in cart:
        cart_table.add_row(str(item[0]), item[1], item[2], str(item[3]), str(item[4]))

    return cart_table


def full_table_create(items):
    full_table = Table(
        header_style="bold red", box=box.SIMPLE_HEAD, title="Items Table"
    )
    full_table.add_column("Item No", justify="center")
    full_table.add_column("Item Name", justify="left")
    full_table.add_column("Category", justify="left")
    full_table.add_column("Price", justify="right")
    full_table.add_column("Stock", justify="right")

    for i in range(len(items)):
        full_table.add_row(
            str(items[i][0]),
            items[i][1],
            items[i][2],
            str(items[i][3]),
            str(items[i][4]),
        )

    return full_table


def items_table_create(items):

    items_table = Table(
        header_style="bold red", box=box.SIMPLE_HEAD, title="Items Table"
    )
    items_table.add_column("Item No", justify="center")
    items_table.add_column("Item Name", justify="left")
    items_table.add_column("Category", justify="left")
    items_table.add_column("Price", justify="right")

    for i in range(len(items)):
        items_table.add_row(
            str(items[i][0]), items[i][1], items[i][2], str(items[i][3])
        )
        items[i] = list(items[i])

    return items_table


def bill_table_create(cart):
    table = Table(header_style="bold red", box=box.SIMPLE_HEAD)
    table.add_column("S No", justify="center")
    table.add_column("Item Name", justify="left")
    table.add_column("Quantity", justify="center")
    table.add_column("Price", justify="right")
    table.add_column("Total", justify="right")

    for i in range(len(cart)):
        table.add_row(
            str(i + 1),
            cart[i][1],
            str(cart[i][4]),
            str(cart[i][3]),
            str(cart[i][3] * cart[i][4]),
        )

    return table


def bill(cart, dt, sub_total, tax, total_cost):
    try:
        os.system("cls")
        console.print(f"{'Your Bill': ^60}", style="BOLD RED")
        q = "SELECT customer_name FROM customer_table WHERE email = '{}'".format(email)
        cursor.execute(q)
        name = cursor.fetchall()[0][0]

        console.print(f"Customer Name : [blue]{name}", style="success")
        console.print(f"Email Address : [blue]{email}", style="success")
        console.print(
            f"Date and Time of Purchase : [blue]{dt.day}/{dt.month}/{dt.year} - {dt.hour}:{dt.minute}",
            style="success",
        )
        console.print(bill_table_create(cart))
        console.print(f"SubTotal : [blue]{sub_total} Rs", style="success")
        console.print("Shipping : [blue]100 Rs", style="success")
        console.print(f"Taxes :  [blue]{tax} Rs", style="success")
        console.print(f"Total : [blue] {total_cost} \n", style="success")

        ch = inquirer.confirm(
            message="Do you want to save the bill as a csv file ?", style=style
        ).execute()
        if ch:
            bill_csv(name, email, dt, cart, sub_total, tax, total_cost)

        console.print(
            "Thank you for shopping at our online supermarket!", style="success"
        )

    except Exception as e:
        console.print(
            f"Your Bill could not be generated \nPlease try again later \n{e}",
            style="error",
        )


def bill_csv(name, email, dt, cart, sub_total, tax, total_cost):
    try:
        file_name = console.input("[yellow]Enter File name : ") + ".csv"
        file_object = open(file_name, "w", newline="")
        wobj = csv.writer(file_object)

        wobj.writerows(
            [
                ["", "", "BILL"],
                ["Name", name],
                ["Email", email],
                ["Date", f"{dt.day}/{dt.month}/{dt.year} - {dt.hour}:{dt.minute}"],
                [
                    "",
                ],
                ["S No", "Item Name", "Quantity", "Price", "Total"],
            ]
        )

        for i in range(len(cart)):
            wobj.writerow(
                [i + 1, cart[i][1], cart[i][4], cart[i][3], cart[i][3] * cart[i][4]]
            )

        wobj.writerows(
            [
                [
                    "",
                ],
                ["", "", "", "Sub Total", sub_total],
                ["", "", "", "Shipping", 100],
                ["", "", "", "Taxes", tax],
                ["", "", "", "Total", total_cost],
            ]
        )

        console.print(
            f"CSV FILE {file_name} has been generated \nPlease check in the program folder \n",
            style="success",
        )
        file_object.close()

        ch = inquirer.confirm(
            message="Do you want to open the csv file on your system now ?", style=style
        ).execute()
        if ch:
            try:
                os.startfile(file_name)
                console.print("File opened", style="success")
            except Exception as e:
                console.print(
                    f"Could not open the file \nPlease make sure a default app is set for opening csv files on your system \n{e}",
                    style="error",
                )
    except Exception as e:
        console.print(
            f"CSV File was not generated \nPlease Try again \n{e}", style="error"
        )
        console.input("[yellow]Enter a key to continue ")


def search_buy():
    global items, itemnos_in_cart
    q = "SELECT item_no, item_name, category, price, stock FROM items_table WHERE stock > 0"
    cursor.execute(q)
    items = cursor.fetchall()
    item_names = []
    for item in items:
        item_names.append(item[1])

    try:
        while True:
            os.system("cls")
            console.print(
                Panel.fit(
                    Text("SEARCH AND BUY", style="heading", justify="center"),
                    style="border",
                ),
                justify="center",
            )
            search = inquirer.fuzzy(
                message="Search for products",
                choices=item_names,
                style=style,
                border=True,
            ).execute()
            while True:
                flag = False
                qty = IntPrompt.ask("[yellow]Enter quantity")
                if qty == 0:
                    console.print(
                        "Quantity cannot be zero \nPlease Enter a non-zero number",
                        style="error",
                    )
                else:
                    for item in items:
                        if item[1] == search:
                            if item[4] < qty:
                                console.print(
                                    f"Limited Stock left \nPlease enter a value less than {item[4] + 1}",
                                    style="error",
                                )
                                flag = True
                                break
                    if not flag:
                        break

            for item in items:
                if item[1] == search:
                    console.print(
                        f"\n[success][i]ITEM DETAILS : [/i][/success]\n Item no : {item[0]} \n Item name : {item[1]} \n Category : {item[2]} \n Price : {item[3]}",
                        style="blue",
                    )
                    brought = list(item)[0:-1]
                    brought.append(qty)
                    break

            itemnos_in_cart.append(str(brought[0]))
            cart.append(brought)
            item_names.remove(search)

            console.print("\nItem added to your cart", style="success")
            ch = inquirer.confirm(message="Continue Shopping ? ", style=style).execute()
            if not ch:
                console.print(
                    "All items successfully added to your cart", style="success"
                )
                spinner = Spinner(
                    "point",
                    text=Text(f"Continuing to confirm purchase", style="green"),
                    style="green",
                )
                with Live(spinner, refresh_per_second=20) as live:
                    for i in range(7):
                        time.sleep(0.2)
                break
    except Exception as e:
        console.print(f"Could not perform the action \n{e}", style="error")
        console.input("[yellow]Enter a key to continue ")


def confirm_purchase():
    global items, cart, itemnos_in_cart

    os.system("cls")
    console.print(
        Panel.fit(
            Text("CONFIRMATION MENU", style="heading", justify="center"), style="border"
        ),
        justify="center",
    )

    console.print(cart_table_create(cart))

    sub_total = 0
    for i in cart:
        sub_total += i[3] * i[4]
    tax = sub_total / 10
    total_cost = sub_total + tax + 100

    console.print(f"Total Bill = [blue]{sub_total}", style="success")
    ch = inquirer.confirm(message="Confirm your purchase ", style=style).execute()
    if ch:
        try:
            q = "SELECT * FROM customer_table WHERE email = %s"
            v = (email,)
            cursor.execute(q, v)
            userinfo = cursor.fetchall()

            db_purchase = userinfo[0][4]
            db_purchase += total_cost

            db_points = userinfo[0][5]
            db_points += (total_cost / 100) * 5

            current_order = []
            dt = datetime.datetime.now()
            current_order.append(
                f"{dt.day}/{dt.month}/{dt.year} - {dt.hour}:{dt.minute}"
            )
            for i in itemnos_in_cart:
                current_order.append(int(i))

            items = eval(userinfo[0][3])
            items.append(current_order)

            for item in cart:
                q = "UPDATE items_table SET stock = stock - %s where item_no = %s"
                v = (item[4], item[0])
                cursor.execute(q, v)
                conobj.commit()

            q = "UPDATE customer_table SET total_purchase = %s, points = %s, items = %s WHERE email = %s"
            v = (db_purchase, db_points, str(items), email)
            cursor.execute(q, v)
            conobj.commit()
            console.print("Purchase Confirmed \n", style="success")
            console.print("Generating your bill")
            bill(cart, dt, sub_total, tax, total_cost)
            console.input("[success]Enter a key to continue")

        except Exception as e:
            console.print(
                f"Failed to Confirm your Purchase \nPlease try again later \n{e}",
                style="error",
            )
            console.input("[success]Enter a key to continue")

    else:
        console.print("Purchase cancelled", style="error")
        console.input("[success]Enter a key to continue")

    cart = []
    itemnos_in_cart = []


def edit_quantity(items, cart):
    os.system("cls")
    console.print(
        Panel.fit(
            Text("EDIT QUANTITY", style="heading", justify="center"), style="border"
        ),
        justify="center",
    )

    try:
        console.print(cart_table_create(cart))
        item_no = IntPrompt.ask(
            "[yellow]Enter the item no to edit",
            choices=itemnos_in_cart,
            show_choices=False,
        )
        for i in range(len(items)):
            if items[i][0] == item_no:
                stock = items[i][4]

        while True:
            qty = IntPrompt.ask("[yellow]Enter new quantity")
            if qty < stock:
                for i in range(len(cart)):
                    if cart[i][0] == item_no:
                        cart[i][4] = qty
                console.print("Quantity changed successfully", style="success")
                console.print(cart_table_create(cart))
                console.input("[yellow]Enter a key to continue")
                break
            else:
                console.print("Limited Stock Left", style="error")
                console.print(
                    f"Please Enter a value less than {stock + 1}", style="error"
                )
                console.input("[yellow]Enter a key to continue")
    except Exception as e:
        console.print(f"\nQuantity was not changed \n{e}", style="error")
        console.input("[yellow]Enter a key to continue")


def remove_cart(cart, itemnos_in_cart):
    try:
        console.print(cart_table_create(cart))
        item_no = IntPrompt.ask(
            "[yellow]Enter item no to remove",
            choices=itemnos_in_cart,
            show_choices=False,
        )
        ch = inquirer.confirm(
            message=f"Confirm to remove item no {item_no}", style=style
        ).execute()
        if ch:
            for item in cart:
                if item[0] == item_no:
                    cart.remove(item)
        itemnos_in_cart.remove(str(item_no))
        print()
        console.print(cart_table_create(cart))
        console.print("Item removed from your cart", style="success")
        console.input("[yellow]Enter a key to continue")
    except Exception as e:
        console.print(f"\nItem was not removed from your cart \n{e}", style="error")
        console.input("[yellow]Enter a key to continue")


def buy():
    try:
        global cart, itemnos_in_cart
        search_buy()
        while True:
            os.system("cls")
            console.print(
                Panel.fit(
                    Text("SHOPPING MENU", style="heading", justify="center"),
                    style="border",
                ),
                justify="center",
            )
            ch = inquirer.select(
                message="Select your choice",
                style=style,
                choices=["Confirm Purchase", "Edit your cart", "Cancel Purchase"],
            ).execute()

            if ch == "Confirm Purchase":
                confirm_purchase()
                break

            elif ch == "Edit your cart":
                while True:
                    os.system("cls")
                    console.print(
                        Panel.fit(
                            Text("EDIT CART", style="heading", justify="center"),
                            style="border",
                        ),
                        justify="center",
                    )
                    ch = inquirer.select(
                        message="Select your choice",
                        style=style,
                        choices=[
                            "Change Quantity",
                            "Remove an Item",
                            "Return to Shopping Menu",
                        ],
                    ).execute()
                    if ch == "Change Quantity":
                        edit_quantity(items, cart)
                    elif ch == "Remove an Item":
                        remove_cart(cart, itemnos_in_cart)
                    elif ch == "Return to Shopping Menu":
                        break

            elif ch == "Cancel Purchase":
                console.print("Purchase Cancelled", style="error")
                cart = []
                itemnos_in_cart = []
                break
    except Exception as e:
        console.print(
            f"Could not access buy menu \nPlease try again later \n{e}", style="error"
        )
        console.input("[yellow]Enter a key to continue ")


def item_insert():
    os.system("cls")
    console.print(
        Panel.fit(
            Text("INSERT ITEM", style="heading", justify="center"), style="border"
        ),
        justify="center",
    )

    item_name = console.input("[input]Enter item name : ").title()
    category = console.input("[input]Enter category : ").title()
    price = FloatPrompt.ask("[yellow]Enter your price")
    stock = IntPrompt.ask("[yellow]Enter stock")
    try:
        q = "INSERT INTO items_table (item_name, category, price, stock) VALUES (%s, %s, %s, %s)"
        v = (item_name, category, price, stock)
        cursor.execute(q, v)
        conobj.commit()
        console.print("Item inserted", style="success")
        console.input("[success]Enter a key to continue")
    except Exception as e:
        console.print(
            f"\nCould not insert item \nPlease try again later\n{e}", style="error"
        )
        console.input("[yellow]Enter a key to continue ")


def remove_item():
    try:
        cursor.execute("SELECT * FROM items_table")
        items = cursor.fetchall()
        console.print(full_table_create(items))
        item_nos = []
        for i in items:
            item_nos.append(str(i[0]))
        item_no = IntPrompt.ask(
            "Enter item no to remove", choices=item_nos, show_choices=False
        )
        q = "DELETE FROM items_table WHERE item_no = %s"
        v = (item_no,)
        cursor.execute(q, v)
        conobj.commit()
        console.print("Item Removed", style="success")
        console.input("[yellow]Enter a key to continue ")
    except Exception as e:
        console.print(
            "Could not remove the item \nPlease try again later \n", e, style="error"
        )
        console.input("[yellow]Enter a key to continue ")


def view_items():
    try:
        while True:
            os.system("cls")
            console.print(
                Panel.fit(
                    Text("VIEW MENU", style="heading", justify="center"), style="border"
                ),
                justify="center",
            )
            ch = inquirer.select(
                message="Select your choice",
                style=style,
                choices=[
                    "Sort by Price",
                    "Group by Category",
                    "View items out of stock",
                    "Return to Customer Menu",
                ],
            ).execute()

            if ch == "Sort by Price":
                q = "SELECT item_no, item_name, category, price FROM items_table ORDER BY price"
                cursor.execute(q)
                items = cursor.fetchall()
                console.print(items_table_create(items))
                console.input("[success]Press any key to continue ")

            elif ch == "Group by Category":
                q = "SELECT distinct category FROM items_table"
                cursor.execute(q)

                cats = []
                for i in cursor.fetchall():
                    cats.append(i[0])

                ch = inquirer.select(
                    message="Select your category",
                    multiselect=True,
                    style=style,
                    choices=cats,
                ).execute()
                selected = str(ch)
                selected = selected[1:-1]
                selected = "(" + selected + ")"

                q = "SELECT item_name, category, price FROM items_table WHERE category IN {}".format(
                    selected
                )
                cursor.execute(q)
                rec = cursor.fetchall()

                def get_content(x):
                    name = rec[x][0].title()
                    category = rec[x][1].title()
                    price = rec[x][2]
                    return f"[bold red]{name}[/bold red] - [yellow]₹{price}\n{category}"

                item_renderables = [
                    Panel(get_content(x), expand=True) for x in range(len(rec))
                ]
                console.print(Columns(item_renderables))
                console.input("[success]Press any key to continue ")

            elif ch == "View items out of stock":
                q = "SELECT item_no, item_name, category, price FROM items_table WHERE stock = 0"
                cursor.execute(q)
                items = cursor.fetchall()
                console.print(items_table_create(items))
                console.input("[success]Press any key to continue ")

            elif ch == "Return to Customer Menu":
                break

    except Exception as e:
        console.print(
            f"Could not view items \nPlease try again later \n{e}", style="error"
        )
        console.input("[success]Press any key to continue ")


def edit_items():
    os.system("cls")
    console.print(
        Panel.fit(Text("EDIT ITEM", style="heading", justify="center"), style="border"),
        justify="center",
    )
    q = "SELECT * FROM items_table"
    cursor.execute(q)
    items = cursor.fetchall()
    console.print(full_table_create(items))
    item_nos = []
    for i in items:
        item_nos.append(str(i[0]))
    item_no = IntPrompt.ask(
        "[yellow]Enter item no you want to edit", choices=item_nos, show_choices=False
    )
    try:
        item_name = console.input("[input]Enter new item name : ").title()
        category = console.input("[input]Enter new category : ").title()
        price = FloatPrompt.ask("[yellow]Enter new price")
        stock = IntPrompt.ask("[yellow]Enter new stock")
        q = "UPDATE items_table SET item_name = %s, category = %s, price = %s, stock = %s WHERE item_no = %s"
        v = (item_name, category, price, stock, item_no)
        cursor.execute(q, v)
        conobj.commit()
        console.print("Item info edited !!!", style="success")
        console.input("[success]Enter a key to continue")
    except Exception as e:
        console.print(
            f"Failed to edit item info \nPlease Try again later \n{e}", style="error"
        )
        console.input("[success]Enter a key to continue")


def search():
    try:
        q = "SELECT item_name FROM items_table"
        cursor.execute(q)
        items_names = []
        for i in cursor.fetchall():
            items_names.append(i[0])
        while True:
            os.system("cls")
            console.print(
                Panel.fit(
                    Text("SEARCH", style="heading", justify="center"), style="border"
                ),
                justify="center",
            )
            search = inquirer.fuzzy(
                message="Enter search query : ", style=style, choices=items_names
            ).execute()
            cursor.execute(
                "SELECT * FROM items_table WHERE item_name = '{}'".format(search)
            )
            search_result = cursor.fetchall()
            item = search_result[0]
            console.print(
                f"\n[success][i]ITEM DETAILS : [/i][/success]\n Item no : {item[0]} \n Item name : {item[1]} \n Category : {item[2]} \n Price : {item[3]} \n",
                style="blue",
            )
            ch = inquirer.confirm(
                message="Continue Searching ? ", style=style
            ).execute()
            if not ch:
                break

    except Exception as e:
        console.print(
            "Could not search at the moment \nPlease try again later \n",
            e,
            style="error",
        )
        console.input("[success]Enter a key to continue")


def edit_customer(rec):
    global email
    os.system("cls")
    console.print(
        Panel.fit(
            Text("EDIT CUSTOMER ACCOUNT", style="heading", justify="center"),
            style="border",
        ),
        justify="center",
    )
    try:
        f = 0
        cid = rec[0]
        while True:
            name = console.input("[yellow]Enter your new name : ")
            while True:
                if f == 1:
                    break
                email = console.input("[yellow]Enter your new email : ")
                q = "SELECT email FROM customer_table"
                cursor.execute(q)
                for i in cursor.fetchall():
                    if i[0] == email:
                        console.print(
                            "An account with this email already exists \nPlease provide a new email",
                            style="error",
                        )
                        spinner = Spinner(
                            "point",
                            text=Text(
                                f"Going back to customer account page", style="red"
                            ),
                            style="red",
                        )
                        with Live(spinner, refresh_per_second=20) as live:
                            for i in range(7):
                                time.sleep(0.2)
                        f = 1
                        break
                else:
                    break

            if f == 1:
                break
            q = "UPDATE customer_table SET customer_name = %s, email = %s WHERE customer_id = %s"
            v = (name, email, cid)
            cursor.execute(q, v)
            conobj.commit()
            console.print("User Details Updated !!", style="success")
            spinner = Spinner(
                "point",
                text=Text(f"Going back to customer account page", style="green"),
                style="green",
            )
            with Live(spinner, refresh_per_second=20) as live:
                for i in range(7):
                    time.sleep(0.2)
            break
    except Exception as e:
        console.print(
            "Could not update customer details \nPlease try again later \n",
            e,
            style="error",
        )
        spinner = Spinner(
            "point",
            text=Text(f"Going back to customer account page", style="red"),
            style="red",
        )
        with Live(spinner, refresh_per_second=20) as live:
            for i in range(15):
                time.sleep(0.2)


def change_pass(user):
    os.system("cls")
    console.print(
        Panel.fit(
            Text("CHANGE PASSWORD", style="heading", justify="center"), style="border"
        ),
        justify="center",
    )
    f = 0
    while True:
        try:
            if f == 1:
                break
            console.print("Enter your current password : ", style="pass", end="")
            current_pass = pwinput(prompt="").encode("utf-8")
            q = f"SELECT passwd FROM {user}_table WHERE email = %s"
            v = (email,)
            cursor.execute(q, v)
            rec = cursor.fetchall()
            hashed_pass = rec[0][0].encode("utf-8")

            if bcrypt.checkpw(current_pass, hashed_pass):
                console.print("Authenticated", style="success")
                while True:
                    console.print("Enter your new password : ", style="pass", end="")
                    new_pass = pwinput(prompt="")
                    console.print("Confirm your password : ", style="pass", end="")
                    con_pass = pwinput(prompt="")
                    if new_pass == con_pass:
                        new_hash = bcrypt.hashpw(
                            new_pass.encode("utf-8"), bcrypt.gensalt()
                        )
                        q = f"UPDATE {user}_table SET passwd = %s WHERE email = %s"
                        v = (new_hash, email)
                        cursor.execute(q, v)
                        conobj.commit()
                        console.print("Password Changed !!", style="success")
                        f = 1
                        spinner = Spinner(
                            "point",
                            text=Text(
                                f"Continuing customer account page", style="green"
                            ),
                            style="green",
                        )
                        with Live(spinner, refresh_per_second=20) as live:
                            for i in range(7):
                                time.sleep(0.2)
                        break
                    else:
                        console.print(
                            "Confirmation password does not match with your password",
                            style="error",
                        )
        except Exception as e:
            console.print(
                f"Failed to change your password \nPlease Try again later \n{e}",
                style="error",
            )
            spinner = Spinner(
                "point",
                text=Text(f"Going back to customer account page", style="red"),
                style="red",
            )
            with Live(spinner, refresh_per_second=20) as live:
                for i in range(15):
                    time.sleep(0.2)
        else:
            console.print("Password entered is not correct", style="error")


def orders(rec):
    try:
        os.system("cls")
        console.print(
            Panel.fit(
                Text("VIEW PAST ORDERS", style="heading", justify="center"),
                style="border",
            ),
            justify="center",
        )
        orders_info = eval(rec[3])
        dates = []
        for order in orders_info:
            dates.append(order[0])
        dates = dates[::-1]
        date = inquirer.select(
            message="Select the date on which you made the purchase",
            style=style,
            choices=dates,
        ).execute()
        for order in orders_info:
            if order[0] == date:
                item_nos = tuple((order[1:]))
                break

        if len(item_nos) == 1:
            q = "SELECT item_no, item_name, category, price FROM items_table WHERE item_no = {}".format(
                item_nos[0]
            )
        else:
            q = "SELECT item_no, item_name, category, price FROM items_table WHERE item_no IN {}".format(
                item_nos
            )
        cursor.execute(q)
        order_info = cursor.fetchall()
        console.print(f"Items brought on {date} are ", style="success")
        console.print(items_table_create(order_info))
        console.input("[yellow]Enter a key to continue ")
    except Exception as e:
        console.print(f"Failed to retrieve your past orders \n{e}", style="error")
        console.input("Enter a key to continue ")


def delete_account(user, rec):
    os.system("cls")
    console.print(
        Panel.fit(
            Text("DELETE ACCOUNT", style="heading", justify="center"), style="border"
        ),
        justify="center",
    )
    console.print(
        "Deleting account is permanent. This action is [b][i]irreversible[/b][/i]",
        style="red blink",
    )
    ch = inquirer.confirm(
        message="Confirm to delete your account ? ", style=style
    ).execute()

    if ch:
        try:
            console.print("Enter your current password : ", style="pass", end="")
            current_pass = pwinput(prompt="").encode("utf-8")
            hashed_pass = rec[6].encode("utf-8")
            if bcrypt.checkpw(current_pass, hashed_pass):
                conf = Prompt.ask(
                    "[yellow]ENTER 'YES' to delete your account or 'NO' to cancel",
                    choices=["YES", "NO"],
                )
                if conf == "YES":
                    q = "delete from {}_table where email = '{}'".format(user, email)
                    cursor.execute(q)
                    conobj.commit()
                    console.print("Account Deleted", style="success")
                    for i in track(range(5), description="Signing out in..."):
                        time.sleep(1)
                    exit()
                else:
                    console.print("Account Not Deleted", style="success")
                    console.input("[success]Enter any key to continue")
        except Exception as e:
            console.print(
                f"Could not delete your account \nPlease Try again later \n{e}"
            )
            console.input("[success]Enter any key to continue")

        else:
            console.print("Password is incorrect", style="error")
            console.input("[error]Enter any key to continue")

    else:
        console.print("Account not deleted", style="success")
        console.input("[success]Enter any key to continue")


def account_stats(rec):
    try:
        if len(eval(rec[3])) != 0:
            os.system("cls")
            console.print(
                Panel.fit(
                    Text("ACCOUNT STATS", style="heading", justify="center"),
                    style="border",
                ),
                justify="center",
            )
            console.print(f"Total Purchase : [blue]{float(rec[4])}", style="success")
            console.print(f"Total Points : [blue]{float(rec[5])}", style="success")
            items = eval(rec[3])
            today = datetime.date.today()

            dt = items[-1][0].split()[0].split("/")
            last_dt = datetime.date(int(dt[2]), int(dt[1]), int(dt[0]))

            dt = items[0][0].split()[0].split("/")
            first_dt = datetime.date(int(dt[2]), int(dt[1]), int(dt[0]))

            console.print(
                f"\nLast Purchase was made on : [blue]{items[-1][0]}", style="success"
            )
            console.print(
                f"Last Purchase was made [blue]{(today - last_dt).days} day(s) ago",
                style="success",
            )

            console.print(
                f"\nFirst Purchase was made on : [blue]{items[0][0]}", style="success"
            )
            console.print(
                f"First Purchase was made [blue]{(today - first_dt).days} day(s) ago \n",
                style="success",
            )

            console.input("[success]Enter any key to continue")
        else:
            console.print(
                "Please make a purchase before visiting this page", style="error"
            )
            spinner = Spinner(
                "point",
                text=Text(f"Going Back to customer account page", style="red"),
                style="red",
            )
            with Live(spinner, refresh_per_second=20) as live:
                for i in range(8):
                    time.sleep(0.2)
    except Exception as e:
        console.print(
            f"Could not access your account stats \nPlease Try again later \n{e}"
        )
        spinner = Spinner(
            "point",
            text=Text(f"Going Back to customer account page", style="green"),
            style="green",
        )
        with Live(spinner, refresh_per_second=20) as live:
            for i in range(8):
                time.sleep(0.2)


def customer_account():
    try:
        while True:
            os.system("cls")
            console.print(
                Panel.fit(
                    Text("CUSTOMER ACCOUNT", style="heading", justify="center"),
                    style="border",
                ),
                justify="center",
            )
            ch = inquirer.select(
                message="Select your choice",
                style=style,
                choices=[
                    "Account Stats",
                    "View Past Orders",
                    "Edit Account Details",
                    "Change Password",
                    "Delete your Account",
                    "Return to Customer Menu",
                ],
            ).execute()

            q = "SELECT * FROM customer_table WHERE email = %s"
            v = (email,)
            cursor.execute(q, v)
            customer_info = cursor.fetchall()[0]

            if ch == "Account Stats":
                account_stats(customer_info)
            elif ch == "View Past Orders":
                orders(customer_info)
            elif ch == "Edit Account Details":
                edit_customer(customer_info)
            elif ch == "Change Password":
                change_pass("customer")
            elif ch == "Delete your Account":
                delete_account("customer", customer_info)
            elif ch == "Return to Customer Menu":
                break
    except Exception as e:
        console.print(f"Could not access your account \nPlease Try again later \n{e}")
        console.input("[yellow]Enter a key to continue")


def edit_employee(rec):
    global email
    os.system("cls")
    console.print(
        Panel.fit(
            Text("EDIT EMPLOYEE ACCOUNT", style="heading", justify="center"),
            style="border",
        ),
        justify="center",
    )
    try:
        f = 0
        eid = rec[0]
        while True:
            name = console.input("[yellow]Enter your new name : ")
            while True:
                if f == 1:
                    break
                email = console.input("[yellow]Enter your new email : ")
                q = "SELECT email FROM employee_table"
                cursor.execute(q)
                for i in cursor.fetchall():
                    if i[0] == email:
                        console.print(
                            "An account with this email already exists \nPlease provide a new email",
                            style="error",
                        )
                        console.input("[input]Enter a key to go back")
                        f = 1
                        break
                else:
                    break
            if f == 1:
                break
            des = console.input("[yellow]Enter your new designation : ")
            sal = FloatPrompt.ask("[yellow]Enter your new salary")

            q = "UPDATE employee_table SET employee_name = %s, email = %s, designation = %s, salary = %s WHERE employee_id = %s"
            v = (name, email, des, sal, eid)
            cursor.execute(q, v)
            conobj.commit()
            console.print("Employee Details Updated !!", style="success")
            console.input("[yellow]Enter a key to continue")
            break

    except Exception as e:
        console.print(
            "Could not update employee details \nPlease try again later \n",
            e,
            style="error",
        )


def employee_account():
    while True:
        try:
            os.system("cls")
            console.print(
                Panel.fit(
                    Text("EMPLOYEE ACCOUNT", style="heading", justify="center"),
                    style="border",
                ),
                justify="center",
            )
            ch = inquirer.select(
                message="Select your choice",
                style=style,
                choices=[
                    "Edit Account Details",
                    "Change Password",
                    "Delete your Account",
                    "Return to Employee Menu",
                ],
            ).execute()

            q = "SELECT * FROM employee_table WHERE email = %s"
            v = (email,)
            cursor.execute(q, v)
            employee_info = cursor.fetchall()[0]

            if ch == "Edit Account Details":
                edit_employee(employee_info)
            elif ch == "Change Password":
                change_pass("employee")
            elif ch == "Delete your Account":
                delete_account("employee", employee_info)
            elif ch == "Return to Employee Menu":
                break
        except Exception as e:
            console.print(
                f"Could not access your account \nPlease Try again later \n{e}"
            )
            console.input("[yellow]Enter a key to continue")


while True:
    os.system("cls")
    console.print(
        Panel.fit(
            Text("SHOP MANAGEMENT", style="heading", justify="center"),
            title="Welcome",
            style="border",
        ),
        justify="center",
    )
    ch = inquirer.select(
        message="Select your choice",
        style=style,
        choices=["Customer Login", "Employee Login", "Register", "Quit"],
    ).execute()

    if ch == "Customer Login":
        email, x = sign_in("customer")
        if x:
            while True:
                os.system("cls")
                console.print(
                    Panel.fit(
                        Text("CUSTOMER MENU", style="heading", justify="center"),
                        style="border",
                    ),
                    justify="center",
                )
                ch = inquirer.select(
                    message="Select your choice",
                    style=style,
                    choices=[
                        "Buy Items",
                        "View Items",
                        "Search for an Item",
                        "Account Details",
                        "Sign Out",
                    ],
                ).execute()
                if ch == "Buy Items":
                    buy()
                elif ch == "View Items":
                    view_items()
                elif ch == "Search for an Item":
                    search()
                elif ch == "Account Details":
                    customer_account()
                elif ch == "Sign Out":
                    print("Going back to Main Menu....")
                    break

        else:
            console.print(
                "Could not authenticate you \nPlease Try again Later", style="error"
            )
            spinner = Spinner(
                "point", text=Text(f"Quitting Program", style="red"), style="red"
            )
            with Live(spinner, refresh_per_second=20) as live:
                for i in range(7):
                    time.sleep(0.2)
            break

    elif ch == "Employee Login":
        email, x = sign_in("employee")
        if x:
            while True:
                os.system("cls")
                console.print(
                    Panel.fit(
                        Text("EMPLOYEE MENU", style="heading", justify="center"),
                        style="border",
                    ),
                    justify="center",
                )
                ch = inquirer.select(
                    message="Select your choice",
                    style=style,
                    choices=[
                        "Insert a New Item",
                        "Edit an Existing Item",
                        "Search for an Item",
                        "Delete an Item",
                        "Account Details",
                        "Sign Out",
                    ],
                ).execute()
                if ch == "Insert a New Item":
                    item_insert()
                elif ch == "Edit an Existing Item":
                    edit_items()
                elif ch == "Search for an Item":
                    search()
                elif ch == "Delete an Item":
                    remove_item()
                elif ch == "Account Details":
                    employee_account()
                elif ch == "Sign Out":
                    console.print("Returning to Main Menu.....", style="success")
                    break
        else:
            console.print(
                "Could not authenticate you \nPlease Try again Later", style="error"
            )
            spinner = Spinner(
                "point", text=Text(f"Quitting Program", style="red"), style="red"
            )
            with Live(spinner, refresh_per_second=20) as live:
                for i in range(7):
                    time.sleep(0.2)

    elif ch == "Register":
        while True:
            os.system("cls")
            console.print(
                Panel.fit(
                    Text("REGISTRATION MENU", style="heading", justify="center"),
                    style="border",
                ),
                justify="center",
            )
            ch = inquirer.select(
                message="Select your choice",
                style=style,
                choices=[
                    "Customer Registration",
                    "Employee Registration",
                    "Return to Main Menu",
                ],
            ).execute()
            if ch == "Customer Registration":
                customer_register()
                break
            elif ch == "Employee Registration":
                employee_register()
                break
            elif ch == "Return to Main Menu":
                console.print("Thank You", style="success")
                break

    elif ch == "Quit":
        console.print("Quitting.....\nThank You", style="success")
        cursor.close()
        conobj.close()
        break
