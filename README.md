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
9. register.html- this is to handle the registrations
10. apology.html - an error page, similar to finance50

Database here:
budget.db - contains a few table:

helpers.py- contains some helper functions


