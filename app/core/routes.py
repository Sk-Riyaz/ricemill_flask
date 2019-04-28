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
from app.utilities import write_to_db
from config import Config


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


@bp.route('/home', methods=['GET'])
@login_required
def home():
    generic_data = {
        "title": "Home",
        "heading": "Home"
    }
    print(current_user.id)
    message = request.args.get('message')
    if message is not None:
        flash(message)
    return render_template("core/home.html", data=generic_data)


@bp.route('/purchase', methods=['GET', 'POST'])
@utilities.roles_required([Config.ADMINISTRATOR_STR])
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

    return render_template("core/purchase.html", data=generic_data, form=form)


@bp.route('/sales', methods=['GET', 'POST'])
@utilities.roles_required([Config.ADMINISTRATOR_STR])
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

    return render_template("core/sales.html", data=generic_data, form=form)
