from django.urls import path
from . import views
app_name = "shop"
urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('add_to_favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', views.favorites, name='favorites'),
    path('search/', views.search, name='search'),
    path('filter_by_category/<slug:slug>/', views.filter_by_category, name='filter_by_category'),
    path('add_comment/<slug:slug>/', views.add_comment, name='add_comment'),  # Thêm đường dẫn cho view add_comment
]