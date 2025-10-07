from flask import Flask, render_template
from flask_login import LoginManager
from models import db, User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Blueprint routes ---
from routes.auth import auth_bp
from routes.product import product_bp
from routes.sales import sales_bp
from routes.dashboard import dashboard_bp

app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(dashboard_bp)

# ✅ ใช้ app.app_context() แทน before_first_request
with app.app_context():
    db.create_all()
    if not User.query.first():
        from werkzeug.security import generate_password_hash
        admin = User(username="admin", password=generate_password_hash("admin123"), is_admin=True)
        db.session.add(admin)
        db.session.commit()
        print("[+] สร้างแอดมินเริ่มต้น username=admin, password=admin123")

@app.route('/')
def index():
    return render_template('pos.html')

@app.cli.command("resetdb")
def resetdb():
    """ล้างฐานข้อมูลและสร้างใหม่"""
    with app.app_context():
        db.drop_all()
        db.create_all()
        from werkzeug.security import generate_password_hash
        admin = User(username="admin", password=generate_password_hash("admin123"), is_admin=True)
        db.session.add(admin)
        db.session.commit()
        print("[+] Database ถูกรีเซ็ตแล้ว และสร้าง admin ใหม่เรียบร้อย")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=4001,debug=True)
