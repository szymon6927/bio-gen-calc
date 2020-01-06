from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from sqlalchemy import func
from werkzeug.security import generate_password_hash

from app.customer_calculation.models import CustomerCalculation
from app.database import db
from app.helpers.file_helper import save_picture
from app.userpanel.forms import CustomerEditForm
from app.userpanel.models import Customer
from app.userpanel.models import CustomerActivity
from app.userpanel.models import Page
from app.userpanel.views import userpanel


@userpanel.route('/', methods=['GET'], strict_slashes=False)
@login_required
def userpanel_view():
    return redirect(url_for('userpanel.dashboard_view'))


@userpanel.route('/dashboard', methods=['GET'])
@login_required
def dashboard_view():
    activity = (
        CustomerActivity.query.with_entities(
            CustomerActivity.url, CustomerActivity.module_name, func.count(CustomerActivity.url).label('count')
        )
        .filter_by(customer=current_user)
        .group_by(CustomerActivity.url, CustomerActivity.module_name)
        .all()
    )

    statistics = {}
    statistics['total_calculations'] = CustomerCalculation.query.filter_by(customer=current_user).count()
    statistics['total_visits'] = CustomerActivity.query.filter_by(customer=current_user).count()
    return render_template(
        'userpanel/dashboard.html', title="Dashboard", user=current_user.login, activity=activity, statistics=statistics
    )


@userpanel.route('/editprofile', methods=['GET', 'POST'])
@login_required
def edit_profile_view():
    profile = Customer.query.get_or_404(current_user.id)
    form = CustomerEditForm(obj=profile)

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            profile.profile_pic = picture_file

        if form.password.data:
            profile.password = generate_password_hash(form.password.data, method='sha256')

        profile.first_name = form.first_name.data
        profile.last_name = form.last_name.data

        db.session.add(profile)
        db.session.commit()

        flash('You have successfully edited the profile.', 'success')

        return redirect(url_for('userpanel.edit_profile_view'))

    profile_pic = url_for('static', filename='uploads/profile_pics/' + current_user.profile_pic)

    return render_template('userpanel/customers/customer_edit_profile.html', form=form, profile_pic=profile_pic)


@userpanel.context_processor
def inject():
    return {'module_desc': Page.query.filter_by(slug=request.path).first()}
