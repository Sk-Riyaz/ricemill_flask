from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
#from flask_user import roles_required
from werkzeug.urls import url_parse

from functools import wraps

from app import app, db
from app.forms import LoginForm, RegistrationForm, AgentForm, PurchaseForm, SalesForm, VarietyForm
from app.models import User, PurchaseAgent, SaleAgent, Variety, Roles, Purchase, Sale
from app import constants, utilities


def roles_required(roles):
    def wrapper(fn):
        print("c:1", roles)

        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return app.login_manager.unauthorized()
            urole = current_user.get_role()
            print("c:2", roles, urole)
            if urole is None or urole not in roles:
                return app.login_manager.unauthorized()
            print("c:3", roles, urole)
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("User already loggedin")
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        # flash('Login requested for user {}, remember_me={}'.format(
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


def write_to_db(data):
    try:
        db.session.add(data)
        db.session.commit()
        return 200, "Success"
    except Exception as e:
        app.logger.error(e)
        db.session.rollback()
        return 500, e


def userFormHandler(form):
    role = Roles.query.filter_by(id=form.roles.data).first()
    user = User(username=form.username.data,
                email=form.email.data, role_id=role.id)
    user.set_password(form.password.data)
    print(user)
    return write_to_db(user)


def agentFormHandler(form):
    agentTypeModel = {
        "1": PurchaseAgent,
        "2": SaleAgent
    }
    app.logger.info("data is coming")
    curModel = agentTypeModel.get(form.agent_type.data)
    if curModel is None:
        abort(500)

    agent = curModel(
        name=form.name.data,
        email=form.email.data,
        mobile=form.mobile.data,
        address=form.address.data
    )
    return write_to_db(agent)


def varietyFormHandler(form):
    variety = Variety(name=form.name.data)
    return write_to_db(variety)


def purchaseFormHandler(form):
    purchase = Purchase(
        rstnumber=form.rst_number.data,
        weight=form.weight.data,
        moisture=form.moisture.data,
        rate=form.rate.data,
        variety_id=form.variety.data,
        agent_id=form.agent.data,
        timestamp=form.date.data,
        amount=form.amount.data
    )
    return write_to_db(purchase)


def saleFormHandler(form):
    sale = Sale(
        party_name=form.party_name.data,
        party_address=form.party_address.data,
        gst_number=form.gst_number.data,
        vehicle_number=form.vehicle_number.data,
        no_of_bags=form.no_of_bags.data,
        variety_id=form.variety.data,
        agent_id=form.agent.data,
        quintol=form.quintol.data,
        rate=form.rate.data,
        timestamp=form.date.data,
        amount=form.amount.data
    )
    return write_to_db(sale)


def handleForm(form, utype):
    if form is None:
        abort(500)

    handler = getFormHandler(utype)
    if handler is None:
        abort(500)
    return handler(form)


def getFormHandler(formType):
    modelDict = {
        'user': userFormHandler,
        'agent': agentFormHandler,
        'variety': varietyFormHandler
    }
    return modelDict.get(formType)


@app.route('/add/<utype>', methods=['GET', 'POST'])
@login_required
@roles_required([constants.SUPER_USER_STR, constants.ADMINISTRATOR_STR])
def register(utype):
    genericData = {
        "title": f"Add {str.capitalize(utype)}",
        "heading": f"Add {str.capitalize(utype)}"
    }
    formDict = {
        'user': RegistrationForm,
        'agent': AgentForm,
        'variety': VarietyForm
    }
    form = formDict.get(utype)
    if form is None:
        abort(404)

    form = form()
    if form.validate_on_submit():
        status, e = handleForm(form, utype)
        # app.logger.info("status: ", status, e)
        if status != 200:
            abort(status)
        flash(f"{utype} inserted successfully")
        app.logger.info(f"{utype} inserted successfully")
        return redirect(utype)
    return render_template(f"add_{utype}.html", form=form, data=genericData)


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
    form.agent.choices = utilities.getAgentChoices(type=PurchaseAgent)
    form.variety.choices = utilities.getVarietyChoices()
    if form.validate_on_submit():
        status, e = purchaseFormHandler(form)
        if status != 200:
            abort(status)
        flash("Purchase inserted Successfully")
        app.logger.info("Purchase inserted Successfully")
        return redirect('purchase')

    return render_template("purchase.html", data=genericData, form=form)


@app.route('/sales', methods=['GET', 'POST'])
def sales():
    genericData = {
        "title" : "Sales",
        "heading": "Sales"
        }

    form = SalesForm()
    form.agent.choices = utilities.getAgentChoices(type=SaleAgent)
    form.variety.choices = utilities.getVarietyChoices()
    if form.validate_on_submit():
        status, e = saleFormHandler(form)
        if status != 200:
            abort(status)
        app.logger.info("Sale inserted Successfully")
        flash("Sale inserted Successfully")
        return redirect('sales')

    return render_template("sales.html", data=genericData, form=form)

