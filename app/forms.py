from app.models import User, Company, Doctor
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя или email', validators=[
        DataRequired('Заполните это поле')])
    password = PasswordField('Пароль', validators=[
                             DataRequired('Заполните это поле')])
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Войти')


class CompanyRegistrationForm(FlaskForm):
    username = StringField('Имя пользователя (для входа)', validators=[
                           DataRequired('Заполните это поле')])
    name = StringField('Имя компании')
    email = StringField('Email', validators=[
                        DataRequired('Заполните это поле'), Email()])
    password = PasswordField('Пароль', validators=[
                             DataRequired('Заполните это поле')])
    password2 = PasswordField('Повторите пароль', validators=[
                              DataRequired('Заполните это поле'), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        doctor = Doctor.query.filter_by(username=username.data).first()
        if doctor is not None:
            raise ValidationError(
                'Пожалуйста, используйте другое имя пользователя')

    def validate_email(self, email):
        company = Company.query.filter_by(email=email.data).first()
        if company is not None:
            raise ValidationError('Пожалуйста, используйте другую почту')


class DoctorRegistrationForm(FlaskForm):
    username = StringField('Имя пользователя (для входа)', validators=[
                           DataRequired('Заполните это поле')])
    first_name = StringField('Имя')
    second_name = StringField('Фамилия')
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


class EditCompanyForm(FlaskForm):
    username = StringField('Имя пользователя (для входа)')
    email = StringField('Почта', validators=[Email()])
    name = StringField('Имя компании')
    about = TextAreaField('О компании', validators=[Length(min=0, max=140)])
    submit = SubmitField('Сохранить')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditCompanyForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Это имя пользователя уже занято')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError(
                    'Этот email используется другим аккаунтом')


class EditDoctorForm(FlaskForm):
    username = StringField('Имя пользователя (для входа)')
    email = StringField('Почта', validators=[Email()])
    first_name = StringField('Имя')
    second_name = StringField('Фамилия')
    submit = SubmitField('Сохранить')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditDoctorForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Это имя пользователя уже занято')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError(
                    'Этот email используется другим аккаунтом')
