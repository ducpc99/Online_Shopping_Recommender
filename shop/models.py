from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

class Category(models.Model):
    title = models.CharField(max_length=200)
    sub_category = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        related_name='sub_categories', null=True, blank=True
    )
    is_sub = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:200]  # Giới hạn độ dài của slug
        # Ensure the slug is unique
        original_slug = self.slug
        queryset = Category.objects.all()
        next_num = 1
        while queryset.filter(slug=self.slug).exists():
            self.slug = f"{original_slug[:190]}-{next_num}"  # Đảm bảo slug vẫn trong giới hạn
            next_num += 1
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # Cho phép trường này trống
    image_url = models.URLField(null=True, blank=True)  # Đường dẫn URL cho hình ảnh bên ngoài
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True)  # Giới hạn độ dài của slug

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:200]  # Giới hạn độ dài của slug
        # Ensure the slug is unique
        original_slug = self.slug
        queryset = Product.objects.all()
        next_num = 1
        while queryset.filter(slug=self.slug).exists():
            self.slug = f"{original_slug[:190]}-{next_num}"  # Đảm bảo slug vẫn trong giới hạn
            next_num += 1
        super().save(*args, **kwargs)
