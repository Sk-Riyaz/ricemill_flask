from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from flask_user import roles_required
from werkzeug.urls import url_parse

from app import app
from app.forms import LoginForm, RegistrationForm, PurchaseForm, SalesForm
from app.models import User


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("User already loggedin")
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        #flash('Login requested for user {}, remember_me={}'.format(
        #    form.username.data, form.remember_me.data))

        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid user or password")
            return redirect(url_for('login'))
        flash("User loggedin")
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        print(current_user.is_admin())
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)

    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
@login_required
@roles_required(['SUPER_USER'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("Successfully")
        pass
    return render_template("register.html", form=form)


@app.route('/home')
@login_required
def home():
    genericData = {
        "title": "Home",
        "heading": "Home"
    }
    print(current_user.id)
    return render_template("home.html", data=genericData)


@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    genericData = {
        "title": "Purchase",
        "heading": "Purchase"
    }

    form = PurchaseForm()
    if form.validate_on_submit():
        flash("Purchase inserted Successfully")
        print("Purchase inserted Successfully")
        return redirect('purchase')

    print("Inserted Failed")
    return render_template("purchase.html", data=genericData, form=form)

    print(str(request.form))
    genericData["title"] = "Home"
    genericData["heading"] = "Home"
    #return redirect(url_for("home"), errorMessage="Sale Successfully inserted")
    return render_template("purchase.html", errorMessage="Purchase Successfully inserted", data=genericData)


@app.route('/sales', methods=['GET', 'POST'])
def sales():
    genericData = {
        "title" : "Sales",
        "heading": "Sales"
        }

    form = SalesForm()
    if request.method == "GET":
        return render_template("sales.html", data=genericData, form=form)

    print(str(request.form))
    #return redirect(url_for("home"), errorMessage="Sale Successfully inserted")
    genericData["title"] = "Home"
    genericData["heading"] = "Home"
    return render_template("purchase.html", errorMessage="Sale Successfully inserted", data=genericData)
