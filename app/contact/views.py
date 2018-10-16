from flask import Flask, render_template, flash, redirect, url_for
from . import contact
from flask_mail import Mail, Message
from .forms import ContactForm

import smtplib


@contact.route('/contact', methods=['GET', 'POST'])
def contact_page():
    form = ContactForm()
    if form.validate_on_submit():
        app = Flask(__name__)
        mail = Mail(app)

        msg = Message("Message from gene-calc.pl contact page",
                      sender=("Gene-Calc Team - contact", "contact@gene-calc.pl"),
                      recipients=[form.email.data])
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
