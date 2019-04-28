from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
#from flask_user import roles_required
from werkzeug.urls import url_parse

from functools import wraps

from app.core import bp
from app import db#, logger
#from app.auth import LoginForm, RegistrationForm, ChangePasswordForm, AgentForm, PurchaseForm, SalesForm, VarietyForm
from app.core.forms import PurchaseForm, SalesForm
from app.models import User, PurchaseAgent, SaleAgent, Variety, Roles, Purchase, Sale
from app import utilities
from config import Config


def roles_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                #return login_manager.unauthorized()
                return False
            urole = current_user.get_role()
            if urole is None or urole not in roles:
                #return login_manager.unauthorized()
                return False
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
        #logger.error(e)
        db.session.rollback()
        return 500, e

"""
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
    #logger.info("data is coming")
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
"""

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

"""
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
"""


@bp.route('/home')
@login_required
def home():
    generic_data = {
        "title": "Home",
        "heading": "Home"
    }
    print(current_user.id)
    return render_template("home.html", data=generic_data)


@bp.route('/purchase', methods=['GET', 'POST'])
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
        #logger.info("Purchase inserted Successfully")
        return redirect(url_for('core.purchase'))

    return render_template("purchase.html", data=generic_data, form=form)


@bp.route('/sales', methods=['GET', 'POST'])
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
        #logger.info("Sale inserted Successfully")
        flash("Sale inserted Successfully")
        return redirect(url_for('core.sales'))

    return render_template("sales.html", data=generic_data, form=form)
