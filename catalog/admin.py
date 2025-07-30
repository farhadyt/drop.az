# catalog/admin.py
from django.contrib import admin, messages
from django.db.models import Count, Sum, Q
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import csv

from .models import Category, Product

# =================================
# ADMIN MIXINS & UTILITY CLASSES
# =================================

class ExportCsvMixin:
    """
    Seçilmiş obyektləri CSV faylı olaraq ixrac etmək üçün Mixin.
    """
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Seçilmişləri CSV olaraq ixrac et"

# =================================
# CUSTOM ADMIN FILTERS
# =================================

class StockLevelFilter(admin.SimpleListFilter):
    """
    Stok səviyyəsinə görə məhsulları filtrləmək üçün xüsusi filtr.
    """
    title = 'Stok səviyyəsi'
    parameter_name = 'stock_level'

    def lookups(self, request, model_admin):
        return (
            ('in_stock', 'Kifayət qədər (>5)'),
            ('low_stock', 'Az stok (1-5)'),
            ('out_of_stock', 'Stok yoxdur (0)'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'in_stock':
            return queryset.filter(stock__gt=5)
        if self.value() == 'low_stock':
            return queryset.filter(stock__range=(1, 5))
        if self.value() == 'out_of_stock':
            return queryset.filter(stock=0)

# =================================
# CATEGORY ADMIN CONFIGURATION
# =================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin, ExportCsvMixin):
    """
    Kateqoriya modeli üçün Admin Panel konfiqurasiyası.
    """
    list_display = ['name', 'slug', 'parent', 'product_count']
    list_filter = ['parent']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']
    actions = ['export_as_csv']

    def get_queryset(self, request):
        """
        Effektivlik üçün N+1 problemini həll edir.
        """
        return super().get_queryset(request).select_related('parent').annotate(
            products_count=Count('products', filter=Q(products__available=True))
        )

    def product_count(self, obj):
        """
        Kateqoriyadakı aktiv məhsulların sayını göstərir və link verir.
        """
        count = obj.products_count
        url = reverse('admin:catalog_product_changelist') + f'?category__id__exact={obj.id}'
        return format_html('<a href="{}">{} məhsul</a>', url, count)
    product_count.short_description = 'Aktiv Məhsul Sayı'
    product_count.admin_order_field = 'products_count'


# =================================
# PRODUCT ADMIN CONFIGURATION
# =================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportCsvMixin):
    """
    Məhsul modeli üçün Admin Panel konfiqurasiyası.
    """
    list_display = [
        'get_image_thumbnail',
        'name',
        'category',
        'price',  # <-- DÜZƏLİŞ BURADADIR
        'stock',
        'get_stock_status',
        'available',
        'updated_at'
    ]
    list_filter = [
        'available',
        'category',
        StockLevelFilter,
        'created_at',
        'updated_at'
    ]
    search_fields = ['name', 'description', 'category__name', 'slug']
    list_editable = ['price', 'stock', 'available'] # <-- BU SƏTR İNDİ DÜZGÜN İŞLƏYƏCƏK
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['-created_at']
    list_per_page = 20
    date_hierarchy = 'created_at'
    actions = ['export_as_csv', 'make_available', 'make_unavailable']

    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Qiymət və Anbar', {
            'fields': ('price', 'stock', 'available')
        }),
        ('Şəkil', {
            'fields': ('image', 'get_image_preview')
        }),
        ('Sistem Məlumatları', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['get_image_preview', 'created_at', 'updated_at']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')

    def get_image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return "—"
    get_image_thumbnail.short_description = 'Şəkil'

    def get_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 5px;" />',
                obj.image.url
            )
        return 'Şəkil yüklənməyib'
    get_image_preview.short_description = 'Şəkil (Böyük)'

    def get_stock_status(self, obj):
        if obj.stock == 0:
            return format_html('<span style="color: #dc3545;">Bitib</span>')
        elif obj.stock <= 5:
            return format_html('<span style="color: #ffc107;">Az qalıb</span>')
        return format_html('<span style="color: #28a745;">Stokda var</span>')
    get_stock_status.short_description = 'Anbar Statusu'

    def make_available(self, request, queryset):
        rows_updated = queryset.update(available=True)
        self.message_user(request, f'{rows_updated} məhsul satışa çıxarıldı.', messages.SUCCESS)
    make_available.short_description = "Seçilmiş məhsulları satışa çıxart"

    def make_unavailable(self, request, queryset):
        rows_updated = queryset.update(available=False)
        self.message_user(request, f'{rows_updated} məhsul satışdan yığışdırıldı.', messages.WARNING)
    make_unavailable.short_description = "Seçilmiş məhsulları satışdan yığışdır"

# =================================
# ADMIN SITE CUSTOMIZATION
# =================================

admin.site.site_header = 'drop.az İdarəetmə Paneli'
admin.site.site_title = 'drop.az Admin'
admin.site.index_title = 'İdarəetmə Mərkəzi'