from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, SubmitField, ValidationError, validators
from wtforms.validators import DataRequired


class HardyWeinberForm(FlaskForm):
    """
    Form for HardyWeinberForm calculation
    """
    ho = FloatField('ho', validators=[DataRequired(message="Podaj ho")])
    he = FloatField('he')
    rho = FloatField('rho')
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
