from app import db
from app.errors import bp
from flask import render_template


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500


@bp.app_errorhandler(405)
def method_not_allowed_error(error):
    db.session.rollback()
    return render_template('errors/404.html'), 405


@bp.errorhandler(413)
def too_large(error):
    # ? Template
    return 'Слишком большой файл', 413
