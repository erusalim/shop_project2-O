import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalog.models import Category, Product
from django.utils.text import slugify

# Очистить старые данные
Product.objects.all().delete()

# Получить существующие категории
categories = {cat.slug: cat for cat in Category.objects.all()}

# Товары для процессоров
if 'processors' in categories:
    products = [
        ('Intel Core i9-13900K', 'Intel Core i9-13900K', 50000, 'Флагманский процессор Intel для экстремальной производительности', 3),
        ('AMD Ryzen 9 7950X', 'AMD Ryzen 9 7950X', 48000, 'Топовый процессор AMD с 16 ядрами', 2),
        ('Intel Core i5-13600K', 'Intel Core i5-13600K', 25000, 'Отличный баланс цены и производительности', 8),
        ('AMD Ryzen 5 7600X', 'AMD Ryzen 5 7600X', 22000, 'Мощный 6-ядерный процессор', 5),
        ('Intel Core i3-13100', 'Intel Core i3-13100', 8000, 'Бюджетный вариант для офиса', 0),  # stock=0
    ]
    for name, slug_base, price, desc, stock in products:
        Product.objects.create(
            name=name,
            slug=slugify(slug_base),
            price=price,
            description=desc,
            stock=stock,
            category=categories['processors'],
            is_active=True
        )

# Товары для видеокарт
if 'graphics-cards' in categories:
    products = [
        ('NVIDIA RTX 4090', 'NVIDIA RTX 4090', 150000, 'Мощнейшая видеокарта для игр и 3D', 1),
        ('AMD RX 7900 XTX', 'AMD RX 7900 XTX', 95000, 'Топовая видеокарта AMD', 2),
        ('NVIDIA RTX 4070 Ti', 'NVIDIA RTX 4070 Ti', 70000, 'Отличная видеокарта для гейминга', 4),
        ('NVIDIA RTX 4060', 'NVIDIA RTX 4060', 30000, 'Компактная видеокарта для 1080p', 0),  # stock=0
        ('Intel Arc A770', 'Intel Arc A770', 28000, 'Нвая видеокарта от Intel с DLSS поддержкой', 3),
    ]
    for name, slug_base, price, desc, stock in products:
        Product.objects.create(
            name=name,
            slug=slugify(slug_base),
            price=price,
            description=desc,
            stock=stock,
            category=categories['graphics-cards'],
            is_active=True
        )

# Товары для материнских плат
if 'motherboards' in categories:
    products = [
        ('ASUS ROG MAXIMUS Z790', 'ASUS ROG MAXIMUS Z790', 45000, 'Премиум материнская плата для Socket 1700', 2),
        ('MSI MEG Z790 GODLIKE', 'MSI MEG Z790 GODLIKE', 50000, 'Легендарная материнская плата', 1),
        ('Gigabyte Z790 AORUS Master', 'Gigabyte Z790 AORUS Master', 35000, 'Отличная плата для Z790', 3),
        ('ASUS TUF Gaming B850M-Plus', 'ASUS TUF Gaming B850M-Plus', 15000, 'Бюджетная AM5 плата', 5),
        ('MSI B450 Tomahawk Max', 'MSI B450 Tomahawk Max', 8000, 'Легендарная плата (снята с производства)', 0),  # stock=0
    ]
    for name, slug_base, price, desc, stock in products:
        Product.objects.create(
            name=name,
            slug=slugify(slug_base),
            price=price,
            description=desc,
            stock=stock,
            category=categories['motherboards'],
            is_active=True
        )

# Товары для оперативной памяти
if 'ram' in categories:
    products = [
        ('Kingston Fury Beast DDR5 32GB', 'Kingston Fury Beast DDR5 32GB', 20000, 'Быстрая память DDR5 5600Mhz', 6),
        ('Corsair Vengeance RGB 32GB DDR4', 'Corsair Vengeance RGB 32GB DDR4', 15000, 'Красивая и быстрая память', 8),
        ('G.Skill Trident Z5 64GB', 'G.Skill Trident Z5 64GB', 35000, 'Профессиональная память DDR5', 3),
        ('ADATA XPG Spectrix 16GB', 'ADATA XPG Spectrix 16GB', 8000, 'RGB память средней ценовой категории', 10),
        ('SK Hynix HMA851U6ABR6N-UH', 'SK Hynix HMA851U6ABR6N-UH', 3000, 'Серверная память (редкость)', 0),  # stock=0
    ]
    for name, slug_base, price, desc, stock in products:
        Product.objects.create(
            name=name,
            slug=slugify(slug_base),
            price=price,
            description=desc,
            stock=stock,
            category=categories['ram'],
            is_active=True
        )

# Товары для накопителей
if 'storage' in categories:
    products = [
        ('Samsung 990 Pro 2TB', 'Samsung 990 Pro 2TB', 25000, 'Сверхбыстрый NVMe SSD для PCIe 4.0', 4),
        ('WD Black SN850X 1TB', 'WD Black SN850X 1TB', 10000, 'Отличный игровой SSD', 8),
        ('Seagate FireCuda 530 500GB', 'Seagate FireCuda 530 500GB', 6000, 'Бюджетный NVMe с хорошей скоростью', 5),
        ('SK Hynix Gold P41 1TB', 'SK Hynix Gold P41 1TB', 8000, 'Надежный SSD с хорошим соотношением цены', 6),
        ('Intel 670p 512GB', 'Intel 670p 512GB', 4000, 'Старый но все еще быстрый SSД (снят с производства)', 0),  # stock=0
    ]
    for name, slug_base, price, desc, stock in products:
        Product.objects.create(
            name=name,
            slug=slugify(slug_base),
            price=price,
            description=desc,
            stock=stock,
            category=categories['storage'],
            is_active=True
        )

print(f'✓ Добавлено {Product.objects.count()} товаров в {Category.objects.count()} категориях')
