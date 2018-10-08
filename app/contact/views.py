from flask import Flask, render_template, flash, redirect, url_for
from . import contact
from flask_mail import Mail, Message
from .forms import ContactForm


@contact.route('/contact', methods=['GET', 'POST'])
def contact_page():
    form = ContactForm()
    if form.validate_on_submit():
        app = Flask(__name__)
        mail = Mail(app)

        msg = Message("Test message", sender=("Gene-Calc Team", "contact@gene-calc.pl"), recipients=[form.email.data])
        mail.send(msg)

        flash(f'Thanks <strong>{form.name.data}</strong> for your message.')
        return redirect(url_for('contact.contact_page'))
    
    return render_template('contact/index.html', title="Contact Us", form=form)

