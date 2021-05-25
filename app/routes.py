from app import app, db
from app.decorators import role_required
from app.models import Company, Doctor
from app.forms import DoctorLoginForm, DoctorRegistrationForm, CompanyLoginForm, CompanyRegistrationForm
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
    company_form = CompanyLoginForm()
    if company_form.validate_on_submit():
        company = Company.query.filter_by(
            username=company_form.email.data).first()
        if company is None:
            company = Company.query.filter_by(
                email=company_form.email.data).first()
        if company is None or not company.check_password(company_form.password.data):
            flash('Неправильно введены данные')
            return redirect(url_for('login'))
        login_user(company, remember=company_form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('company')
        return redirect(next_page)
    doctor_form = DoctorLoginForm()
    if doctor_form.validate_on_submit():
        doctor = Doctor.query.filter_by(
            username=doctor_form.username.data).first()
        if doctor is None:
            doctor = Doctor.query.filter_by(
                email=doctor_form.username.data).first()
        if doctor is None or not doctor.check_password(doctor_form.password.data):
            flash('Неправильно введены данные')
            return redirect(url_for('login'))
        login_user(doctor, remember=doctor_form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('doctor', username=current_user.username)
        return redirect(next_page)
    return render_template('login.html', title='Войти, как компания', form=company_form,
                           title2='Войти, как врач', form2=doctor_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    company_form = CompanyRegistrationForm()
    if company_form.validate_on_submit():
        company = Company(username=company_form.username.data, name=company_form.name.data,
                          email=company_form.email.data, role='company')
        company.set_password(company_form.password.data)
        db.session.add(company)
        db.session.commit()
        flash('Поздравляем с регистрацией!')
        return redirect(url_for('login'))
    doctor_form = DoctorRegistrationForm()
    if doctor_form.validate_on_submit():
        doctor = Doctor(username=doctor_form.username.data, email=doctor_form.email.data,
                        first_name=doctor_form.first_name.data, second_name=doctor_form.second_name.data,
                        role='doctor')
        doctor.set_password(doctor_form.password.data)
        db.session.add(doctor)
        db.session.commit()
        flash('Поздравляем с регистрацией!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация компании',
                           form=company_form, title2='Регистрация доктора', form2=doctor_form)


@app.route('/doctor/<username>')
@role_required(role='doctor')
def doctor(username):
    return render_template('doctor.html', title='Страница врача',
                           doctor=Doctor.query.filter_by(id=current_user.id).first())


@app.route('/company')
@role_required(role='company')
def company():
    return render_template('company.html', title='Страница компании',
                           company=Company.query.filter_by(id=current_user.id).first())
