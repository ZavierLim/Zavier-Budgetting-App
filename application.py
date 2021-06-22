import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///budget.db")


@app.route("/")
@login_required
def index():
    budget=db.execute("SELECT * FROM categories WHERE id=?",session.get("user_id"))
    return render_template("index.html",Stocks=budget)

@app.route("/deletet", methods=["GET", "POST"])
@login_required
def deletet():
    if request.method=="GET":
        alltransactions=db.execute("SELECT * FROM transactions WHERE user_id=?",session.get("user_id"))
        return render_template("deletet.html",transactions=alltransactions)
    if request.method=="POST":
        deletet=request.form.get("deletet") #this gives the date

        #get the category and amount that is to be deleted
        toaddback=db.execute("SELECT addamount FROM transactions WHERE user_id=? and datetime=?",session.get("user_id"),deletet)
        categorytoadd=db.execute("SELECT category FROM transactions WHERE user_id=? and datetime=?",session.get("user_id"),deletet)

        #get the numbers
        number=toaddback[0]['addamount']
        categorynumber=categorytoadd[0]['category']

        #delete from transactions
        db.execute("DELETE FROM transactions WHERE user_id=? and datetime=?",session.get("user_id"),deletet)

        #add to budget
        budget=db.execute("SELECT budget FROM categories WHERE id=? and category=?",session.get("user_id"),categorynumber)
        actualbudget=budget[0]['budget']

        #current+deleted
        budgetleft=actualbudget-int(number) #300+50=350

        #remamining
        tbudget=db.execute("SELECT totalbudget FROM categories WHERE id=? and category=?",session.get("user_id"),categorynumber)
        totalbudget=tbudget[0]['totalbudget'] #1000
        remaining=int(totalbudget)-int(budgetleft) #1000-350

        db.execute("UPDATE categories SET budget = ?,remaining=? WHERE id=? and category=?",budgetleft,remaining,session.get("user_id"),categorynumber)

    flash("Deleted transaction!")
    return redirect("/")

@app.route("/category", methods=["GET", "POST"])
@login_required
def category():
    if request.method=="GET":
        return render_template("category.html")
    if request.method=="POST":
        addcategory=request.form.get("newcategory")
        addamount=request.form.get("budget")
        addnotes=request.form.get("notes")
        spending=int(0)

        if not addcategory or not addamount or not addnotes or not addamount.isdigit():
            return apology("error in values")


        db.execute("INSERT INTO categories (id,category,budget,totalbudget,remaining,notes) VALUES(?,?,?,?,?,?)",session.get("user_id"),addcategory,spending,addamount,addamount,addnotes)
    flash("Updated Category!")
    return redirect("/")

@app.route("/deletecategory", methods=["GET", "POST"])
@login_required
def deletecategory():
    if request.method=="GET":
        allcategory=db.execute("SELECT DISTINCT(category) FROM categories WHERE id=?",session.get("user_id"))
        #symbol
        #A
        #B
        #AAPL
        return render_template("deletecategory.html",categories=allcategory)

    if request.method=="POST":
        deletecategory=request.form.get("deletecategory")
        if not deletecategory:
            return apology("error in values")

    db.execute("DELETE FROM categories WHERE id=? and category=?",session.get("user_id"),deletecategory)
    flash("Deleted Category!")
    return redirect("/")


@app.route("/transactions")
@login_required
def transaction():
    alltransactions=db.execute("SELECT * FROM transactions WHERE user_id=?",session.get("user_id"))
    return render_template("transactions.html",Stocks=alltransactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")




@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method=="GET":
        allcategory=db.execute("SELECT DISTINCT(category) FROM categories WHERE id=?",session.get("user_id"))
        #symbol
        #A
        #B
        #AAPL
        return render_template("add.html",categories=allcategory)

    if request.method=="POST":
        addcategory=request.form.get("category")
        addamount=request.form.get("amount")
        addnotes=request.form.get("notes")

        if not addcategory or not addamount or not addnotes or not addamount.isdigit():
            return apology("error in values")

        lookeddate=datetime.now()


        db.execute("INSERT INTO transactions (user_id,category,addamount,notes,datetime) VALUES(?,?,?,?,?)",session.get("user_id"),addcategory,addamount,addnotes,lookeddate)

        #spent
        budget=db.execute("SELECT budget FROM categories WHERE id=? and category=?",session.get("user_id"),addcategory)
        actualbudget=budget[0]['budget'] #0

        #current-newtransaction
        budgetleft=actualbudget+int(addamount) #0+50

        #remamining budget
        tbudget=db.execute("SELECT totalbudget FROM categories WHERE id=? and category=?",session.get("user_id"),addcategory)
        totalbudget=tbudget[0]['totalbudget'] #1000
        remaining=int(totalbudget)-int(budgetleft) #1000-50

        db.execute("UPDATE categories SET budget = ?,remaining=? WHERE id=? and category=?",budgetleft,remaining,session.get("user_id"),addcategory)
    flash("Brought!")
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    """Register user"""
    if request.method=="GET":
        return render_template("register.html")
    else:
        username=request.form.get("username")
        password=request.form.get("password")
        password2=request.form.get("confirmation")

        if not username or not password or not password2 or password!=password2:
            return apology("from register")


        encrypted=generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (username,hash) VALUES(?, ?)", username, encrypted)
        except:
            return apology("username taken")

        return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
