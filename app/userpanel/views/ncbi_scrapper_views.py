import csv
import io

from flask import flash
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required

from app.database import db
from app.mail_scrapper.ncbi_scrapper import NCBIPubScrapper
from app.userpanel.decorators import superuser_required
from app.userpanel.forms import NCBIMailFrom
from app.userpanel.forms import NCBIPackageForm
from app.userpanel.forms import NCBIScrapperForm
from app.userpanel.forms import get_mail_package_choices
from app.userpanel.models import NCBIMail
from app.userpanel.models import NCBIMailPackage
from app.userpanel.views import userpanel


@userpanel.route('/ncbi-scrapper/packages')
@login_required
@superuser_required
def ncbi_packages_list_view():
    ncbi_packages = NCBIMailPackage.query.order_by(NCBIMailPackage.created_at).all()

    return render_template('userpanel/ncbi_scrapper/packages.html', ncbi_packages=ncbi_packages)


@userpanel.route('/ncbi-scrapper/package/<int:package_id>', methods=['GET', 'POST'])
@login_required
@superuser_required
def ncbi_package_details_view(package_id):
    ncbi_package = NCBIMailPackage.query.get_or_404(package_id)
    ncbi_mails = NCBIMail.query.filter_by(package_id=ncbi_package.id).all()

    form = NCBIPackageForm(obj=ncbi_package)

    if form.validate_on_submit():
        ncbi_package.name = form.name.data
        ncbi_package.was_sent = form.was_sent.data
        ncbi_package.comment = form.comment.data

        db.session.add(ncbi_package)
        db.session.commit()

        flash('You have successfully edited the package.', 'success')

        return redirect(url_for('userpanel.ncbi_package_details_view', package_id=package_id))

    return render_template(
        'userpanel/ncbi_scrapper/package_details.html', ncbi_package=ncbi_package, ncbi_mails=ncbi_mails, form=form
    )


@userpanel.route('/ncbi-scrapper/package/delete/<int:package_id>')
@login_required
@superuser_required
def ncbi_package_delete_view(package_id):
    ncbi_package = NCBIMailPackage.query.get_or_404(package_id)

    db.session.delete(ncbi_package)
    db.session.commit()

    flash('You have successfully delete the package - {}.'.format(ncbi_package.name), 'success')

    return redirect(url_for('userpanel.ncbi_packages_list_view'))


@userpanel.route('/ncbi-scrapper/packages/add', methods=['GET', 'POST'])
@login_required
@superuser_required
def ncbi_package_add_view():
    form = NCBIPackageForm()

    if form.validate_on_submit():
        ncbi_package = NCBIMailPackage()
        ncbi_package.name = form.name.data
        ncbi_package.comment = form.comment.data

        db.session.add(ncbi_package)
        db.session.commit()

        flash('You have successfully added the package.', 'success')

        return redirect(url_for('userpanel.ncbi_packages_list_view'))

    return render_template('userpanel/ncbi_scrapper/package_add.html', form=form)


@userpanel.route('/ncbi-scrapper/packages/export-to-csv/<int:package_id>')
@login_required
@superuser_required
def ncbi_packages_csv_export_view(package_id):
    ncbi_package = NCBIMailPackage.query.get_or_404(package_id)

    dest = io.StringIO()
    writer = csv.writer(dest)

    csv_header = ["Email Address", "Created At"]
    writer.writerow(csv_header)

    for email_obj in ncbi_package.email:
        writer.writerow([email_obj.email, email_obj.created_at])

    csv_response = make_response(dest.getvalue())
    csv_response.headers[
        "Content-Disposition"
    ] = f"attachment; filename=export-{ncbi_package.name.replace(' ', '_')}.csv"
    csv_response.headers["Content-type"] = "text/csv"
    return csv_response


