from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, widgets
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    login = StringField(validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField(validators=[DataRequired(), Length(min=8, max=80)])


class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        # add WYSIWYG class to existing classes
        existing_classes = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'%s %s' % (existing_classes, "ckeditor")
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()
