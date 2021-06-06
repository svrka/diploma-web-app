from app.decorators import role_required
from app import db
from app.auth import bp
from app.models import User, Company, Doctor
from app.auth.email import send_doctor_registration_email, send_password_reset_email
from app.auth.forms import LoginForm, DoctorRegistrationForm, CompanyRegistrationForm, RegisterDoctorForm, ResetPasswordForm, ResetPasswordRequestForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data).first()
        if user is None:
            user = User.query.filter_by(
                email=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильно введены данные')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.company' if current_user.role == 'company' else 'main.doctor',
                                username=current_user.username)
        return redirect(next_page)
    return render_template('auth/login.html', title='Войти', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/register_company', methods=['GET', 'POST'])
def register_company():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = CompanyRegistrationForm()
    if form.validate_on_submit():
        company = Company(username=form.username.data, name=form.name.data,
                          email=form.email.data, role='company')
        company.set_password(form.password.data)
        db.session.add(company)
        db.session.commit()
        flash('Поздравляем с регистрацией!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Регистрация компании', form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Письмо с информацией о смене пароля отправлено на почту')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Смена пароля', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Ваш пароль был изменен')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@bp.route('/register_doctor', methods=['GET', 'POST'])
@role_required(role='company')
def register_doctor():
    company = Company.query.filter_by(id=current_user.id).first()
    if company.doctor:
        return redirect(url_for('main.company', username=current_user.username))
    form = RegisterDoctorForm()
    if form.validate_on_submit():
        doctor = Doctor(email=form.email.data,
                        company_id=current_user.id, role='doctor')
        db.session.add(doctor)
        db.session.commit()
        send_doctor_registration_email(doctor, company)
        flash('Письмо отправлено на почту доктору')
        return redirect(url_for('main.company', username=current_user.username))
    return render_template('auth/register_doctor.html', title='Зарегистрировать доктора', form=form)


@bp.route('/doctor_registration/<token>', methods=['GET', 'POST'])
def doctor_registration(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    doctor = Doctor.verify_registration_token(token)
    if not doctor:
        return redirect(url_for('main.index'))
    form = DoctorRegistrationForm(doctor.email)
    if form.validate_on_submit():
        doctor.username = form.username.data
        doctor.email = form.email.data
        doctor.first_name = form.first_name.data
        doctor.second_name = form.second_name.data
        # doctor.role = 'doctor'
        doctor.set_password(form.password.data)
        db.session.commit()
        flash('Поздравляем с регистрацией!')
        return redirect(url_for('auth.login'))
    elif request.method == 'GET':
        form.email.data = doctor.email
    return render_template('auth/register.html', title='Регистрация доктора', form=form)
