from app.models import Company, Doctor
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo


class CompanyLoginForm(FlaskForm):
    email = StringField('Email', validators=[
                        DataRequired('Заполните это поле')])
    password = PasswordField('Пароль', validators=[
                             DataRequired('Заполните это поле')])
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Войти')


class CompanyRegistrationForm(FlaskForm):
    name = StringField('Имя компании', validators=[
                               DataRequired('Заполните это поле')])
    email = StringField('Email', validators=[
                        DataRequired('Заполните это поле'), Email()])
    password = PasswordField('Пароль', validators=[
                             DataRequired('Заполните это поле')])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired('Заполните это поле'), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, email):
        company = Company.query.filter_by(email=email.data).first()
        if company is not None:
            raise ValidationError('Пожалуйста, используйте другую почту')


class DoctorLoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
                           DataRequired('Заполните это поле')])
    password = PasswordField('Пароль', validators=[
                             DataRequired('Заполните это поле')])
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Войти')


class DoctorRegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
                           DataRequired('Заполните это поле')])
    email = StringField('Email', validators=[
                        DataRequired('Заполните это поле'), Email()])
    password = PasswordField('Пароль', validators=[
                             DataRequired('Заполните это поле')])
    password2 = PasswordField('Повторите пароль', validators=[
                              DataRequired('Заполните это поле'), EqualTo('password')])
    submit = SubmitField('Зарегитрироваться')

    def validate_username(self, username):
        doctor = Doctor.query.filter_by(username=username.data).first()
        if doctor is not None:
            raise ValidationError(
                'Пожалуйста, используйте другое имя пользователя')

    def validate_email(self, email):
        doctor = Doctor.query.filter_by(email=email.data).first()
        if doctor is not None:
            raise ValidationError('Пожалуйста, используйте другую почту')
