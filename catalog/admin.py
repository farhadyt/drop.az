# catalog/admin.py - Widget ilə update edilmiş versiya

from django.contrib import admin, messages
from django.db.models import Count, Sum, Q
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django import forms
import csv

from .models import Category, Product
from .widgets import IconPickerWidget  # Yeni widget import

# =================================
# CATEGORY FORM WITH ICON WIDGET
# =================================

class CategoryAdminForm(forms.ModelForm):
    """
    Custom form with Professional Icon Picker Widget
    """
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'icon_class': IconPickerWidget(attrs={
                'class': 'icon-picker-field',
                'placeholder': 'FontAwesome icon seçin... (məs: fas fa-heart)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Icon field help text
        self.fields['icon_class'].help_text = (
            'Professional Icon Picker istifadə edərək icon seçin. '
            '2000+ FontAwesome icon mövcuddur.'
        )
        
        # Icon color field styling  
        if 'icon_color' in self.fields:
            self.fields['icon_color'].widget.attrs.update({
                'type': 'color',
                'class': 'color-picker',
                'title': 'Icon rəngini seçin'
            })

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
# CATEGORY ADMIN WITH PROFESSIONAL WIDGET
# =================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin, ExportCsvMixin):
    """
    Professional Category Admin with Visual Icon Picker
    """
    form = CategoryAdminForm  # Custom form with widget
    
    list_display = ['get_icon_display', 'name', 'slug', 'parent', 'product_count', 'get_icon_info']
    list_filter = ['parent']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']
    actions = ['export_as_csv']

    fieldsets = (
        ('📋 Əsas Məlumatlar', {
            'fields': ('name', 'slug', 'parent'),
            'classes': ('wide',)
        }),
        ('🎨 Professional Icon Picker', {
            'fields': ('icon_class', 'icon_color', 'icon_image'),
            'classes': ('wide', 'icon-fieldset'),
            'description': '''
                <div class="icon-help-section">
                    <h3>🎯 Professional Icon Picker</h3>
                    <ul>
                        <li><strong>Icon Seç düyməsini</strong> basaraq 2000+ professional icon-dan seçin</li>
                        <li><strong>Axtarış</strong> və <strong>filter</strong> funksiyalarından istifadə edin</li>
                        <li>Yaxud <strong>Custom Icon</strong> yükləyin</li>
                        <li><strong>Rəng seçici</strong> ilə icon rəngini dəyişin</li>
                    </ul>
                </div>
            '''
        }),
        ('📊 Önizləmə', {
            'fields': ('get_icon_preview_detailed',),
            'classes': ('collapse', 'wide')
        }),
    )
    readonly_fields = ['get_icon_preview_detailed']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parent').annotate(
            products_count=Count('products', filter=Q(products__available=True))
        )

    def get_icon_display(self, obj):
        """Enhanced icon display for list view"""
        if obj.icon_image:
            return format_html(
                '<div class="admin-icon-display">'
                '<img src="{}" alt="{}" class="icon-thumbnail">'
                '<span class="icon-type">Custom</span>'
                '</div>',
                obj.icon_image.url, obj.name
            )
        elif obj.icon_class:
            color_style = f'color: {obj.icon_color};' if obj.icon_color else 'color: #007bff;'
            return format_html(
                '<div class="admin-icon-display">'
                '<i class="{}" style="font-size: 24px; {}"></i>'
                '<span class="icon-type">FA</span>'
                '</div>',
                obj.icon_class, color_style
            )
        return format_html(
            '<div class="admin-icon-display">'
            '<i class="fas fa-folder" style="color: #6c757d; font-size: 24px;"></i>'
            '<span class="icon-type">Default</span>'
            '</div>'
        )
    
    get_icon_display.short_description = '🎨 Icon'
    get_icon_display.allow_tags = True

    def get_icon_info(self, obj):
        """Detailed icon information for list view"""
        if obj.icon_image:
            return format_html('<span class="icon-info custom">🖼️ Custom Image</span>')
        elif obj.icon_class:
            return format_html(
                '<span class="icon-info fontawesome" title="{}">'
                '✨ {} <small>({})</small>'
                '</span>', 
                obj.icon_class, 
                obj.icon_class.replace('fas fa-', '').replace('far fa-', '').replace('fab fa-', '').title(),
                obj.icon_color or '#007bff'
            )
        return format_html('<span class="icon-info default">📁 Default</span>')
    
    get_icon_info.short_description = 'ℹ️ Icon Info'
    get_icon_info.allow_tags = True

    def get_icon_preview_detailed(self, obj):
        """Detailed preview in admin form"""
        if obj.icon_image:
            return format_html(
                '<div class="detailed-icon-preview">'
                '<div class="preview-section">'
                '<h4>🖼️ Custom Icon Preview</h4>'
                '<div class="preview-box custom">'
                '<img src="{}" alt="{}" class="large-icon-preview">'
                '</div>'
                '<p class="preview-info">Custom uploaded icon aktiv</p>'
                '</div>'
                '</div>',
                obj.icon_image.url, obj.name
            )
        elif obj.icon_class:
            color_style = f'color: {obj.icon_color};' if obj.icon_color else 'color: #007bff;'
            return format_html(
                '<div class="detailed-icon-preview">'
                '<div class="preview-section">'
                '<h4>✨ FontAwesome Icon Preview</h4>'
                '<div class="preview-box fontawesome">'
                '<i class="{}" style="font-size: 64px; {}"></i>'
                '</div>'
                '<div class="preview-details">'
                '<p><strong>Class:</strong> <code>{}</code></p>'
                '<p><strong>Rəng:</strong> <span style="background: {}; width: 20px; height: 20px; display: inline-block; border-radius: 3px; vertical-align: middle; margin-right: 5px;"></span> {}</p>'
                '</div>'
                '</div>'
                '</div>',
                obj.icon_class, color_style, obj.icon_class, 
                obj.icon_color or '#007bff', obj.icon_color or '#007bff'
            )
        return format_html(
            '<div class="detailed-icon-preview">'
            '<div class="preview-section">'
            '<h4>📁 Default Icon</h4>'
            '<div class="preview-box default">'
            '<i class="fas fa-folder" style="font-size: 64px; color: #6c757d;"></i>'
            '</div>'
            '<p class="preview-info">Heç bir custom icon seçilməyib</p>'
            '</div>'
            '</div>'
        )
    
    get_icon_preview_detailed.short_description = '🔍 Detailed Preview'
    get_icon_preview_detailed.allow_tags = True

    def product_count(self, obj):
        count = obj.products_count
        url = reverse('admin:catalog_product_changelist') + f'?category__id__exact={obj.id}'
        return format_html('<a href="{}" class="product-count-link">{} məhsul</a>', url, count)
    product_count.short_description = '📦 Məhsullar'
    product_count.admin_order_field = 'products_count'

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css',
                'admin/css/icon-admin-enhanced.css',
            )
        }
        js = (
            'admin/js/icon-picker-integration.js',
        )

