## SHOP MANAGEMENT SYSTEM

This is a Python-based online supermarket application that utilizes MySQL as a database and provides a command-line interface (CLI) for user interaction.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/arjun-mec/Shop-Management-Python?quickstart=1)

### Features

- **User Authentication:** Customers and employees can register with unique credentials and securely log in.
- **Customer Functionality:**
  - Browse available items, sort by price, and filter by category.
  - Search for specific items.
  - Add items to cart, adjust quantities, and remove items.
  - Confirm purchases and generate bills (with optional CSV export).
  - View past order history and account statistics.
  - Manage account details and passwords.
  - Delete their accounts.
- **Employee Functionality:**
  - Add new items to the inventory.
  - Edit existing item details.
  - Delete items from the inventory.
  - Search for items (similar to customer functionality).
  - Manage account details and passwords.
  - Delete their accounts.

### Technologies Used

- **Python:** Core programming language for the application logic.
- **MySQL:** Relational database management system for storing user data, items, and orders.
- **Libraries:** Required libraries are listed in the `requirements.txt` file.

### How to Run

1. **Prerequisites:**
   - Ensure you have Python installed on your system.
   - Install the required libraries from the `requirements.txt` file:
     ```bash
     pip install -r requirements.txt
     ```
2. **Database Setup:**
   - Create a MySQL database and update the connection details in the script.
   - Create the necessary tables (customer_table, employee_table, items_table) using the provided schema.
3. **Configuration:**
   - Replace placeholder values like `host_name`, `user_name`, `db_password`, and `db_name` with your actual database credentials.
4. **Run the Application:**
   - Execute the Python script from your terminal.
   - Follow the interactive prompts to navigate through the application.
