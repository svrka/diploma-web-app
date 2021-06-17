from app import db
from app.decorators import worker_in_company, role_required, user_required
from app.main import bp
from app.models import Company, Doctor, Worker
from app.main.forms import AddWorkerForm, EditCompanyForm, EditDoctorForm, EditWorkerForm
from flask import render_template, flash, redirect, url_for, request, abort, current_app, send_from_directory
from flask_login import current_user, login_required
import os
from werkzeug.utils import secure_filename


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='О дипломе')


@bp.route('/dashboard')
def dashboard():
    abort(404)


@bp.route('/doctor/<username>')
@login_required
@user_required
def doctor(username):
    doctor = Doctor.query.filter_by(username=username).first_or_404()
    company = Company.query.get(doctor.company_id)
    return render_template('doctor.html', title='Страница врача', doctor=doctor, company=company)


@bp.route('/company/<username>')
@login_required
@user_required
def company(username):
    company = Company.query.filter_by(username=username).first_or_404()
    dates = []
    for examination in company.examinations:
        if examination.datetime.date() not in dates:
            dates.append(examination.datetime.date())
    return render_template('company.html', title='Страница компании', company=company, dates=dates)


@bp.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
    if current_user.role == 'doctor':
        form = EditDoctorForm(current_user.username, current_user.email)
        user = Doctor.query.get(current_user.id)
    elif current_user.role == 'company':
        form = EditCompanyForm(current_user.username, current_user.email)
        user = Company.query.get(current_user.id)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if current_user.role == 'doctor':
            user.first_name = form.first_name.data
            user.second_name = form.second_name.data
        elif current_user.role == 'company':
            user.name = form.name.data
            user.about = form.about.data
        db.session.commit()
        flash('Данные сохранены')
        return redirect(url_for('main.edit_user'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        if current_user.role == 'doctor':
            form.first_name.data = user.first_name
            form.second_name.data = user.second_name
        elif current_user.role == 'company':
            form.name.data = user.name
            form.about.data = user.about
    return render_template('edit_user.html', title='Настройка доктора', form=form)


@bp.route('/upload_avatar/<table>/<id>', methods=['POST'])
@login_required
def upload_avatar(table, id):
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if table == 'user':
        user = current_user
        reply = url_for('main.edit_user')
    elif table == 'worker':
        user = Worker.query.get(id)
        reply = url_for('main.edit_worker', id=id)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        user.avatar_file = filename
        db.session.commit()
        uploaded_file.save(os.path.join(user.uploads_path, filename))
    flash('Аватар сохранен')
    return redirect(reply)


@bp.route('/uploads/<path>/<filename>')
@login_required
def uploads(path, filename):
    return send_from_directory(os.path.join('..', path), filename)


@bp.route('/workers', methods=['GET', 'POST'])
@login_required
def workers():
    form = AddWorkerForm()
    if form.validate_on_submit():
        worker = Worker(first_name=form.first_name.data, middle_name=form.middle_name.data,
                        second_name=form.second_name.data, email=form.email.data, company_id=current_user.id)
        db.session.add(worker)
        db.session.commit()
        if not os.path.exists('{}/workers/{}'.format(current_user.uploads_path, worker.id)):
            os.mkdir('{}/workers/{}'.format(current_user.uploads_path, worker.id))
        worker.uploads_path = os.path.join(
            current_user.uploads_path, 'workers', str(worker.id))
        db.session.commit()
        flash('Новый сотрудник добавлен')
        return redirect(url_for('main.workers'))
    if current_user.role == 'company':
        company = Company.query.get(current_user.id)
        workers = Worker.query.filter_by(company_id=current_user.id).all()
    elif current_user.role == 'doctor':
        doctor = Doctor.query.get(current_user.id)
        company = Company.query.get(doctor.company_id)
        workers = Worker.query.filter_by(company_id=doctor.company_id).all()
    return render_template('workers.html', title='Работники', form=form, company=company, workers=workers)


@bp.route('/worker/<id>')
@login_required
@worker_in_company
def worker_profile(id):
    return render_template('worker_profile.html', title='Профиль работника', worker=Worker.query.get(id))


@bp.route('/<id>/edit_worker', methods=['GET', 'POST'])
@login_required
@role_required(role='company')
@worker_in_company
def edit_worker(id):
    worker = Worker.query.get(id)
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
    return render_template('edit_worker.html', title='Изменение данных работника', worker=worker, form=form)
