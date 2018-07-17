from flask_wtf import FlaskForm
from flask_wtf.html5 import NumberInput
from wtforms import IntegerField, SelectField, SubmitField
# from flask.ext.wtf.html5 import NumberInput
from wtforms.validators import InputRequired


class HardyWeinberForm(FlaskForm):
    """
    Form for HardyWeinberForm calculation
    """
    ho = IntegerField('ho', validators=[InputRequired(message="Give ho")], widget=NumberInput(min=0), )
    he = IntegerField('he', validators=[InputRequired(message="Give he")], widget=NumberInput(min=0))
    rho = IntegerField('rho', validators=[InputRequired(message="Give rho")], widget=NumberInput(min=0))
    critical_select = SelectField(u'Level of significance',
                                  choices=[('1', '0.05'), ('2', '0.01')],
                                  validators=[InputRequired(message="Select level of significance")])
    submit = SubmitField('Calcuate!')
