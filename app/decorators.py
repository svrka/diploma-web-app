from app.models import Company, Doctor
from flask import flash, request, redirect, url_for, abort
from flask_login import current_user
from functools import wraps


def role_required(role):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.role == role:
                flash('Эта страница не доступна для просмотра')
                return redirect(url_for('main.index'))
            return func(*args, **kwargs)
        return decorated_view
    return wrapper


def user_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.username in str(request):
            if current_user.role == 'company' and not Company.query.get(current_user.id).doctor.username in str(request):
                return abort(404)
            elif current_user.role == 'doctor' and not Company.query.get(Doctor.query.get(current_user.id).company_id).username in str(request):
                return abort(404)
        return func(*args, **kwargs)
    return decorated_view


def worker_in_company(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.role == 'company':
            id = current_user.id
        elif current_user.role == 'doctor':
            id = Doctor.query.get(current_user.id).company_id
        for worker in Company.query.get(id).workers:
            if str(worker.id) == request.view_args.get('id'):
                return func(*args, **kwargs)
        return abort(404)
    return decorated_view


def exam_in_company(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.role == 'company':
            id = current_user.id
        elif current_user.role == 'doctor':
            id = Doctor.query.get(current_user.id).company_id
        for exam in Company.query.filter_by(id=id).first().examinations:
            if str(exam.id) == request.view_args.get('id'):
                return func(*args, **kwargs)
        return abort(404)
    return decorated_view
