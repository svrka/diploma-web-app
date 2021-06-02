from app.email import send_email
from flask import render_template, current_app


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('Смена пароля',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))


def send_doctor_registration_email(doctor, company):
    token = doctor.get_registration_token()
    send_email('Регистрация врача', sender=current_app.config['ADMINS'][0],
               recipients=[doctor.email],
               text_body=render_template('email/register_doctor.txt',
                                         company=company, doctor=doctor, token=token),
               html_body=render_template('email/register_doctor.html',
                                         company=company, doctor=doctor, token=token))
