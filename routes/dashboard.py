from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Sale

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def dashboard():
    if not current_user.is_admin:
        return "Permission denied"
    sales = Sale.query.all()
    total = sum(s.total for s in sales)
    return render_template('dashboard.html', total=total, sales=sales)
