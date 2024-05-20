import csv
from django.core.management.base import BaseCommand
from slugify import slugify  # Sử dụng slugify từ slugify library
from shop.models import Product, Category

class Command(BaseCommand):
    help = 'Import products from a CSV file'

    def handle(self, *args, **kwargs):
        with open('importer/products.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Kiểm tra và tạo danh mục chính nếu không có danh mục phụ
                if not row['sub_category']:
                    parent_category, created = Category.objects.get_or_create(
                        title=row['category'],
                        defaults={'slug': slugify(row['category']), 'is_sub': False}
                    )
                    category = parent_category
                else:
                    # Kiểm tra và tạo danh mục phụ nếu có
                    parent_category, created = Category.objects.get_or_create(
                        title=row['category'],
                        defaults={'slug': slugify(row['category']), 'is_sub': False}
                    )
                    sub_category, created = Category.objects.get_or_create(
                        title=row['sub_category'],
                        sub_category=parent_category,
                        defaults={'slug': slugify(row['sub_category']), 'is_sub': True}
                    )
                    category = sub_category

                # Thêm sản phẩm vào CSDL
                product, created = Product.objects.get_or_create(
                    title=row['title'],
                    defaults={
                        'category': category,
                        'image_url': row['image_url'],
                        'description': row['description'],
                        'price': row['price'],
                        'slug': slugify(row['title'])
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Added product: {row["title"]}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Product already exists: {row["title"]}'))
