import smtplib
from os import environ

from flask import Blueprint
from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_mail import Mail
from flask_mail import Message

from app.common.decorators import add_customer_activity
from app.contact.forms import ContactForm
from app.contact.literals import ERROR_MESSAGE
from app.contact.literals import MESSAGE_TITLE
from app.contact.literals import SENDER_NAME
from app.userpanel.models import Page

contact = Blueprint('contact', __name__)


@contact.route('/contact', methods=['GET', 'POST'])
@add_customer_activity
def contact_page():
    form = ContactForm()
    if form.validate_on_submit():
        app = Flask(__name__)
        mail = Mail(app)

        msg = Message(
            MESSAGE_TITLE,
            sender=(SENDER_NAME, environ.get('EMAIL', "contact@gene-calc.pl")),
            recipients=[environ.get('EMAIL', "contact@gene-calc.pl")],
        )
        msg.body = f'From: {form.name.data} \nE-mail: {form.email.data} \nMessage: {form.message.data}'

        try:
            mail.send(msg)
            flash(f'Thanks <strong>{form.name.data}</strong> for your message.', 'success')
        except smtplib.SMTPAuthenticationError:
            flash(f'{ERROR_MESSAGE}', 'danger')
        except smtplib.SMTPServerDisconnected:
            flash(f'{ERROR_MESSAGE}', 'danger')
        except smtplib.SMTPException:
            flash(f'{ERROR_MESSAGE}', 'danger')
        except OSError:
            flash(f'{ERROR_MESSAGE}', 'danger')

        return redirect(url_for('contact.contact_page'))

    return render_template('contact/index.html', title="Contact Us", form=form)


@contact.context_processor
def inject():
    return {'module_desc': Page.query.filter_by(slug=request.path).first()}
