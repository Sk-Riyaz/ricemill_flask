from flask import redirect, url_for, abort
from flask_login import current_user
from functools import wraps

from app import db
from app.models import Roles, Variety


def roles_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(
                    url_for('core.home',
                            message=("Please login to access the page"))
                )
            urole = current_user.get_role()
            print("ROLES: ", urole, roles)
            if urole is None or urole not in roles:
                return redirect(
                    url_for('core.home',
                            message=("You do not have access to that page."
                                     " Please contact Admin!"))
                )
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


def write_to_db(data, db_action=None):
    if data is None:
        return 500, Exception("Invalid data received")

    try:
        if db_action is not None:
            db_action(data)
        else:
            db.session.add(data)
        db.session.commit()
        return 200, "Success"
    except Exception as e:
        # logger.error(e)
        db.session.rollback()
        return 500, e


def get_select_choice(func):
    def fn(**kwargs):
        select_option = [(0, "Select")]
        select_option.extend(func(**kwargs))
        return select_option
    return fn


def get_variety_choices(**kwargs):
    return [(v.id, v.name) for v in Variety.query.order_by(Variety.name).all()]


def get_agent_choices(**kwargs):
    return [(agent.id, agent.name) for agent in kwargs.get("type").query.order_by(kwargs.get("type").name).all()]


@get_select_choice
def get_report_agent_choices(**kwargs):
    return [(agent.id, agent.name) for agent in kwargs.get("type").query.order_by(kwargs.get("type").name).all()]


@get_select_choice
def get_roles(**kwargs):
    return [(r.id, r.name) for r in Roles.query.order_by(Roles.id).all()]
    return []