@userpanel.route('/ncbi-scrapper/email/<int:email_id>', methods=['GET', 'POST'])
@login_required
@superuser_required
def ncbi_email_details_view(email_id):
    ncbi_mail = NCBIMail.query.get_or_404(email_id)

    form = NCBIMailFrom(obj=ncbi_mail)
    form.mail_package.choices = get_mail_package_choices()

    if request.method == 'GET':
        form.mail_package.data = ncbi_mail.package_id

    if form.validate_on_submit():
        ncbi_mail.email = form.email.data
        ncbi_mail.ncbi_publication_url = form.ncbi_publication_url.data
        ncbi_mail.publication_id = form.publication_id.data
        ncbi_mail.package_id = form.mail_package.data

        db.session.commit()

        flash('You have successfully edited the mail.', 'success')

        return redirect(url_for('userpanel.ncbi_email_details_view', email_id=email_id))

    return render_template('userpanel/ncbi_scrapper/mail_details.html', ncbi_mail=ncbi_mail, form=form)


@userpanel.route('/ncbi-scrapper/email/delete/<int:email_id>')
@login_required
@superuser_required
def ncbi_email_delete_view(email_id):
    ncbi_email = NCBIMail.query.get_or_404(email_id)

    db.session.delete(ncbi_email)
    db.session.commit()

    flash(f'You have successfully delete the email - {ncbi_email.email}.', 'success')

    return redirect(url_for('userpanel.ncbi_package_details_view', package_id=ncbi_email.package_id))


@userpanel.route('/ncbi-scrapper/emails')
@login_required
@superuser_required
def ncbi_emails_list_view():
    ncbi_emails = NCBIMail.query.order_by(NCBIMail.created_at).all()

    return render_template('userpanel/ncbi_scrapper/mails.html', ncbi_emails=ncbi_emails)


@userpanel.route('/ncbi-scrapper/email/add', methods=['GET', 'POST'])
@login_required
@superuser_required
def ncbi_email_add_view():
    form = NCBIMailFrom()
    form.mail_package.choices = get_mail_package_choices()

    if form.validate_on_submit():
        ncbi_mail = NCBIMail()
        ncbi_mail.email = form.email.data
        ncbi_mail.ncbi_publication_url = form.ncbi_publication_url.data
        ncbi_mail.publication_id = form.publication_id.data
        ncbi_mail.package_id = int(form.mail_package.data)

        db.session.add(ncbi_mail)
        db.session.commit()

        flash(f'You have successfully added the mail to the package.', 'success')

        return redirect(url_for('userpanel.ncbi_package_details_view', package_id=ncbi_mail.package_id))

    return render_template('userpanel/ncbi_scrapper/mail_add.html', form=form)


@userpanel.route('/ncbi-scrapper/scrapper', methods=['GET', 'POST'])
@login_required
@superuser_required
def ncbi_scrapper_run_view():
    form = NCBIScrapperForm()
    form.mail_package.choices = get_mail_package_choices()

    if form.validate_on_submit():
        scrapper = NCBIPubScrapper()
        ncbi_objects = scrapper.run(0, form.publication_number.data)

        objects_to_add = []

        for ncbi_object in ncbi_objects:
            ncbi_mail = NCBIMail(
                publication_id=ncbi_object.publication_id,
                ncbi_publication_url=ncbi_object.publication_url,
                email=ncbi_object.email,
                package_id=form.mail_package.data,
            )

            exist = NCBIMail.query.filter_by(email=ncbi_mail.email).first()

            if not exist:
                objects_to_add.append(ncbi_mail)
                flash(f'Successfully added {ncbi_mail.email}', 'info')
            else:
                flash(f'E-mail {ncbi_mail.email} already exist in DB', 'danger')

        if objects_to_add:
            db.session.add_all(objects_to_add)
            db.session.commit()

            flash(
                f'You have successfully scrapped {len(objects_to_add)} e-mails ',
                f'form {form.publication_number.data} NCBI publications success',
            )

        return redirect(url_for('userpanel.ncbi_scrapper_run_view'))

    return render_template('userpanel/ncbi_scrapper/scrapper.html', form=form)
