from app import app, db
from app.models import Company
from app.forms import LoginForm, RegistrationForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    workers = [
        {'username': 'Игорь'},
        {'username': 'Алексей'}
    ]
    return render_template('index.html', title='Главная', workers=workers)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        company = Company.query.filter_by(email=form.email.data).first()
        if company is None or not company.check_password(form.password.data):
            flash('Неправильные почта или пароль')
            return redirect(url_for('login'))
        login_user(company, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Вход', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Company(company_name=form.company_name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем с регистрацией!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
