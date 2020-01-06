from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from sqlalchemy import asc
from sqlalchemy import desc

from app.customer_calculation.models import CustomerCalculation
from app.database import db
from app.userpanel.views import userpanel


@userpanel.route('/calculations', methods=['GET'])
@login_required
def calculations_list_view():
    query = request.args.get('query')
    order_by = request.args.get('order_by', "created_at")
    sort_by = request.args.get('sort_by')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if query:
        return redirect(
            url_for('userpanel.calculations_search_view', query=query, order_by=order_by, sort_by=sort_by, page=page)
        )

    if sort_by == "desc":
        calculations = (
            CustomerCalculation.query.filter_by(customer=current_user)
            .order_by(desc(order_by))
            .paginate(page=page, per_page=per_page)
        )
    elif sort_by == "asc":
        calculations = (
            CustomerCalculation.query.filter_by(customer=current_user)
            .order_by(asc(order_by))
            .paginate(page=page, per_page=per_page)
        )
    else:
        calculations = (
            CustomerCalculation.query.filter_by(customer=current_user)
            .order_by(desc(order_by))
            .paginate(page=page, per_page=per_page)
        )

    return render_template('userpanel/calculations/calculations.html', calculations=calculations)


@userpanel.route('/calculations/search', methods=['GET'])
@login_required
def calculations_search_view():
    query = request.args.get('query')
    order_by = request.args.get('order_by', "created_at")
    sort_by = request.args.get('sort_by')
    page = request.args.get('page', 1, type=int)
    per_page = 5
    if sort_by == "desc":
        calculations = (
            CustomerCalculation.query.filter(CustomerCalculation.title.like(f'%{query}%'))
            .filter(CustomerCalculation.customer == current_user)
            .order_by(desc(order_by))
            .paginate(page=page, per_page=per_page)
        )
    elif sort_by == "asc":
        calculations = (
            CustomerCalculation.query.filter(CustomerCalculation.title.like(f'%{query}%'))
            .filter(CustomerCalculation.customer == current_user)
            .order_by(asc(order_by))
            .paginate(page=page, per_page=per_page)
        )
    else:
        calculations = (
            CustomerCalculation.query.filter(CustomerCalculation.title.like(f'%{query}%'))
            .filter(CustomerCalculation.customer == current_user)
            .order_by(desc(order_by))
            .paginate(page=page, per_page=per_page)
        )

    return render_template('userpanel/calculations/calculations.html', calculations=calculations)


@userpanel.route('/calculations/delete/<int:calculation_id>')
@login_required
def calculation_delete_view(calculation_id):
    calculation = CustomerCalculation.query.filter_by(id=calculation_id).first()
    db.session.delete(calculation)
    db.session.commit()

    flash('You have successfully deleted the calculation.', 'success')

    return redirect(url_for('userpanel.calculations_list_view'))


@userpanel.route('/calculations/<int:calculation_id>')
@login_required
def calculation_details_view(calculation_id):
    calculation = CustomerCalculation.query.filter_by(id=calculation_id).first()

    return render_template('userpanel/calculations/calculation_details.html', calculation=calculation)
