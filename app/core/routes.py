from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import current_user, login_required

from app.core import bp
from app import db  #, logger
from app.core.forms import PurchaseForm, SalesForm #, PurchaseReportForm, SalesReportForm, PurchaseReportFields
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


@bp.route('/', methods=['GET'])
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

    purchases_report = []
    for _purchase in Purchase.query.order_by(Purchase.created_on.desc()).all():
        form_data = {}
        form_data.update({'id': _purchase.id})
        form_data.update({'agent': _purchase.agent.name})
        form_data.update({'date': _purchase.created_on})
        purchases_report.append(form_data)
        #print("purchase: ", purchase)

    sales_report = []
    for _sale in Sale.query.order_by(Sale.created_on.desc()).all():
        form_data = {}
        form_data.update({'id': _sale.id})
        form_data.update({'agent': _sale.agent.name})
        form_data.update({'date': _sale.created_on})
        sales_report.append(form_data)

    return render_template("core/home.html", data=generic_data, purchases=purchases_report, sales=sales_report)


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

    #purchases = Purchase.query.all()
    purchases_report = []
    for _purchase in Purchase.query.order_by(Purchase.created_on.desc()).all():
        form_data = {}
        form_data.update({'id': _purchase.id})
        form_data.update({'agent': _purchase.agent.name})
        form_data.update({'date': _purchase.created_on})
        form_data.update({'rstnumber': _purchase.rstnumber})
        purchases_report.append(form_data)
        #print("purchase: ", purchase)

    return render_template("core/purchase.html", data=generic_data, form=form, purchases=purchases_report)


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

    sales_report = []
    for _sale in Sale.query.order_by(Sale.created_on.desc()).all():
        form_data = {}
        form_data.update({'id': _sale.id})
        form_data.update({'agent': _sale.agent.name})
        form_data.update({'date': _sale.created_on})
        sales_report.append(form_data)
        #print("sales: ", _sale)

    return render_template("core/sales.html", data=generic_data, form=form, sales=sales_report)


@bp.route('/report/<form_type>', methods=['GET', 'POST'])
@utilities.roles_required([Config.ADMINISTRATOR_STR, Config.USER_STR])
def report(form_type):
    generic_data = {
        "title": "Report",
        "heading": "Report"
    }

    purchases_report = []
    purchases = Purchase.query.all()
    for _purchase in purchases:
        form_data = {}
        form_data.update({'id': _purchase.id})
        form_data.update({'agent': _purchase.agent.name})
        form_data.update({'date': _purchase.timestamp})
        purchases_report.append(form_data)
        print("purchase: ", purchase)
    return render_template("core/report.html", data=generic_data, purchases=purchases_report)


def populate_data(form_type, model_data):
    if form_type == 'purchase':
        return {
            'id': model_data.id,
            'rstnumber': model_data.rstnumber,
            'weight': model_data.weight,
            'moisture': model_data.moisture,
            'rate': model_data.rate,
            'variety': model_data.variety.name,
            'agent': model_data.agent.name,
            'timestamp': model_data.timestamp,
            'amount': model_data.amount
        }
    elif form_type == 'sale':
        print("Riyaz   ", model_data.party_name)
        return {
            'id': model_data.id,
            'party_name': model_data.party_name,
            'party_address': model_data.party_address,
            'gst_number': model_data.gst_number,
            'vehicle_number': model_data.vehicle_number,
            'no_of_bags': model_data.no_of_bags,
            'variety': model_data.variety.name,
            'agent': model_data.agent.name,
            'timestamp': model_data.timestamp,
            'quintol': model_data.quintol,
            'rate': model_data.rate,
            'amount': model_data.amount
        }


@bp.route('/report/<form_type>/detail', methods=['GET'])
def form_detail(form_type):
    generic_data = {
        "title": f"{form_type.capitalize()} Report",
        "heading": f"{form_type.capitalize()} Report"
    }

    id = request.args.get('id')
    print(form_type, id)
    model = {
        'purchase': Purchase,
        'sale': Sale
    }

    model_type = model.get(form_type)
    if model_type is None:
        abort(404)

    model_data = model_type.query.filter_by(id=id).first_or_404()
    form_data = populate_data(form_type, model_data)
    return render_template(f"core/{form_type}_detail.html", data=generic_data, form_data=form_data)

