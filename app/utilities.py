from app import db
from app.models import Roles, Variety


def getSelectChoice(func):
    def fn(**kwargs):
        selectOption = [(0, "Select")]
        selectOption.extend(func(**kwargs))
        return selectOption
    return fn


@getSelectChoice
def getVarietyChoices(**kwargs):
    return [(v.id, v.name) for v in db.session.query(Variety).all()]
    return []


@getSelectChoice
def getAgentChoices(**kwargs):
    return [(agent.id, agent.name) for agent in kwargs.get("type")().query.all()]
    return []


@getSelectChoice
def getRoles(**kwargs):
    return [(r.id, r.name) for r in Roles.query.all()]
    return []
