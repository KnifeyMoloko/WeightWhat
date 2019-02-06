from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from .import mail


def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app. _get_current_object()

    msg = Message(subject=app.config['MAIL_SUBJECT'] + subject,
                  recipients=[to], sender=app.config['MAIL_SENDER'])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)

    thr = Thread(target=async_send_mail, args=[app, msg])
    thr.start()
    return thr
