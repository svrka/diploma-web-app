from sqlalchemy.orm import backref
from app import db, login
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
import json
import jwt
from time import time
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)
    last_message_read_time = db.Column(db.DateTime)

    messages_sent = db.relationship(
        'Message', foreign_keys='Message.sender_id', backref='author', lazy='dynamic')
    messages_received = db.relationship(
        'Message', foreign_keys='Message.recipient_id', backref='recipient', lazy='dynamic')
    notifications = db.relationship(
        'Notification', backref='user', lazy='dynamic')

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

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(Message.timestamp > last_read_time).count()

    def add_notification(self, name, data, author, body):
        n = Notification(name=name, payload_json=json.dumps(
            data), user=self, author=author, body=body)
        db.session.add(n)
        return n


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
    messages = db.relationship(
        'Message', backref='examination', lazy='dynamic')

    def __repr__(self):
        return 'Дата: {}, Давление: {}, Алкоголь: {}'.format(self.datetime, self.blood_pressure, self.alcohol_level)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'))
    exam_id = db.Column(db.Integer, db.ForeignKey('examination.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self) -> str:
        return '{}: {}'.format(self.author.role, self.body)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    author = db.Column(db.String(24), index=True)
    body = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
