from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models import db, Product, Sale, SaleItem

sales_bp = Blueprint('sales', __name__, url_prefix='/sales')

@sales_bp.route('/', methods=['GET', 'POST'])
@login_required
def pos():
    products = Product.query.all()

    if request.method == 'POST':
        cart = request.form.getlist('product_id')
        quantities = request.form.getlist('quantity')
        total = 0

        # สร้าง Sale
        sale = Sale(user_id=current_user.id, total=0)
        db.session.add(sale)
        db.session.commit()

        # สร้าง SaleItem
        for pid, qty in zip(cart, quantities):
            product = Product.query.get(int(pid))
            q = int(qty)
            subtotal = product.price * q
            product.stock -= q
            db.session.add(SaleItem(
                sale_id=sale.id,
                product_id=product.id,
                quantity=q,
                subtotal=subtotal
            ))
            total += subtotal

        sale.total = total
        db.session.commit()

        # ดึง SaleItem เพื่อแสดงใบเสร็จ
        items = SaleItem.query.filter_by(sale_id=sale.id).all()
        return render_template('receipt.html', sale=sale, items=items)

    return render_template('pos.html', products=products)
