from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, Email, Optional


class EditCompanyForm(FlaskForm):
    username = StringField('Имя пользователя (для входа)', validators=[
                           DataRequired('Заполните это поле')])
    email = StringField('Почта', validators=[
                        Email(), DataRequired('Заполните это поле')])
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
    username = StringField('Имя пользователя (для входа)', validators=[
                           DataRequired('Заполните это поле')])
    email = StringField('Почта', validators=[
                        Email(), DataRequired('Заполните это поле')])
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


class AddWorker(FlaskForm):
    first_name = StringField('Имя')
    second_name = StringField('Фамилия')
    middle_name = StringField('Отчество')
    email = StringField('Почта', validators=[Optional(), Email()])
    submit = SubmitField('Добавить')
