# app/home/views.py

from flask import render_template, flash
from flask import jsonify
from .forms import HardyWeinberForm
from . import hardy_weinber


@hardy_weinber.route('/hardy_weinber_page')
def hardy_weinber_page():
    """
    Render the hardy_weinber template on the / route
    """
    form = HardyWeinberForm()
    return render_template('hardy_weinber/index.html', form=form, title="Hardy-Weinberg equalibration")


@hardy_weinber.route('/hwcalculate', methods=['GET', 'POST'])
def hw_calculate():
    form = HardyWeinberForm()
    print("He = {} !!".format(form.he.data), flush=True)
    if form.validate_on_submit():
        flash('Walidacja ok')
        return render_template('hardy_weinber/index.html', form=form, result=form.he.data,
                               title="Hardy-Weinberg equalibration")
    else:
        flash('Walidacja bledna')
        return render_template('hardy_weinber/index.html', form=form, result=form.he.data,
                               title="Hardy-Weinberg equalibration")
