from app.models import Company
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
            return abort(404)
        return func(*args, **kwargs)
    return decorated_view


def company_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        result = False
        for worker in Company.query.filter_by(id=current_user.id).first().workers:
            if str(worker.id) == request.view_args.get('id'):
                result = True
        if result:
            return func(*args, **kwargs)
        else:
            return abort(404)
    return decorated_view
