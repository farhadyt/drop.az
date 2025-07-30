from django.contrib import admin
from .models import Category, Product

# Modelimizi admin panelində daha yaxşı idarə etmək üçün xüsusi class-lar yaradırıq
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    # "slug" sahəsini "name" sahəsini yazarkən avtomatik doldurur
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available', 'created_at']
    # Siyahıdakı məlumatları birbaşa dəyişmək üçün imkan yaradır
    list_editable = ['price', 'stock', 'available']
    # Sağ tərəfdə filterləmə paneli əlavə edir
    list_filter = ['available', 'created_at', 'category']
    prepopulated_fields = {'slug': ('name',)}