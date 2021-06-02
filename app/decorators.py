from app.models import Company, Doctor
from flask import current_app, flash, request, redirect, url_for, abort
from flask_login import config, current_user
from functools import wraps


def role_required(role):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if request.method in config.EXEMPT_METHODS:
                return func(*args, **kwargs)
            elif current_app.config.get('LOGIN_DISABLED'):
                return func(*args, **kwargs)
            elif not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            elif not current_user.role == role:
                flash('Эта страница не доступна для просмотра')
                return redirect(url_for('main.index'))
            return func(*args, **kwargs)
        return decorated_view
    return wrapper


def user_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in config.EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not current_user.username in str(request):
            if current_user.role == 'company' and not Company.query.get(current_user.id).doctor.username in str(request):
                return abort(404)
            elif current_user.role == 'doctor' and not Company.query.get(Doctor.query.get(current_user.id).company_id).username in str(request):
                return abort(404)
        return func(*args, **kwargs)
    return decorated_view


def worker_in_company(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        for worker in Company.query.filter_by(id=current_user.id).first().workers:
            if str(worker.id) == request.view_args.get('id'):
                return func(*args, **kwargs)
        return abort(404)
    return decorated_view


def exam_in_company(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        for exam in Company.query.filter_by(id=current_user.id).first().examinations:
            if str(exam.id) == request.view_args.get('id'):
                return func(*args, **kwargs)
        return abort(404)
    return decorated_view
