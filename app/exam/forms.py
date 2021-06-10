from app.models import User, Worker
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, Email, Optional


class SearchWorkerForm(FlaskForm):
    search = StringField('Фамилия')
    submit = SubmitField('Поиск')

    def validate_search(self, search):
        worker = Worker.query.filter_by(
            company_id=current_user.id, second_name=search.data).first()
        if worker is None:
            raise ValidationError('Такой работник не найден')


class ExaminationForm(FlaskForm):
    blood_pressure = StringField('Давление', validators=[
                                 DataRequired('Это поле должно быть заполнено')])
    alcohol_level = StringField('Уровень алкоголя', validators=[
                                DataRequired('Это поле должно быть заполнено')])
    worker_id = StringField('Номер работника', validators=[
                            DataRequired('Это поле должно быть заполнено')])
    submit = SubmitField('Отправить')
