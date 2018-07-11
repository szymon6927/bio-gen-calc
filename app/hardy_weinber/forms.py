from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField, ValidationError, validators
from flask.ext.wtf.html5 import NumberInput
from wtforms.validators import InputRequired


class HardyWeinberForm(FlaskForm):
    """
    Form for HardyWeinberForm calculation
    """
    ho = IntegerField('ho', validators=[InputRequired(message="Podaj ho")], widget=NumberInput(min=0), )
    he = IntegerField('he', validators=[InputRequired(message="Podaj he")], widget=NumberInput(min=0))
    rho = IntegerField('rho', validators=[InputRequired(message="Podaj rho")], widget=NumberInput(min=0))
    critical_select = SelectField(u'Programming Language',
                                  choices=[('1', '0.05'), ('2', '0.01')],
                                  validators=[InputRequired(message="Wybierz stopień istoności")])
    submit = SubmitField('Calcuate!')