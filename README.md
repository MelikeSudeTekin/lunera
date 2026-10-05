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
```

## Kurulum

Projeyi bilgisayarınıza klonlayın:

```bash
git clone https://github.com/MelikeSudeTekin/lunera.git
```

Proje klasörüne girin:

```bash
cd lunera
```

Sanal ortam oluşturun:

```bash
python -m venv venv
```

Sanal ortamı Windows üzerinde aktifleştirin:

```bash
venv\Scripts\activate
```

Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

Veritabanını ve başlangıç verilerini oluşturun:

```bash
python seed_db.py
```

Uygulamayı çalıştırın:

```bash
python app.py
```

Ardından tarayıcıdan aşağıdaki adrese gidin:

```text
http://127.0.0.1:5000
```

## Veritabanı

LUNERA, SQLite veritabanı kullanmaktadır.

Yerel veritabanı dosyaları ve `instance/` klasörü `.gitignore` içerisinde tutulduğu için GitHub repository'sine dahil edilmez.

## Güvenlik

Projede kullanıcı şifreleri düz metin olarak saklanmaz. Şifre işlemleri Werkzeug üzerinden hashleme kullanılarak gerçekleştirilir.

Ayrıca yerel veritabanı dosyaları, sanal ortam klasörleri ve Python cache dosyaları Git repository'sinden hariç tutulmuştur.

## Geliştirme Alanları

Projenin ilerleyen aşamalarında aşağıdaki özelliklerin eklenmesi planlanabilir:

- Ödeme sistemi entegrasyonu
- E-posta bildirimleri
- Gelişmiş ürün filtreleme
- Ürün değerlendirme ve yorum sistemi
- Daha gelişmiş yönetici istatistikleri
- Görsel ürün yönetiminin geliştirilmesi
- REST API desteği
- Daha gelişmiş mobil responsive tasarım

## Proje Durumu
Aktif geliştirme aşamasındadır.
LUNERA, gerçek bir e-ticaret uygulamasının temel kullanıcı, ürün, sepet, sipariş ve yönetim süreçlerini öğrenmek ve uygulamak amacıyla geliştirilmiştir.

## Geliştirici
**Melike Sude Tekin**
Yapay Zeka Operatörlüğü öğrencisi.

GitHub:  
https://github.com/MelikeSudeTekin
## Lisans

Bu proje eğitim ve portföy amaçlı geliştirilmiştir.
