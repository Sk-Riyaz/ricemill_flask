from flask import render_template, redirect, url_for, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
#from flask_user import roles_required
from werkzeug.urls import url_parse

from app.admin import bp
from app import db  # logger, login_manager, db
from app.admin.forms import RegistrationForm, AgentForm, VarietyForm
from app.models import User, PurchaseAgent, SaleAgent, Variety, Roles
from config import Config
from app import utilities
from app.utilities import write_to_db


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
    # logger.info("data is coming")
    cur_model = agent_type_2_model.get(form.agent_type.data)
    if cur_model is None:
        abort(500)

    agent = cur_model(
        name=form.name.data,
        email=form.email.data,
        mobile=form.mobile.data,
        address=form.address.data
    )
    return write_to_db(agent, db.session.add)


def variety_form_handler(form, action):
    variety = Variety(name=form.name.data)
    return write_to_db(variety, db.session.add)


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


@bp.route('/add/<form_type>', methods=['GET', 'POST'])
@login_required
@utilities.roles_required([Config.SUPER_USER_STR])
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
    print(Roles.query.all())
    if form_type == 'user':
        form.roles.choices = utilities.get_roles()
    if form.validate_on_submit():
        status, e = handle_form(form, form_type, 'add')
        # logger.info("status: ", status, e)
        if status != 200:
            # logger.error(f"status: {status}, {e}")
            abort(status)
        flash(f"{form_type} inserted successfully")
        # logger.info(f"{form_type} inserted successfully")
        return redirect(form_type)
    return render_template(f"admin/add_{form_type}.html", form=form,
                           data=generic_data)


@bp.route('/admin/<action>/<form_type>', methods=['GET', 'POST'])
@login_required
@utilities.roles_required([Config.SUPER_USER_STR])
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
        # logger.info("status: ", status, e)
        if status != 200:
            # logger.error(f"status: {status}, {e}")
            abort(status)
        flash(f"{form_type} {action}ed successfully")
        # logger.info(f"{form_type} {action}ed successfully")
        return redirect(form_type)
    return render_template(f"{action}_{form_type}.html", form=form,
                           data=generic_data)
