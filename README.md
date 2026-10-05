# LUNERA

LUNERA, Flask ve SQLite kullanılarak geliştirilmiş, kullanıcı ve yönetici taraflarını içeren full-stack bir e-ticaret uygulamasıdır.

Proje; ürün listeleme, ürün detayları, kullanıcı hesapları, sepet yönetimi, favoriler, stok kontrolü, sipariş oluşturma ve yönetici paneli gibi temel e-ticaret özelliklerini bir araya getirir.

## Proje Özellikleri

### Kullanıcı Tarafı

- Kullanıcı kayıt ve giriş sistemi
- Güvenli şifre hashleme
- Kullanıcı oturumu yönetimi
- Ürün listeleme
- Ürün detay sayfası
- Ürün arama
- Kategori filtreleme
- Sıralama seçenekleri
- Beden ve renk seçimi
- Stok kontrolü
- Sepete ürün ekleme
- Sepetten ürün silme
- Sepet miktarı güncelleme
- Favori ürünler
- Sipariş oluşturma
- Sipariş geçmişi
- Sipariş başarılı sayfası

### Yönetici Paneli

- Yönetici giriş sistemi
- Yönetim paneli
- Ürün ekleme
- Ürün düzenleme
- Ürün silme
- Ürün stok yönetimi
- Siparişleri görüntüleme
- Sipariş durumlarını yönetme
- Kullanıcıları görüntüleme
- Mağaza verilerini yönetme

## Kullanılan Teknolojiler

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- SQLite
- HTML5
- CSS3
- JavaScript
- Werkzeug

## Proje Yapısı

```text
lunera/
│
├── app.py
├── seed_db.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   ├── ...
│   └── ...
│
└── static/
    ├── css/
    ├── js/
    └── images/
