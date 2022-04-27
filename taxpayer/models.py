from taxpayer import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Accountant.query.get(int(user_id))

class Accountant(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(120), default=datetime.utcnow)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    firstName = db.Column(db.String(120), nullable=False)
    lastName = db.Column(db.String(120), nullable=False)
    phoneNumber = db.Column(db.String(120), nullable=False)
    myclient = db.relationship('TaxPayer', backref='accountant', lazy=True)

    def __repr__(self):
        return f'{self.username}, {self.firstName} {self.lastName}'


class TaxPayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    firstName = db.Column(db.String(120), nullable=False)
    lastName = db.Column(db.String(120), nullable=False)
    phoneNumber = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    stateTax = db.Column(db.Integer, nullable=False, default=0)
    fines = db.Column(db.Integer, nullable=False, default=0)
    arrears = db.Column(db.Integer, nullable=False, default=0)
    yearsOwned = db.Column(db.Integer, nullable=False, default=0)
    datePaid = db.Column(db.DateTime(120), nullable=False, default=datetime.utcnow)
    salary = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(120), nullable=False, default='Paid')
    user_id = db.Column(db.Integer, db.ForeignKey('accountant.id'), nullable=False)

    #def __repr__(self):
     #   return f'{self.email}, {self.firstName} {self.lastName}, {self.state}'