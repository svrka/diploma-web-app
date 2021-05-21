from app.models import Company
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Заполните это поле')])
    # username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired('Заполните это поле')])
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    company_name = StringField('Имя компании', validators=[DataRequired('Заполните это поле')])
    # username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired('Заполните это поле'), Email()])
    password = PasswordField('Пароль', validators=[DataRequired('Заполните это поле')])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired('Заполните это поле'), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    # def validate_username(self, username):
    #     user = Company.query.filter_by(company_name=username.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = Company.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другой Email')
