from app import db
from app import login

from sqlalchemy.sql.schema import UniqueConstraint
from flask_login import UserMixin
#from flask_user import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import constants


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class BaseModel(db.Model):
    __abstract__ = True
    created_on = db.Column(
        db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    updated_on = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())


class User(UserMixin, BaseModel):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean, default=False, nullable=False)
    # Need to delete after confirmation. Basically not needed.
    #roles = db.relationship('Roles', uselist=False, secondary='user_roles')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Roles', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    """
    def set_role(self):
        self.roles = [r.name for r in self.roles]
    """

    def get_role(self):
        return self.role.name

    def is_admin(self):
        return self.get_role() in [constants.SUPER_USER_STR, constants.ADMINISTRATOR_STR]

    def __repr__(self):
        return f'<User Id: {self.id} Name: {self.username} Role: {self.get_role()}>'


# Define the Role data-model
class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f'<Role Id: {self.id} Name: {self.name}>'

# Define the UserRoles association table
"""
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
"""


class PurchaseAgent(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    email = db.Column(db.String(120))
    mobile = db.Column(db.String(15), index=True, nullable=False)
    address = db.Column(db.String(200))
    purchases = db.relationship('Purchase', backref='agent', lazy='dynamic')
    __table_args__ = (UniqueConstraint(
        'name', 'mobile', name='_name_mobile_uc'),)

    def __repr__(self):
        return f'<Agent Id: {self.id} Name: {self.name} Phone: {self.mobile}>'


class SaleAgent(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    email = db.Column(db.String(120))
    mobile = db.Column(db.String(15), index=True, nullable=False)
    address = db.Column(db.String(200))
    sales = db.relationship('Sale', backref='agent', lazy='dynamic')
    __table_args__ = (UniqueConstraint(
        'name', 'mobile', name='_name_mobile_uc'),)

    def __repr__(self):
        return f'<Agent Id: {self.id} Name: {self.name} Phone: {self.mobile}>'


class Variety(db.Model):
    __tablename__ = "varieties"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return f'<Variety Id: {self.id} Name: {self.name}>'


class Purchase(BaseModel):
    __tablename__ = "purchases"
    id = db.Column(db.Integer, primary_key=True)
    rstnumber = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    moisture = db.Column(db.Float, nullable=False)
    rate = db.Column(db.Float, nullable=False)
    variety_id = db.Column(
        db.String(64), db.ForeignKey('varieties.id'), nullable=False)
    agent_id = db.Column(
        db.Integer, db.ForeignKey('purchase_agent.id'), nullable=False)
    timestamp = db.Column(
        db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Puchase Id: {self.id} rstnumber: {self.rstnumber} Agent: {self.agent_id} Time: {self.timestamp}>'


class Sale(BaseModel):
    __tablename__ = "sales"
    id = db.Column(db.Integer, primary_key=True)
    party_name = db.Column(db.String(128), nullable=False)
    party_address = db.Column(db.String(200), nullable=False)
    gst_number = db.Column(db.String(32), nullable=False)
    vehicle_number = db.Column(db.String(32), nullable=False)
    no_of_bags = db.Column(db.Integer, nullable=False)
    variety_id = db.Column(
        db.String(64), db.ForeignKey('varieties.id'), nullable=False)
    agent_id = db.Column(
        db.Integer, db.ForeignKey('sale_agent.id'), nullable=False)
    quintol = db.Column(db.Float, nullable=False)
    rate = db.Column(db.Float, nullable=False)
    timestamp = db.Column(
        db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Sale Id: {self.id} PartyName: {self.party_name} Agent: {self.agent_id} Time: {self.timestamp} VehicleNumber: {self.vehicle_number}>'

