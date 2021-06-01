from app import db
from app.decorators import exam_in_company, worker_in_company, role_required, user_required
from app.main import bp
from app.models import Company, Doctor, Examination, Worker
from app.main.forms import AddWorkerForm, EditCompanyForm, EditDoctorForm, EditWorkerForm, ExaminationForm, SearchWorkerForm
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Главная')


@bp.route('/doctor/<username>')
@user_required
def doctor(username):
    return render_template('doctor.html', title='Страница врача',
                           doctor=Doctor.query.filter_by(id=current_user.id).first())


@bp.route('/company/<username>')
@user_required
def company(username):
    company = Company.query.filter_by(id=current_user.id).first()
    dates = []
    for examination in company.examinations:
        if examination.datetime.date() not in dates:
            dates.append(examination.datetime.date())
    return render_template('company.html', title='Страница компании',
                           company=company, dates=dates)


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
    form = AddWorkerForm()
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


@bp.route('/worker/<id>')
@role_required(role='company')
@worker_in_company
def worker_profile(id):
    return render_template('worker_profile.html', title='Профиль работника',
                           worker=Worker.query.filter_by(id=id).first())


@bp.route('/<id>/edit_worker', methods=['GET', 'POST'])
@role_required(role='company')
@worker_in_company
def edit_worker(id):
    worker = Worker.query.filter_by(id=id).first()
    form = EditWorkerForm()
    if form.validate_on_submit():
        worker.first_name = form.first_name.data
        worker.middle_name = form.middle_name.data
        worker.second_name = form.second_name.data
        worker.email = form.email.data
        db.session.commit()
        flash('Данные сохранены')
        return redirect(url_for('main.edit_worker', id=worker.id))
    elif request.method == 'GET':
        form.first_name.data = worker.first_name
        form.middle_name.data = worker.middle_name
        form.second_name.data = worker.second_name
        form.email.data = worker.email
    return render_template('edit_worker.html', title='Изменение данных работника', form=form)


@bp.route('/examination', methods=['GET', 'POST'])
@role_required(role='company')
def examination():
    search_form = SearchWorkerForm()
    exam_form = ExaminationForm()
    if search_form.validate_on_submit():
        worker = Worker.query.filter_by(
            second_name=search_form.search.data).first()
        return render_template('examination.html', title='Обследование', exam_form=exam_form, worker=worker)
    if exam_form.validate_on_submit():
        exam = Examination(blood_pressure=exam_form.blood_pressure.data,
                           alcohol_level=exam_form.alcohol_level.data, worker_id=exam_form.worker_id.data,
                           company_id=current_user.id)
        db.session.add(exam)
        db.session.commit()
        flash('Данные отправлены')
    return render_template('examination.html', title='Обследование', search_form=search_form)


@bp.route('/examinations/<date>')
@role_required(role='company')
def examinations_date(date):
    company = Company.query.filter_by(id=current_user.id).first()
    exams = []
    for examination in company.examinations:
        if str(examination.datetime.date()) == str(date):
            exams.append(examination)
    return render_template('examinations_date.html', title='Результаты обследования', date=date, exams=exams, company=company)


@bp.route('/examination/<id>')
@role_required(role='company')
@exam_in_company
def view_examination(id):
    examination = Examination.query.filter_by(id=id).first_or_404()
    return render_template('view_examination.html', title='Просмотр обследования', examination=examination)
