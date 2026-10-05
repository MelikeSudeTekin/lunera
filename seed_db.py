import os
from app import create_app, db, Category, Product, User

app = create_app()

def seed_database():
    with app.app_context():
        # Veritabanını sıfırla ve yeniden oluştur (Demo için)
        db.drop_all()
        db.create_all()

        from werkzeug.security import generate_password_hash
        admin_user = User(
            first_name="Admin",
            last_name="Lunera",
            email="admin@lunera.com",
            password=generate_password_hash("Admin123!"),
            is_admin=True
        )
        db.session.add(admin_user)

        # Kategoriler
        categories = [
            Category(name='Kadın'),
            Category(name='Erkek'),
            Category(name='Çocuk'),
            Category(name='Ayakkabı'),
            Category(name='Çanta'),
            Category(name='Aksesuar')
        ]
        db.session.add_all(categories)
        db.session.commit()

        # Ürünler
        products = [
            Product(
                name='Oversize Basic T-Shirt',
                description='Yüksek kaliteli pamuklu oversize t-shirt. Günlük kullanım için ideal.',
                price=799.0,
                discount_price=639.0,
                category_id=2, # Erkek
                image='https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                color='Beyaz',
                sizes='XS,S,M,L,XL',
                stock=50
            ),
            Product(
                name='Premium Hoodie',
                description='Soğuk havalar için mükemmel, içi polar premium kapüşonlu sweatshirt.',
                price=1299.0,
                discount_price=None,
                category_id=2, # Erkek
                image='https://images.unsplash.com/photo-1556821840-3a63f95609a7?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                color='Siyah',
                sizes='S,M,L,XL,XXL',
                stock=30
            ),
            Product(
                name='Wide Leg Jeans',
                description='Modern kesim, yüksek bel wide leg kadın kot pantolon.',
                price=1499.0,
                discount_price=1199.0,
                category_id=1, # Kadın
                image='https://images.unsplash.com/photo-1541099649105-f69ad21f3246?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                color='Mavi',
                sizes='XS,S,M,L',
                stock=20
            ),
            Product(
                name='Basic Sweatshirt',
                description='Her dolapta olması gereken rahat ve şık basic sweatshirt.',
                price=899.0,
                discount_price=None,
                category_id=1, # Kadın
                image='https://images.unsplash.com/photo-1554568218-0f1715e72254?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                color='Bej',
                sizes='XS,S,M',
                stock=0 # Tükendi test için
            ),
            Product(
                name='Classic Sneaker',
                description='Hem spor hem günlük kullanıma uygun klasik beyaz sneaker.',
                price=2199.0,
                discount_price=1899.0,
                category_id=4, # Ayakkabı
                image='https://images.unsplash.com/photo-1549298916-b41d501d3772?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                color='Beyaz',
                sizes='38,39,40,41,42,43,44',
                stock=15
            ),
            Product(
                name='Leather Bag',
                description='Hakiki deri, geniş iç hacimli omuz çantası.',
                price=3499.0,
                discount_price=2999.0,
                category_id=5, # Çanta
                image='https://images.unsplash.com/photo-1584916201218-f4242ceb4809?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                color='Kahverengi',
                sizes='Standart',
                stock=5
            ),
            Product(
                name='Denim Jacket',
                description='Vintage görünümlü klasik kot ceket.',
                price=1899.0,
                discount_price=None,
                category_id=2, # Erkek
                image='https://images.unsplash.com/photo-1495105787522-5334e3ffa0ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                color='Mavi',
                sizes='S,M,L,XL',
                stock=25
            ),
            Product(
                name='Basic Cap',
                description='Logo detaylı, ayarlanabilir spor şapka.',
                price=399.0,
                discount_price=299.0,
                category_id=6, # Aksesuar
                image='https://images.unsplash.com/photo-1588850561407-ed78c282e89b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                color='Siyah',
                sizes='Standart',
                stock=40
            )
        ]
        
        db.session.add_all(products)
        db.session.commit()
        print("Veritabanı başarıyla demo verilerle dolduruldu!")

if __name__ == '__main__':
    seed_database()