# =================================
# PRODUCT ADMIN (Unchanged)
# =================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportCsvMixin):
    """
    Məhsul modeli üçün Admin Panel konfiqurasiyası.
    """
    list_display = [
        'get_image_thumbnail',
        'name',
        'get_category_with_icon',
        'price',
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
    list_editable = ['price', 'stock', 'available']
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

    def get_category_with_icon(self, obj):
        """Display category with its icon"""
        if obj.category:
            if obj.category.icon_image:
                return format_html(
                    '<div class="category-with-icon">'
                    '<img src="{}" alt="{}" class="category-mini-icon"> {}'
                    '</div>',
                    obj.category.icon_image.url, obj.category.name, obj.category.name
                )
            elif obj.category.icon_class:
                color_style = f'color: {obj.category.icon_color};' if obj.category.icon_color else 'color: #007bff;'
                return format_html(
                    '<div class="category-with-icon">'
                    '<i class="{}" style="{}"></i> {}'
                    '</div>',
                    obj.category.icon_class, color_style, obj.category.name
                )
        return obj.category.name if obj.category else "—"
    
    get_category_with_icon.short_description = '📂 Kateqoriya'
    get_category_with_icon.admin_order_field = 'category__name'
    get_category_with_icon.allow_tags = True

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
            return format_html('<span class="stock-status out">❌ Bitib</span>')
        elif obj.stock <= 5:
            return format_html('<span class="stock-status low">⚠️ Az qalıb</span>')
        return format_html('<span class="stock-status available">✅ Stokda var</span>')
    get_stock_status.short_description = 'Anbar Statusu'

    def make_available(self, request, queryset):
        rows_updated = queryset.update(available=True)
        self.message_user(request, f'{rows_updated} məhsul satışa çıxarıldı.', messages.SUCCESS)
    make_available.short_description = "Seçilmiş məhsulları satışa çıxart"

    def make_unavailable(self, request, queryset):
        rows_updated = queryset.update(available=False)
        self.message_user(request, f'{rows_updated} məhsul satışdan yığışdır.', messages.WARNING)
    make_unavailable.short_description = "Seçilmiş məhsulları satışdan yığışdır"

# =================================
# ADMIN SITE CUSTOMIZATION
# =================================

admin.site.site_header = '🛒 drop.az Professional Admin'
admin.site.site_title = 'drop.az Admin'
admin.site.index_title = '📊 Professional İdarəetmə Paneli'