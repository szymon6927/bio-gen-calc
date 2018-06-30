# app/home/views.py

from flask import render_template, flash
from .forms import HardyWeinberForm
from . import hardy_weinber
from .utils import HardyWeinberCalculation
from .. import detect_domain


@hardy_weinber.route('/hardy-weinber-page')
def hardy_weinber_page():
    """
    Render the hardy_weinber template on the / route
    """
    detect_domain()
    form = HardyWeinberForm()
    return render_template('hardy_weinber/index.html', form=form, title="Hardy-Weinberg equilibrium")


@hardy_weinber.route('/hwcalculate', methods=['GET', 'POST'])
def hw_calculate():
    form = HardyWeinberForm()
    if (form.ho.data == 0 and form.he.data == 0) or (form.he.data == 0 and form.rho.data == 0):
        flash('Incorrect validation, more than two values are equal to 0 !')
        return render_template('hardy_weinber/index.html', form=form,
                               title="Hardy-Weinberg equilibrium")

    if form.validate_on_submit():
        flash('Validation correct!')
        hw = HardyWeinberCalculation(form.ho.data, form.he.data, form.rho.data, form.critical_select.data)
        result = hw.get_calculations()
        return render_template('hardy_weinber/index.html', form=form, result=result,
                               title="Hardy-Weinberg equilibrium")
    else:
        flash('Something goes wrong, try again!')
        return render_template('hardy_weinber/index.html', form=form,
                               title="Hardy-Weinberg equilibrium")
