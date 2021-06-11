from app import db
from app.decorators import exam_in_company, role_required
from app.exam import bp
from app.models import Company, Doctor, Examination, Message, User, Worker
from app.exam.forms import ExaminationForm, SearchWorkerForm
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required


@bp.route('/all')
@login_required
def view_all():
    if current_user.role == 'doctor':
        exams = Examination.query.filter_by(
            company_id=Doctor.query.get(current_user.id).company_id).all()
    elif current_user.role == 'company':
        exams = Company.query.get(current_user.id).examinations.all()
    new_messages = Message.query.filter_by(recipient_id=current_user.id, status=True).with_entities(
        Message.exam_id).distinct()
    return render_template('exam/all.html', title='Обследования', exams=exams, new_exam=new_messages)


@bp.route('/date/<date>')
@login_required
def view_date(date):
    if current_user.role == 'company':
        company = Company.query.get(current_user.id)
    elif current_user.role == 'doctor':
        company = Company.query.get(
            Doctor.query.get(current_user.id).company_id)
    exams = []
    for examination in company.examinations:
        if str(examination.datetime.date()) == str(date):
            exams.append(examination)
    return render_template('exam/view_date.html', title='Обследования {}'.format(date), date=date, exams=exams, company=company)


@bp.route('/start', methods=['GET', 'POST'])
@login_required
@role_required(role='company')
def start_examination():
    if not Company.query.get(current_user.id).workers.all():
        flash('Необходимо добавить работников')
        return redirect(url_for('main.workers'))
    if not Company.query.get(current_user.id).doctor:
        flash('Необходимо добавить доктора')
        return redirect(url_for('auth.register_doctor'))
    search_form = SearchWorkerForm()
    exam_form = ExaminationForm()
    if search_form.validate_on_submit():
        worker = Worker.query.filter_by(
            second_name=search_form.search.data).first()
        return render_template('exam/examination.html', title='Обследование', exam_form=exam_form, worker=worker)
    if exam_form.validate_on_submit():
        exam = Examination(blood_pressure=exam_form.blood_pressure.data,
                           alcohol_level=exam_form.alcohol_level.data, worker_id=exam_form.worker_id.data,
                           company_id=current_user.id)
        db.session.add(exam)
        doctor = Company.query.get(current_user.id).doctor
        doctor.add_message('', exam.id, current_user.id, doctor.id)
        db.session.commit()
        flash('Данные отправлены')
        return redirect(url_for('exam.view_examination', id=exam.id))
    return render_template('exam/examination.html', title='Обследование', search_form=search_form)


@bp.route('/<id>', methods=['GET', 'POST'])
@login_required
@exam_in_company
def view_examination(id):
    examination = Examination.query.get(id)
    messages = Message.query.filter_by(
        recipient=current_user, exam_id=id).filter(Message.status == True).all()
    for msg in messages:
        msg.status = False
        if not msg.get_data():
            db.session.delete(msg)
    db.session.commit()
    return render_template('exam/view_examination.html', title='Просмотр обследования', examination=examination,
                           messages=Message.query.filter_by(exam_id=id).filter(Message.payload_json != '""').order_by(Message.date.desc()))


@bp.route('/close_examination', methods=['POST'])
@role_required(role='doctor')
def close_examination():
    exam = Examination.query.get(request.args.get('exam', type=int))
    company = Company.query.get(exam.company_id)
    close_status = request.args.get('status', type=int)
    exam.close_time = datetime.utcnow()
    exam.close_status = close_status
    if close_status:
        message = 'Вы допущены'
    else:
        message = 'Вы не допущены'
    msg = company.add_message(message, exam.id, current_user.id, company.id)
    msg.close_exam = close_status
    db.session.commit()
    return jsonify({
        'redirect': url_for('exam.view_all')
    })


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

    user.add_message(message, exam_id, current_user.id, user.id)
    db.session.commit()

    return jsonify({
        'message': message,
        'author': 'Вы'
    })


@bp.route('/messages')
@login_required
def messages():
    reply = []
    on_chat = request.args.get('c', type=bool)
    exam_id = request.args.get('e', type=int)
    messages = current_user.messages_received.filter(
        Message.status).order_by(Message.date.asc())
    for msg in messages:

        reply.append({
            'id': msg.id,
            'status': msg.status,
            'date': msg.date,
            'payload_json': msg.get_data(),
            'unread_exams': msg.unread_exams,
            'exam_id': msg.exam_id,
            'author_id': msg.author_id,
            'recipient_id': msg.recipient_id,
            'author': msg.author.role,
            'close_exam': msg.close_exam
        })

        if on_chat and (msg.exam_id == exam_id):
            msg.status = False

    db.session.commit()
    return jsonify(reply)
