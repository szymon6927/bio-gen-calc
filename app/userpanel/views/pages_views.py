from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import login_required
from sqlalchemy import asc

from app.database import db
from app.userpanel.decorators import superuser_required
from app.userpanel.forms import PageEditForm
from app.userpanel.models import Page
from app.userpanel.views import userpanel


@userpanel.route('/pages')
@login_required
@superuser_required
def pages_list_view():
    pages = Page.query.order_by(asc(Page.id)).all()
    return render_template('userpanel/pages/pages.html', pages=pages)


@userpanel.route('/pages/<int:page_id>', methods=['GET', 'POST'])
@login_required
@superuser_required
def page_details_view(page_id):
    page = Page.query.get_or_404(page_id)
    form = PageEditForm(obj=page)

    if form.validate_on_submit():
        page.name = form.name.data
        page.is_active = form.is_active.data
        page.slug = form.slug.data
        page.seo_title = form.seo_title.data
        page.seo_desc = form.seo_desc.data
        page.seo_keywords = form.seo_keywords.data
        page.text = form.text.data
        page.desc = form.desc.data

        db.session.add(page)
        db.session.commit()

        flash('You have successfully edited the page.', 'success')

        return redirect(url_for('userpanel.page_details_view', page_id=page.id))

    return render_template('userpanel/pages/page_details.html', form=form, page=page)


@userpanel.route('/pages/add-page', methods=['GET', 'POST'])
@login_required
@superuser_required
def page_add_view():
    form = PageEditForm()

    if form.validate_on_submit():
        page = Page()
        page.name = form.name.data
        page.is_active = form.is_active.data
        page.slug = form.slug.data
        page.seo_title = form.seo_title.data
        page.desc = form.seo_desc.data
        page.seo_keywords = form.seo_keywords.data
        page.text = form.text.data
        page.desc = form.desc.data

        db.session.add(page)
        db.session.commit()

        flash('You have successfully added the page.', 'success')

        return redirect(url_for('userpanel.pages_list_view'))

    return render_template('userpanel/pages/page_add.html', form=form)


@userpanel.route('/pages/delete/<int:page_id>')
@login_required
@superuser_required
def page_delete_view(page_id):
    page = Page.query.get_or_404(page_id)

    db.session.delete(page)
    db.session.commit()

    flash('You have successfully delete the page - {}.'.format(page.name), 'success')

    return redirect(url_for('userpanel.pages_list_view'))
