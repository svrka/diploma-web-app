from sqlalchemy.orm import backref
from app import db, login
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
import jwt
from time import time
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=[
                            'HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Company(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(64), index=True)
    about = db.Column(db.String(140))
    workers = db.relationship('Worker', backref='company', lazy='dynamic')
    examinations = db.relationship(
        'Examination', backref='company', lazy='dynamic')
    doctor = db.relationship('Doctor', uselist=False,
                             primaryjoin="Company.id == Doctor.company_id")

    def __repr__(self):
        return 'Компания {}'.format(self.name)


class Doctor(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    second_name = db.Column(db.String(64), index=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    def __repr__(self) -> str:
        return 'Доктор {} {}'.format(self.first_name, self.second_name)

    def get_registration_token(self, expires_in=600):
        return jwt.encode(
            {'register_doctor': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256'
        )

    @staticmethod
    def verify_registration_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=[
                            'HS256'])['register_doctor']
        except:
            return
        return Doctor.query.get(id)


class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    second_name = db.Column(db.String(64), index=True)
    middle_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True)

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    examinations = db.relationship(
        'Examination', backref='worker', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.second_name)


class Examination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_pressure = db.Column(db.String(10))
    alcohol_level = db.Column(db.String(10))
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'))

    def __repr__(self):
        return 'Дата: {}, Давление: {}, Алкоголь: {}'.format(self.datetime, self.blood_pressure, self.alcohol_level)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
