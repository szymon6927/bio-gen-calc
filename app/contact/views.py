from flask import render_template, flash, redirect, url_for
from . import contact
from .forms import ContactForm


@contact.route('/contact', methods=['GET', 'POST'])
def contact_page():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        flash(f'Thanks <strong>{contact_form.name.data}</strong> for your message.')
        return redirect(url_for('contact.contact_page'))
    
    return render_template('contact/index.html', title="Contact Us", form=contact_form)

