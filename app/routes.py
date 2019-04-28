from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
#from flask_user import roles_required
from werkzeug.urls import url_parse

from functools import wraps

from app import app, db
from app.forms import LoginForm, RegistrationForm, ChangePasswordForm, AgentForm, PurchaseForm, SalesForm, VarietyForm
from app.models import User, PurchaseAgent, SaleAgent, Variety, Roles, Purchase, Sale
from app import utilities
from config import Config


def roles_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return app.login_manager.unauthorized()
            urole = current_user.get_role()
            if urole is None or urole not in roles:
                return app.login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


def write_to_db(data, db_action):
    try:
        if db_action is not None:
            db_action(data)
        else:
            db.session.add(data)
        db.session.commit()
        return 200, "Success"
    except Exception as e:
        app.logger.error(e)
        db.session.rollback()
        return 500, e


def user_form_handler(form, action):
    if action == "add":
        user = User(username=form.username.data,
                    email=form.email.data,
                    role_id=form.roles.data)
        user.set_password(form.password.data)
        return write_to_db(user, db.session.add)
    elif action == "delete":
        user = User.query.filter_by(form.id.data).first()
        if user is None:
            abort(404)
        return write_to_db(user, db.session.delete)
    elif action == "update":
        user = User(email=form.email.data,
                    role_id=form.roles.data,
                    active=form.active.data)
        return write_to_db(user, db.session.add)
    return 500, Exception(f"Invalid action: {action}")


def agent_form_handler(form, action):
    agent_type_2_model = {
        "1": PurchaseAgent,
        "2": SaleAgent
    }
    app.logger.info("data is coming")
    cur_model = agent_type_2_model.get(form.agent_type.data)
    if cur_model is None:
        abort(500)

    agent = cur_model(
        name=form.name.data,
        email=form.email.data,
        mobile=form.mobile.data,
        address=form.address.data
    )
    return write_to_db(agent)


def variety_form_handler(form, action):
    variety = Variety(name=form.name.data)
    return write_to_db(variety)


def purchase_form_handler(form):
    purchase_data = Purchase(
        rstnumber=form.rst_number.data,
        weight=form.weight.data,
        moisture=form.moisture.data,
        rate=form.rate.data,
        variety_id=form.variety.data,
        agent_id=form.agent.data,
        timestamp=form.date.data,
        amount=form.amount.data
    )
    return write_to_db(purchase_data)


def sale_form_handler(form):
    sale_data = Sale(
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
    return write_to_db(sale_data)


def handle_form(form, form_type, action):
    if form is None or action is None:
        abort(500)

    handler = get_form_handler(form_type)
    if handler is None:
        abort(500)
    return handler(form, action)


def get_form_handler(form_type):
    form_2_handler = {
        'user': user_form_handler,
        'agent': agent_form_handler,
        'variety': variety_form_handler
    }
    return form_2_handler.get(form_type)


def is_form_support_action(form_type, action):
    form_type_2_actions = {
        'user': ['add', 'delete', 'update'],
        'agent': ['add', 'delete', 'update'],
        'variety': ['add', 'delete']
    }
    return form_type_2_actions.get(form_type) is not None and \
           action in form_type_2_actions.get(form_type)


def get_form_for_type(form_type):
    form_dict = {
        'user': RegistrationForm,
        'agent': AgentForm,
        'variety': VarietyForm
    }
    form = form_dict.get(form_type)
    if form is None:
        abort(404)
    return form


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


@app.route('/add/<form_type>', methods=['GET', 'POST'])
@login_required
@roles_required([Config.SUPER_USER_STR, Config.ADMINISTRATOR_STR])
def register(form_type):
    generic_data = {
        "title": f"Add {str.capitalize(form_type)}",
        "heading": f"Add {str.capitalize(form_type)}"
    }
    form_dict = {
        'user': RegistrationForm,
        'agent': AgentForm,
        'variety': VarietyForm
    }
    form = form_dict.get(form_type)
    if form is None:
        abort(404)

    form = form()
    if form.validate_on_submit():
        status, e = handle_form(form, form_type, 'add')
        # app.logger.info("status: ", status, e)
        if status != 200:
            app.logger.error(f"status: {status}, {e}")
            abort(status)
        flash(f"{form_type} inserted successfully")
        app.logger.info(f"{form_type} inserted successfully")
        return redirect(form_type)
    return render_template(f"add_{form_type}.html", form=form, data=generic_data)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    generic_data = {
        "title": "Change Password",
        "heading": "Change Password"
    }
    form = ChangePasswordForm()
    if form.validate_on_submit():
        print()
        pass
    return render_template(f"change_password.html", form=form, data=generic_data)


@app.route('/admin/<action>/<form_type>', methods=['GET', 'POST'])
@login_required
@roles_required([Config.SUPER_USER_STR, Config.ADMINISTRATOR_STR])
def admin_actions(action, form_type):
    generic_data = {
        "title": f"{str.capitalize(action)} {str.capitalize(form_type)}",
        "heading": f"{str.capitalize(action)} {str.capitalize(form_type)}"
    }

    if not is_form_support_action(form_type, action):
        abort(404)

    form = get_form_for_type(form_type)()
    if form.validate_on_submit():
        status, e = handle_form(form, form_type, action)
        # app.logger.info("status: ", status, e)
        if status != 200:
            app.logger.error(f"status: {status}, {e}")
            abort(status)
        flash(f"{form_type} {action}ed successfully")
        app.logger.info(f"{form_type} {action}ed successfully")
        return redirect(form_type)
    return render_template(f"{action}_{form_type}.html", form=form, data=generic_data)


@app.route('/home')
@login_required
def home():
    generic_data = {
        "title": "Home",
        "heading": "Home"
    }
    print(current_user.id)
    return render_template("home.html", data=generic_data)


@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    generic_data = {
        "title": "Purchase",
        "heading": "Purchase"
    }

    form = PurchaseForm()
    form.agent.choices = utilities.get_agent_choices(type=PurchaseAgent)
    form.variety.choices = utilities.get_variety_choices()
    if form.validate_on_submit():
        status, e = purchase_form_handler(form)
        if status != 200:
            abort(status)
        flash("Purchase inserted Successfully")
        app.logger.info("Purchase inserted Successfully")
        return redirect('purchase')

    return render_template("purchase.html", data=generic_data, form=form)


@app.route('/sales', methods=['GET', 'POST'])
def sales():
    generic_data = {
        "title": "Sales",
        "heading": "Sales"
        }

    form = SalesForm()
    form.agent.choices = utilities.get_agent_choices(type=SaleAgent)
    form.variety.choices = utilities.get_variety_choices()
    if form.validate_on_submit():
        status, e = sale_form_handler(form)
        if status != 200:
            abort(status)
        app.logger.info("Sale inserted Successfully")
        flash("Sale inserted Successfully")
        return redirect('sales')

    return render_template("sales.html", data=generic_data, form=form)

@app.route('/manage', methods=['GET', 'POST'])
def manage():
    generic_data = {
        "title": "Sales",
        "heading": "Sales"
        }
    """
    form = SalesForm()
    form.agent.choices = utilities.get_agent_choices(type=SaleAgent)
    form.variety.choices = utilities.get_variety_choices()
    if form.validate_on_submit():
        status, e = sale_form_handler(form)
        if status != 200:
            abort(status)
        app.logger.info("Sale inserted Successfully")
        flash("Sale inserted Successfully")
        return redirect('sales')
    """
    return render_template("manage.html", data=generic_data, uform=RegistrationForm(), aform=AgentForm(), vform=VarietyForm())
