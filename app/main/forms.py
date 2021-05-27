from app.models import User, Worker
from flask_wtf import FlaskForm
from flask_login import current_user
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


class AddWorkerForm(FlaskForm):
    first_name = StringField('Имя')
    second_name = StringField('Фамилия')
    middle_name = StringField('Отчество')
    email = StringField('Почта', validators=[Optional(), Email()])
    submit = SubmitField('Добавить')


class EditWorkerForm(FlaskForm):
    first_name = StringField('Имя')
    second_name = StringField('Фамилия')
    middle_name = StringField('Отчество')
    email = StringField('Почта', validators=[Optional(), Email()])
    submit = SubmitField('Сохранить')


class SearchWorkerForm(FlaskForm):
    search = StringField('Фамилия')
    submit = SubmitField('Поиск')

    def validate_search(self, search):
        worker = Worker.query.filter_by(company_id=current_user.id, second_name=search.data).first()
        if worker is None:
            raise ValidationError('Такой работник не найден')

class ExaminationForm(FlaskForm):
    blood_pressure = StringField('Давление')
    alcohol_level = StringField('Уровень алкоголя')
    worker_id = StringField('Номер работника', validators=[])
    submit = SubmitField('Отправить')