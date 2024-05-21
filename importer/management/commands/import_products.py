import csv
from django.core.management.base import BaseCommand
from slugify import slugify
from shop.models import Product, Category

class Command(BaseCommand):
    help = 'Import products from a CSV file'

    def handle(self, *args, **kwargs):
        with open('importer/data_smartphone.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Xử lý danh mục chính
                parent_category_slug = slugify(row['category'])
                parent_category, created = Category.objects.get_or_create(
                    title=row['category'],
                    defaults={'slug': self.get_unique_slug(parent_category_slug, Category), 'is_sub': False}
                )

                if not row['sub_category']:
                    category = parent_category
                else:
                    # Xử lý danh mục phụ
                    sub_category_slug = slugify(row['sub_category'])
                    sub_category, created = Category.objects.get_or_create(
                        title=row['sub_category'],
                        defaults={
                            'slug': self.get_unique_slug(sub_category_slug, Category),
                            'sub_category': parent_category,
                            'is_sub': True
                        }
                    )
                    category = sub_category

                # Chuyển đổi giá sang định dạng số
                price_str = row['price'].replace('.', '')
                price = float(price_str)

                # Tạo slug duy nhất cho sản phẩm
                product_slug = slugify(row['title'])
                product_slug = self.get_unique_slug(product_slug, Product)

                # Thêm sản phẩm vào CSDL
                product, created = Product.objects.get_or_create(
                    title=row['title'],
                    defaults={
                        'category': category,
                        'image_url': row['image_url'],
                        'description': row['description'],
                        'price': price,
                        'slug': product_slug
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Added product: {row["title"]}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Product already exists: {row["title"]}'))

    def get_unique_slug(self, base_slug, model_class):
        slug = base_slug
        count = 1
        while model_class.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1
        return slug
