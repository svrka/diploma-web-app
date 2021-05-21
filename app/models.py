from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Company(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    workers = db.relationship('Worker', backref='company', lazy='dynamic')

    def __repr__(self):
        return '<Компания {}>'.format(self.company_name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    worker_surname = db.Column(db.String(64), index=True)
    worker_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    def __repr__(self):
        return '<Работник {} {}'.format(self.worker_surname, self.worker_name)


@login.user_loader
def load_user(id):
    return Company.query.get(int(id))
