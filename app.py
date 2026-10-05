import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-lunera-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def index():
        new_arrivals = Product.query.order_by(Product.created_at.desc()).limit(4).all()
        best_sellers = Product.query.limit(4).all()
        return render_template('index.html', new_arrivals=new_arrivals, best_sellers=best_sellers)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            user = User.query.filter_by(email=email).first()
            
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                flash('Başarıyla giriş yaptınız.', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
            else:
                flash('E-posta adresi veya şifre hatalı.', 'error')
                
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
            
        if request.method == 'POST':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            password = request.form.get('password')
            password_confirm = request.form.get('password_confirm')
            
            if not all([first_name, last_name, email, password, password_confirm]):
                flash('Lütfen tüm alanları doldurun.', 'warning')
                return redirect(url_for('register'))
                
            if password != password_confirm:
                flash('Şifreler eşleşmiyor.', 'error')
                return redirect(url_for('register'))
                
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Bu e-posta adresi zaten kullanımda.', 'error')
                return redirect(url_for('register'))
                
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password_hash=generate_password_hash(password)
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Kayıt işlemi başarılı! Lütfen giriş yapın.', 'success')
            return redirect(url_for('login'))
            
        return render_template('register.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Başarıyla çıkış yaptınız.', 'success')
        return redirect(url_for('index'))

    @app.route('/profile')
    @login_required
    def profile():
        return render_template('profile.html', user=current_user)

    @app.route('/product/<int:id>')
    def product_detail(id):
        product = Product.query.get_or_404(id)
        sizes = product.sizes.split(',') if product.sizes else []
        return render_template('product_detail.html', product=product, sizes=sizes)

    @app.route('/search')
    def search():
        query = request.args.get('q', '')
        category_id = request.args.get('category')
        sort = request.args.get('sort')
        
        products_query = Product.query
        
        if query:
            products_query = products_query.filter(Product.name.ilike(f'%{query}%') | Product.description.ilike(f'%{query}%'))
            
        if category_id:
            products_query = products_query.filter(Product.category_id == category_id)
            
        if sort == 'price_asc':
            products_query = products_query.order_by(db.func.coalesce(Product.discount_price, Product.price).asc())
        elif sort == 'price_desc':
            products_query = products_query.order_by(db.func.coalesce(Product.discount_price, Product.price).desc())
        else:
            products_query = products_query.order_by(Product.created_at.desc())
            
        products = products_query.all()
        categories = Category.query.all()
        
        return render_template('search.html', products=products, query=query, categories=categories, current_category=category_id, current_sort=sort)

    @app.route('/cart')
    @login_required
    def cart():
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        
        subtotal = 0
        for item in cart_items:
            product = Product.query.get(item.product_id)
            price = product.discount_price if product.discount_price else product.price
            subtotal += price * item.quantity
            
        shipping = 100 if subtotal > 0 and subtotal < 1500 else 0
        total = subtotal + shipping
        
        return render_template('cart.html', cart_items=cart_items, subtotal=subtotal, shipping=shipping, total=total, Product=Product)

    @app.route('/cart/add', methods=['POST'])
    @login_required
    def add_to_cart():
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity', 1))
        size = request.form.get('size')
        
        product = Product.query.get_or_404(product_id)
        
        if not size and product.sizes:
            flash('Lütfen beden seçiniz.', 'warning')
            return redirect(url_for('product_detail', id=product_id))
            
        if product.stock < quantity:
            flash('Bu ürün stokta bulunmuyor veya yetersiz stok.', 'error')
            return redirect(url_for('product_detail', id=product_id))
            
        existing_item = CartItem.query.filter_by(
            user_id=current_user.id, 
            product_id=product_id, 
            size=size
        ).first()
        
        if existing_item:
            if existing_item.quantity + quantity > product.stock:
                flash('Stok miktarından fazla ürün ekleyemezsiniz.', 'error')
            else:
                existing_item.quantity += quantity
                db.session.commit()
                flash('Ürün sepete eklendi.', 'success')
        else:
            new_item = CartItem(
                user_id=current_user.id,
                product_id=product_id,
                quantity=quantity,
                size=size,
                color=product.color
            )
            db.session.add(new_item)
            db.session.commit()
            flash('Ürün sepete eklendi.', 'success')
            
        return redirect(url_for('cart'))

    @app.route('/cart/remove/<int:id>', methods=['POST'])
    @login_required
    def remove_from_cart(id):
        item = CartItem.query.get_or_404(id)
        if item.user_id == current_user.id:
            db.session.delete(item)
            db.session.commit()
            flash('Ürün sepetten çıkarıldı.', 'success')
        return redirect(url_for('cart'))

    @app.route('/cart/update/<int:id>', methods=['POST'])
    @login_required
    def update_cart(id):
        item = CartItem.query.get_or_404(id)
        if item.user_id != current_user.id:
            return redirect(url_for('cart'))
            
        action = request.form.get('action')
        product = Product.query.get(item.product_id)
        
        if action == 'increase':
            if item.quantity < product.stock:
                item.quantity += 1
            else:
                flash('Stok limitine ulaştınız.', 'warning')
        elif action == 'decrease':
            if item.quantity > 1:
                item.quantity -= 1
        
        db.session.commit()
        return redirect(url_for('cart'))

    @app.route('/favorites')
    @login_required
    def favorites():
        favs = Favorite.query.filter_by(user_id=current_user.id).all()
        products = [Product.query.get(f.product_id) for f in favs]
        return render_template('favorites.html', products=products)

    @app.route('/favorites/toggle/<int:product_id>', methods=['POST'])
    @login_required
    def toggle_favorite(product_id):
        product = Product.query.get_or_404(product_id)
        fav = Favorite.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        
        if fav:
            db.session.delete(fav)
            db.session.commit()
            flash('Ürün favorilerden çıkarıldı.', 'success')
        else:
            new_fav = Favorite(user_id=current_user.id, product_id=product_id)
            db.session.add(new_fav)
            db.session.commit()
            flash('Ürün favorilere eklendi.', 'success')
            
        return redirect(request.referrer or url_for('index'))

    @app.route('/checkout', methods=['GET', 'POST'])
    @login_required
    def checkout():
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        if not cart_items:
            flash('Sepetiniz boş.', 'warning')
            return redirect(url_for('cart'))
            
        subtotal = 0
        for item in cart_items:
            product = Product.query.get(item.product_id)
            price = product.discount_price if product.discount_price else product.price
            subtotal += price * item.quantity
            
        shipping = 100 if subtotal > 0 and subtotal < 1500 else 0
        total = subtotal + shipping
        
        if request.method == 'POST':
            timestamp_str = str(int(datetime.now().timestamp()))[-3:]
            order_number = f"#LUN-{datetime.now().strftime('%Y%m%d')}-{current_user.id}{timestamp_str}"
            
            full_address = f"{request.form.get('address')}, {request.form.get('district')}/{request.form.get('city')} - {request.form.get('postal_code')}"
            phone = request.form.get('phone')
            
            new_order = Order(
                order_number=order_number,
                user_id=current_user.id,
                total_price=total,
                address=full_address,
                phone=phone
            )
            db.session.add(new_order)
            db.session.flush() 
            
            for item in cart_items:
                product = Product.query.get(item.product_id)
                price = product.discount_price if product.discount_price else product.price
                
                if product.stock < item.quantity:
                    db.session.rollback()
                    flash(f'{product.name} için yeterli stok yok.', 'error')
                    return redirect(url_for('cart'))
                
                product.stock -= item.quantity
                
                order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=product.id,
                    quantity=item.quantity,
                    price=price,
                    size=item.size,
                    color=item.color
                )
                db.session.add(order_item)
                db.session.delete(item)
                
            db.session.commit()
            return redirect(url_for('order_success', id=new_order.id))
            
        return render_template('checkout.html', cart_items=cart_items, subtotal=subtotal, shipping=shipping, total=total, Product=Product)

    @app.route('/order/success/<int:id>')
    @login_required
    def order_success(id):
        order = Order.query.get_or_404(id)
        if order.user_id != current_user.id:
            return redirect(url_for('index'))
        return render_template('order_success.html', order=order)

    @app.route('/orders')
    @login_required
    def orders():
        user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
        return render_template('orders.html', orders=user_orders, Product=Product)

    # --- ADMIN ROUTES ---
    def admin_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.is_admin:
                flash('Bu sayfaya erişim yetkiniz yok.', 'error')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function

    @app.route('/admin')
    @admin_required
    def admin_dashboard():
        product_count = Product.query.count()
        user_count = User.query.count()
        order_count = Order.query.count()
        
        orders = Order.query.all()
        total_sales = sum(o.total_price for o in orders)
        
        low_stock_products = Product.query.filter(Product.stock < 5).all()
        
        return render_template('admin/dashboard.html', 
                              product_count=product_count, 
                              user_count=user_count, 
                              order_count=order_count, 
                              total_sales=total_sales,
                              low_stock_products=low_stock_products)

    @app.route('/admin/products')
    @admin_required
    def admin_products():
        products = Product.query.order_by(Product.created_at.desc()).all()
        return render_template('admin/products.html', products=products)

    @app.route('/admin/products/add', methods=['GET', 'POST'])
    @admin_required
    def admin_add_product():
        categories = Category.query.all()
        if request.method == 'POST':
            name = request.form.get('name')
            description = request.form.get('description')
            price = float(request.form.get('price', 0))
            discount_price = request.form.get('discount_price')
            discount_price = float(discount_price) if discount_price else None
            category_id = request.form.get('category_id')
            sizes = request.form.get('sizes')
            color = request.form.get('color')
            stock = int(request.form.get('stock', 0))
            image = request.form.get('image')
            
            new_product = Product(
                name=name, description=description, price=price, discount_price=discount_price,
                category_id=category_id, sizes=sizes, color=color, stock=stock, image=image
            )
            db.session.add(new_product)
            db.session.commit()
            flash('Ürün başarıyla eklendi.', 'success')
            return redirect(url_for('admin_products'))
            
        return render_template('admin/add_product.html', categories=categories)

    @app.route('/admin/products/edit/<int:id>', methods=['GET', 'POST'])
    @admin_required
    def admin_edit_product(id):
        product = Product.query.get_or_404(id)
        categories = Category.query.all()
        
        if request.method == 'POST':
            product.name = request.form.get('name')
            product.description = request.form.get('description')
            product.price = float(request.form.get('price', 0))
            discount_price = request.form.get('discount_price')
            product.discount_price = float(discount_price) if discount_price else None
            product.category_id = request.form.get('category_id')
            product.sizes = request.form.get('sizes')
            product.color = request.form.get('color')
            product.stock = int(request.form.get('stock', 0))
            product.image = request.form.get('image')
            
            db.session.commit()
            flash('Ürün başarıyla güncellendi.', 'success')
            return redirect(url_for('admin_products'))
            
        return render_template('admin/edit_product.html', product=product, categories=categories)

    @app.route('/admin/products/delete/<int:id>', methods=['POST'])
    @admin_required
    def admin_delete_product(id):
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        flash('Ürün başarıyla silindi.', 'success')
        return redirect(url_for('admin_products'))

    @app.route('/admin/orders')
    @admin_required
    def admin_orders():
        orders = Order.query.order_by(Order.created_at.desc()).all()
        return render_template('admin/orders.html', orders=orders)

    @app.route('/admin/orders/status/<int:id>', methods=['POST'])
    @admin_required
    def admin_order_status(id):
        order = Order.query.get_or_404(id)
        status = request.form.get('status')
        if status:
            order.status = status
            db.session.commit()
            flash(f'Sipariş durumu güncellendi.', 'success')
        return redirect(url_for('admin_orders'))

    @app.route('/admin/users')
    @admin_required
    def admin_users():
        users = User.query.order_by(User.created_at.desc()).all()
        return render_template('admin/users.html', users=users)

    # Create tables
    with app.app_context():
        db.create_all()
        
    return app

# --- DATABASE MODELS ---

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    orders = db.relationship('Order', backref='user', lazy=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    discount_price = db.Column(db.Float, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    color = db.Column(db.String(50), nullable=True)
    sizes = db.Column(db.String(255), nullable=True) # e.g. "XS,S,M,L,XL"
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    size = db.Column(db.String(20), nullable=True)
    color = db.Column(db.String(50), nullable=True)

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Hazırlanıyor')
    address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String(20), nullable=True)
    color = db.Column(db.String(50), nullable=True)

class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    district = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.String(20), nullable=True)
    full_address = db.Column(db.Text, nullable=False)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
