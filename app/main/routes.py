from app import db
from app.decorators import exam_in_company, worker_in_company, role_required, user_required
from app.main import bp
from app.models import Company, Doctor, Examination, Message, User, Worker
from app.main.forms import AddWorkerForm, EditCompanyForm, EditDoctorForm, EditWorkerForm, ExaminationForm, SearchWorkerForm
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Главная')


@bp.route('/doctor/<username>')
@login_required
@user_required
def doctor(username):
    if current_user.role == 'doctor':
        doctor = Doctor.query.get(current_user.id)
        company = Company.query.get(doctor.company_id)
    elif current_user.role == 'company':
        company = Company.query.get(current_user.id)
        doctor = company.doctor
    return render_template('doctor.html', title='Страница врача', doctor=doctor, company=company)


@bp.route('/company/<username>')
@login_required
@user_required
def company(username):
    if current_user.role == 'doctor':
        doctor = Doctor.query.get(current_user.id)
        company = Company.query.get(doctor.company_id)
    elif current_user.role == 'company':
        company = Company.query.get(current_user.id)
    dates = []
    for examination in company.examinations:
        if examination.datetime.date() not in dates:
            dates.append(examination.datetime.date())
    return render_template('company.html', title='Страница компании', company=company, dates=dates)


@bp.route('/edit_company', methods=['GET', 'POST'])
@login_required
@role_required(role='company')
def edit_company():
    company = Company.query.get(current_user.id)
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
@login_required
@role_required(role='doctor')
def edit_doctor():
    doctor = Doctor.query.get(current_user.id)
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
@login_required
def workers():
    form = AddWorkerForm()
    if form.validate_on_submit():
        worker = Worker(first_name=form.first_name.data, middle_name=form.middle_name.data,
                        second_name=form.second_name.data, email=form.email.data, company_id=current_user.id)
        db.session.add(worker)
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
    return render_template('workers.html', title='Работники', form=form,
                           company=company, workers=workers)


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
    return render_template('edit_worker.html', title='Изменение данных работника', form=form)


@bp.route('/examination', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('main.view_examination', id=exam.id))
    return render_template('examination.html', title='Обследование', search_form=search_form)


@bp.route('/examinations/<date>')
@login_required
def examinations_date(date):
    if current_user.role == 'company':
        company = Company.query.get(current_user.id)
    elif current_user.role == 'doctor':
        company = Company.query.get(
            Doctor.query.get(current_user.id).company_id)
    exams = []
    for examination in company.examinations:
        if str(examination.datetime.date()) == str(date):
            exams.append(examination)
    return render_template('examinations_date.html', title='Обследования {}'.format(date), date=date, exams=exams, company=company)


@bp.route('/examination/<id>', methods=['GET', 'POST'])
@login_required
@exam_in_company
def view_examination(id):
    examination = Examination.query.get(id)
    # ? Redundant
    current_user.last_message_read_time = datetime.utcnow()
    messages = Message.query.filter_by(
        recipient=current_user).filter(Message.status == True).all()
    for msg in messages:
        msg.status = False
    db.session.commit()
    return render_template('view_examination.html', title='Просмотр обследования', examination=examination,
                           messages=Message.query.filter_by(exam_id=id).order_by(Message.timestamp.desc()))


@bp.route('/send_message', methods=['POST'])
@login_required
def send_message():
    message = request.form['message']
    exam_id = request.form['exam_id']

    examination = Examination.query.get(exam_id)
    if current_user.role == 'company':
        user = User.query.get(examination.company.doctor.id)
    elif current_user.role == 'doctor':
        user = User.query.get(examination.company_id)

    user.add_message(message, exam_id, current_user.id,
                     user.id, user.new_messages)
    db.session.commit()

    return jsonify({
        'message': message,
        'author': current_user.role
    })


# TODO: Company access
@bp.route('/examinations')
@login_required
@role_required(role='doctor')
def examinations():
    exams = Examination.query.filter_by(
        company_id=Doctor.query.get(current_user.id).company_id).all()
    return render_template('examinations.html', title='Обследования', exams=exams)


@bp.route('/messages')
@login_required
def messages():
    since = request.args.get('since', 0.0, type=float)
    messages = current_user.messages_received.filter(
        Message.timestamp > since).order_by(Message.timestamp.asc())
    return jsonify([{
        'id': msg.id,
        'status': msg.status,
        'date': msg.date,
        'timestamp': msg.timestamp,
        'body': msg.body,
        'payload_json': msg.payload_json,
        'exam_id': msg.exam_id,
        'author_id': msg.author_id,
        'recipient_id': msg.recipient_id,
        'author': msg.author.role,
    } for msg in messages])
