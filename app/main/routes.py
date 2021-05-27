from app import db
from app.decorators import role_required
from app.main import bp
from app.models import Company, Doctor, Worker
from app.main.forms import AddWorker, EditCompanyForm, EditDoctorForm
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Главная')


@bp.route('/doctor/<username>')
@role_required(role='doctor')
def doctor(username):
    return render_template('doctor.html', title='Страница врача',
                           doctor=Doctor.query.filter_by(id=current_user.id).first())


@bp.route('/company/<username>')
@role_required(role='company')
def company(username):
    return render_template('company.html', title='Страница компании',
                           company=Company.query.filter_by(id=current_user.id).first())


@bp.route('/edit_company', methods=['GET', 'POST'])
@role_required(role='company')
def edit_company():
    company = Company.query.filter_by(id=current_user.id).first()
    form = EditCompanyForm(company.username, company.email)
    if form.validate_on_submit():
        company.username = form.username.data
        company.email = form.email.data
        company.name = form.name.data
        company.about = form.about.data
        db.session.commit()
        flash('Данные сохранены')
        return redirect(url_for('main.edit_company'))
    elif request.method == 'GET':
        form.username.data = company.username
        form.email.data = company.email
        form.name.data = company.name
        form.about.data = company.about
    return render_template('edit_user.html', title='Настройка компании', form=form)


@bp.route('/edit_doctor', methods=['GET', 'POST'])
@role_required(role='doctor')
def edit_doctor():
    doctor = Doctor.query.filter_by(id=current_user.id).first()
    form = EditDoctorForm(doctor.username, doctor.email)
    if form.validate_on_submit():
        doctor.username = form.username.data
        doctor.email = form.email.data
        doctor.first_name = form.first_name.data
        doctor.second_name = form.second_name.data
        db.session.commit()
        flash('Данные сохранены')
        return redirect(url_for('main.edit_doctor'))
    elif request.method == 'GET':
        form.username.data = doctor.username
        form.email.data = doctor.email
        form.first_name.data = doctor.first_name
        form.second_name.data = doctor.second_name
    return render_template('edit_user.html', title='Настройка доктора', form=form)


@bp.route('/workers', methods=['GET', 'POST'])
@role_required(role='company')
def workers():
    form = AddWorker()
    if form.validate_on_submit():
        worker = Worker(first_name=form.first_name.data, middle_name=form.middle_name.data,
                        second_name=form.second_name.data, email=form.email.data, company_id=current_user.id)
        db.session.add(worker)
        db.session.commit()
        flash('Новый сотрудник добавлен')
        return redirect(url_for('main.workers'))
    workers = Worker.query.filter_by(company_id=current_user.id).all()
    return render_template('workers.html', title='Работники', form=form,
                           company=Company.query.filter_by(id=current_user.id).first(), workers=workers)


# @bp.route('/worker/<id>')
# @role_required(role='company')
# def worker_profile():
#     worker = Worker.query
#     return redirect('worker_profile.html', title='Профиль работника', worker=worker)
