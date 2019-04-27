from app import db
from app.models import Roles, Variety


def get_select_choice(func):
    def fn(**kwargs):
        select_option = [(0, "Select")]
        select_option.extend(func(**kwargs))
        return select_option
    return fn


@get_select_choice
def get_variety_choices(**kwargs):
    return [(v.id, v.name) for v in db.session.query(Variety).all()]
    return []


@get_select_choice
def get_agent_choices(**kwargs):
    return [(agent.id, agent.name) for agent in kwargs.get("type")().query.all()]
    return []


@get_select_choice
def get_roles(**kwargs):
    return [(r.id, r.name) for r in Roles.query.all()]
    return []
