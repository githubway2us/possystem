from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import db, Product

product_bp = Blueprint('product', __name__, url_prefix='/product')

@product_bp.route('/')
@login_required
def list_products():
    products = Product.query.all()
    return render_template('product_list.html', products=products)

@product_bp.route('/add', methods=['POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        return "Permission denied"
    name = request.form['name']
    stock = int(request.form['stock'])
    price = float(request.form['price'])
    db.session.add(Product(name=name, stock=stock, price=price))
    db.session.commit()
    return redirect(url_for('product.list_products'))

@product_bp.route('/delete/<int:id>')
@login_required
def delete_product(id):
    if not current_user.is_admin:
        return "Permission denied"
    p = Product.query.get(id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('product.list_products'))
