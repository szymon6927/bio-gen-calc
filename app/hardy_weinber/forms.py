from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField, ValidationError, validators
from wtforms.validators import InputRequired


class HardyWeinberForm(FlaskForm):
    """
    Form for HardyWeinberForm calculation
    """
    ho = IntegerField('ho', validators=[InputRequired(message="Podaj ho")])
    he = IntegerField('he', validators=[InputRequired(message="Podaj he")])
    rho = IntegerField('rho', validators=[InputRequired(message="Podaj rho")])
    critical_select = SelectField(u'Programming Language',
                                  choices=[('1', '0.01'), ('2', '0.05')],
                                  validators=[InputRequired(message="Wybierz stopień istoności")])
    submit = SubmitField('Calcuate!')

    # def validate_ho(self, field):
    #     if field.data < 0:
    #         raise ValidationError('Field can not be a 0 value')
    #
    # def validate_he(self, field):
    #     if field.data < 0:
    #         raise ValidationError('Field can not be a 0 value')
    #
    # def validate_rho(self, field):
    #     if field.data < 0:
    #         raise ValidationError('Field can not be a 0 value')
