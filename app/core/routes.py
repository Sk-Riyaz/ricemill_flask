from flask import render_template, request, redirect, url_for, flash, abort, jsonify
from flask_login import current_user, login_required

from app.core import core_bp
from app import db  #, logger
from app.core.forms import PurchaseForm, SalesForm, ReportForm
from app.models import PurchaseAgent, SaleAgent, Purchase, Sale
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
    quintol = form.quintol.data
    rate = form.rate.data
    gst = 5
    amt = (quintol * rate) + (quintol * rate * gst / 100)
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
        amount=amt
    )
    return write_to_db(sale_data)


@core_bp.route('/', methods=['GET'])
@core_bp.route('/home', methods=['GET'])
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

    purchases_data = Purchase.query.order_by(Purchase.created_on.desc()).all()
    sales_data = Sale.query.order_by(Sale.created_on.desc()).all()
    return render_template("core/home.html", data=generic_data, purchases=purchases_data, sales=sales_data)


@core_bp.route('/purchase', methods=['GET', 'POST'])
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

    purchases_data = Purchase.query.order_by(Purchase.created_on.desc()).all()
    return render_template("core/purchase.html", data=generic_data, form=form, purchases=purchases_data)


@core_bp.route('/sales', methods=['GET', 'POST'])
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

    sales_data = Sale.query.order_by(Sale.created_on.desc()).all()
    return render_template("core/sales.html", data=generic_data, form=form, sales=sales_data)


def getModelFor(form_type):
    return {
        'purchase': Purchase,
        'sale': Sale
    }.get(form_type)


@core_bp.route('/report/<form_type>', methods=['GET', 'POST'])
@utilities.roles_required([Config.ADMINISTRATOR_STR, Config.USER_STR])
def report(form_type):
    generic_data = {
        "title": "Report",
        "heading": "Report",
        "form_type": form_type
    }

    model = getModelFor(form_type)
    if model is None:
        abort(404)

    form = ReportForm()
    form.agent.choices = utilities.get_agent_choices(type=eval(f"{form_type.capitalize()}Agent"))
    if form.validate_on_submit():
        model_data = model.query.filter(
            model.created_on.between(
                form.from_date.data, form.to_date.data)
        ).all()
        return render_template("core/report.html", data=generic_data, form=form, purchases=model_data, sales=model_data)
    return render_template("core/report.html", data=generic_data, form=form)


@core_bp.route('/report/<form_type>/detail', methods=['GET'])
def form_detail(form_type):
    generic_data = {
        "title": f"{form_type.capitalize()} Report",
        "heading": f"{form_type.capitalize()} Report"
    }

    id = request.args.get('id')
    model = getModelFor(form_type)
    if model is None:
        abort(404)

    model_data = model.query.filter_by(id=id).first_or_404()
    return render_template(f"core/{form_type}_detail.html", data=generic_data, form_data=model_data)


@core_bp.route('/ajax/get', methods=['GET', 'POST'])
def ajaxGet():
    print("ajaxGet Called")
    return jsonify({'key': 'value', 'key2':'riyaz'})