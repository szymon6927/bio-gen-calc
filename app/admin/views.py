from wtforms import fields, widgets

import flask_admin as admin
from flask_admin import BaseView, expose
from flask_admin.contrib import sqla

from ..database import db
from .models import Page


class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        # add WYSIWYG class to existing classes
        existing_classes = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'%s %s' % (existing_classes, "ckeditor")
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(fields.TextAreaField):
    widget = CKTextAreaWidget()


class PageAdmin(sqla.ModelView):
    form_overrides = dict(text=CKTextAreaField)
    create_template = 'admin_overwrite/create.html'
    edit_template = 'admin_overwrite/edit.html'


def run_admin():
    admin_panel = admin.Admin(name="Gene Calc - Admin Panel", base_template='admin_overwrite/layout.html', template_mode='bootstrap4')
    admin_panel.add_view(PageAdmin(Page, db.session))

    return admin_panel
