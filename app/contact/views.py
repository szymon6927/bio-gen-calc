import smtplib
from os import environ

from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_mail import Mail
from flask_mail import Message

from app.common.decorators import add_customer_activity
from app.contact import contact
from app.contact.forms import ContactForm
from app.contact.literals import MESSAGE_TITLE
from app.contact.literals import SENDER_NAME
from app.userpanel.models import Page


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
            recipients=[form.email.data],
        )
        msg.body = form.message.data
        try:
            mail.send(msg)
            flash(f'Thanks <strong>{form.name.data}</strong> for your message.', 'success')
        except smtplib.SMTPAuthenticationError as e:
            flash(f'SMTPAuthenticationError, {e}', 'danger')
        except smtplib.SMTPServerDisconnected as e:
            flash(f'SMTPServerDisconnected, {e}', 'danger')
        except smtplib.SMTPException as e:
            flash(f'SMTPException, {e}', 'danger')
        except OSError as e:
            flash(f'OSError {e}', 'danger')

        return redirect(url_for('contact.contact_page'))

    return render_template('contact/index.html', title="Contact Us", form=form)


@contact.context_processor
def inject():
    return {'module_desc': Page.query.filter_by(slug=request.path).first()}
