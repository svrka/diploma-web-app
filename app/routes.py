from app import app, db
from app.decorators import role_required
from app.models import Company, Doctor, User
from app.forms import DoctorLoginForm, DoctorRegistrationForm, LoginForm, CompanyRegistrationForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Главная')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data).first()
        if user is None:
            user = User.query.filter_by(
                email=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильно введены данные')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('company' if current_user.role == 'company' else 'doctor',
                                username=current_user.username)
            # next_page = url_for('company', username=current_user.username)
        return redirect(next_page)
    return render_template('login.html', title='Войти', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register-company', methods=['GET', 'POST'])
def register_company():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = CompanyRegistrationForm()
    if form.validate_on_submit():
        company = Company(username=form.username.data, name=form.name.data,
                          email=form.email.data, role='company')
        company.set_password(form.password.data)
        db.session.add(company)
        db.session.commit()
        flash('Поздравляем с регистрацией!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация компании', form=form)


@app.route('/register-doctor', methods=['GET', 'POST'])
def register_doctor():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = DoctorRegistrationForm()
    if form.validate_on_submit():
        doctor = Doctor(username=form.username.data, email=form.email.data,
                        first_name=form.first_name.data, second_name=form.second_name.data,
                        role='doctor')
        doctor.set_password(form.password.data)
        db.session.add(doctor)
        db.session.commit()
        flash('Поздравляем с регистрацией!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация доктора', form=form)


@app.route('/doctor/<username>')
@role_required(role='doctor')
def doctor(username):
    return render_template('doctor.html', title='Страница врача',
                           doctor=Doctor.query.filter_by(id=current_user.id).first())


@app.route('/company/<username>')
@role_required(role='company')
def company(username):
    return render_template('company.html', title='Страница компании',
                           company=Company.query.filter_by(id=current_user.id).first())
