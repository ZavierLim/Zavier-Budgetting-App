# Zavier's Budgetting App
#### Video Demo:  https://youtu.be/GXZg6Fnv9qw
#### Description:
This is a budgetting app where you can add and delete categories, add and delete transactions, and also your remaining budget.I have practiced al of the CRUD functions of interacting with the SQl database.Firstly, i have implemented a login function, with registration. if not registered, the user will not be able to login. After a user is registered, the details will be stored in the SQL server (password hashed) and the user wil be able to login.
THe files i have written are:
1.application.py (contains the main route and the functions as well as the get and post methods to each HTML)
2.login.html -to handle logins
3.index.html - to handle the main summary page which shows the budget, total spent, and the remaining budget/deficit
4.add.html - to add transactions
5. category.html- to add new categories
6. deletet.html- to delete transactions
7. deletecategory.html- to delete category
8. layout.html- this is the layout template as well as the cover page for the buttons
    this is the buttons:
                       <li class="nav-item"><a class="nav-link text-white" href="/add">Add Transactions</a></li>
                        <li class="nav-item"><a class="nav-link text-white" href="/deletet">Delete Transactions</a></li>
                        <li class="nav-item"><a class="nav-link text-white" href="/category">Add Category</a></li>
                        <li class="nav-item"><a class="nav-link text-white" href="/deletecategory">Delete Category</a></li>
                        <li class="nav-item"><a class="nav-link text-white" href="/transactions">Your Transactions </a></li>
                        <li class="nav-item"><a class="nav-link text-white" href="/">Your Budget </a></li>
                    </ul>
                    <ul class="navbar-nav ml-auto mt-2">
                        <li class="nav-item"><a class="nav-link text-white" href="/logout">Log Out</a></li>
                    </ul>
                {% else %}
                    <ul class="navbar-nav ml-auto mt-2">
                        <li class="nav-item"><a class="nav-link text-white" href="/register">Register</a></li>
                        <li class="nav-item"><a class="nav-link text-white" href="/login">Log In</a></li>
                    </ul>

9. register.html- this is to handle the registrations
10. apology.html - an error page, similar to finance50

Database here:
budget.db - contains a few table:
BUDGET.DB
CREATE TABLE users (id INTEGER, username TEXT NOT NULL, hash TEXT NOT NULL, PRIMARY KEY(id));
CREATE UNIQUE INDEX username ON users (username);
CREATE TABLE transactions(user_id TEXT,category TEXT,addamount NUMERIC,notes TEXT,datetime datetime,FOREIGN KEY(user_id) REFERENCES users(id));
CREATE TABLE categories (id TEXT, category TEXT NOT NULL, budget NUMERIC, totalbudget NUMERIC, remaining NUMERIC, notes TEXT,FOREIGN KEY(id) REFERENCES users(id));

helpers.py- contains some helper functions


