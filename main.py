from app import create_app, db
from app.models import Message, Notification, User, Doctor, Company, Worker, Examination

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Doctor': Doctor, 'Company': Company, 'Worker': Worker,
            'Examination': Examination, 'Message': Message, 'Notification': Notification}
