from app import db
from app.auth import bp
from app.models import User, Company, Doctor
from app.auth.email import send_password_reset_email
from app.auth.forms import LoginForm, DoctorRegistrationForm, CompanyRegistrationForm, ResetPasswordForm, ResetPasswordRequestForm
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


@bp.route('/register_doctor', methods=['GET', 'POST'])
def register_doctor():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = DoctorRegistrationForm()
    if form.validate_on_submit():
        doctor = Doctor(username=form.username.data, email=form.email.data,
                        first_name=form.first_name.data, second_name=form.second_name.data,
                        role='doctor')
        doctor.set_password(form.password.data)
        db.session.add(doctor)
        db.session.commit()
        flash('Поздравляем с регистрацией!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Регистрация доктора', form=form)


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
