from django.core.management.base import BaseCommand
import pandas as pd
from shop.models import Product, Category  # Đảm bảo đây là đường dẫn đúng

class Command(BaseCommand):
    help = 'Import products from a CSV file into the database.'

    def handle(self, *args, **options):
        file_path = r'C:\Users\pcduc\Downloads\onlineshop\online-shop\importer\product.csv'
        self.stdout.write("Starting import...")
        self.import_products(file_path)
        self.stdout.write(self.style.SUCCESS('Successfully imported all products.'))

    def import_products(self, file_path):
        data = pd.read_csv(file_path)
        for index, row in data.iterrows():
            category, _ = Category.objects.get_or_create(title=row['category'])
            try:
                product, created = Product.objects.get_or_create(
                    title=row['title'],
                    price=row['price'],
                    category=category,  # Sử dụng đối tượng Category
                    image=row['image_url']  # Đảm bảo bạn xử lý trường image phù hợp
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Imported {product.title}'))
                else:
                    self.stdout.write(f'Product {product.title} already exists.')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error importing {row["title"]}: {str(e)}'))
