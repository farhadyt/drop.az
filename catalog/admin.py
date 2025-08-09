# catalog/admin.py - ENHANCED VERSION WITH PRIORITY & INLINE EDITING

from django.contrib import admin, messages
from django.db.models import Count, Sum, Q
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, path
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django import forms
import csv

from .models import Category, Product
from .widgets import IconPickerWidget

# =================================
# CATEGORY FORM WITH PRIORITY & ICON WIDGETS
# =================================

class CategoryAdminForm(forms.ModelForm):
    """
    Custom form with Professional Icon Picker Widget & Priority
    """
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'icon_class': IconPickerWidget(attrs={
                'class': 'icon-picker-field',
                'placeholder': 'FontAwesome icon seçin... (məs: fas fa-heart)'
            }),
            'icon_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'color-picker',
                'title': 'Icon rəngini seçin'
            }),
            'priority': forms.NumberInput(attrs={
                'min': '0',
                'max': '999',
                'class': 'priority-input',
                'style': 'width: 100px; text-align: center; font-weight: bold;'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Icon field help text
        self.fields['icon_class'].help_text = (
            'Professional Icon Picker istifadə edərək icon seçin. '
            '2000+ FontAwesome icon mövcuddur.'
        )
        
        # Priority field help text
        self.fields['priority'].help_text = (
            '0 = Ən yüksək priority (TOP), 1-3 = HIGH, 4-7 = MEDIUM, 8+ = LOW'
        )

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

class PriorityLevelFilter(admin.SimpleListFilter):
    """
    Priority səviyyəsinə görə filtr
    """
    title = 'Priority Səviyyəsi'
    parameter_name = 'priority_level'

    def lookups(self, request, model_admin):
        return (
            ('top', 'TOP (0)'),
            ('high', 'HIGH (1-3)'),
            ('medium', 'MEDIUM (4-7)'),
            ('low', 'LOW (8+)'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'top':
            return queryset.filter(priority=0)
        if self.value() == 'high':
            return queryset.filter(priority__range=(1, 3))
        if self.value() == 'medium':
            return queryset.filter(priority__range=(4, 7))
        if self.value() == 'low':
            return queryset.filter(priority__gte=8)

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
# CATEGORY ADMIN WITH PRIORITY
# =================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin, ExportCsvMixin):
    """
    Professional Category Admin with Priority & Visual Icon Picker
    """
    form = CategoryAdminForm
    
    list_display = ['get_icon_display', 'name', 'slug', 'parent', 'priority', 'get_priority_display', 'product_count', 'get_icon_info']
    list_filter = ['parent', PriorityLevelFilter]
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['priority', 'name']  # Priority-yə görə sıralama
    actions = ['export_as_csv', 'set_high_priority', 'set_medium_priority', 'set_low_priority']
    list_editable = ['priority']  # Priority-ni siyahıda dəyişmək

    fieldsets = (
        ('📋 Əsas Məlumatlar', {
            'fields': ('name', 'slug', 'parent'),
            'classes': ('wide',)
        }),
        ('🎯 Priority & Sıralama', {
            'fields': ('priority',),
            'classes': ('wide', 'priority-section'),
            'description': '''
                <div class="priority-help-section">
                    <h3>🎯 Priority Sistemi</h3>
                    <ul>
                        <li><strong>0</strong> = TOP priority (header-də ən yuxarıda)</li>
                        <li><strong>1-3</strong> = HIGH priority (önəmli kateqoriyalar)</li>
                        <li><strong>4-7</strong> = MEDIUM priority (normal kateqoriyalar)</li>
                        <li><strong>8+</strong> = LOW priority (alt səviyyə kateqoriyalar)</li>
                    </ul>
                </div>
            '''
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

    def get_priority_display(self, obj):
        """Priority gösterimi rəng ilə"""
        level = obj.get_priority_level()
        color = obj.get_priority_color()
        
        # Quick priority change buttons
        buttons_html = f'''
            <div style="display: flex; align-items: center; gap: 5px;">
                <div style="text-align: center;">
                    <div style="background: {color}; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 11px; margin-bottom: 2px;">{level}</div>
                    <div style="font-size: 18px; font-weight: bold; color: {color};">{obj.priority}</div>
                </div>
                <div class="priority-buttons" style="margin-left: 8px;">
                    <button type="button" onclick="setPriority({obj.id}, 0)" style="background: #6f42c1; color: white; border: none; padding: 2px 6px; border-radius: 3px; font-size: 10px; cursor: pointer; margin: 1px;" title="TOP">0</button>
                    <button type="button" onclick="setPriority({obj.id}, 1)" style="background: #28a745; color: white; border: none; padding: 2px 6px; border-radius: 3px; font-size: 10px; cursor: pointer; margin: 1px;" title="HIGH">H</button>
                    <button type="button" onclick="setPriority({obj.id}, 5)" style="background: #ffc107; color: black; border: none; padding: 2px 6px; border-radius: 3px; font-size: 10px; cursor: pointer; margin: 1px;" title="MID">M</button>
                    <button type="button" onclick="setPriority({obj.id}, 10)" style="background: #dc3545; color: white; border: none; padding: 2px 6px; border-radius: 3px; font-size: 10px; cursor: pointer; margin: 1px;" title="LOW">L</button>
                </div>
            </div>
        '''
        
        return format_html(buttons_html)
    
    get_priority_display.short_description = '🎯 Priority & Quick Actions'
    get_priority_display.allow_tags = True

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

    # Bulk actions for priority
    def set_high_priority(self, request, queryset):
        queryset.update(priority=1)
        self.message_user(request, f'{queryset.count()} kateqoriyanın priority-si HIGH təyin edildi.', messages.SUCCESS)
    set_high_priority.short_description = "Priority-ni HIGH (1) et"

    def set_medium_priority(self, request, queryset):
        queryset.update(priority=5)
        self.message_user(request, f'{queryset.count()} kateqoriyanın priority-si MEDIUM təyin edildi.', messages.SUCCESS)
    set_medium_priority.short_description = "Priority-ni MEDIUM (5) et"

    def set_low_priority(self, request, queryset):
        queryset.update(priority=10)
        self.message_user(request, f'{queryset.count()} kateqoriyanın priority-si LOW təyin edildi.', messages.SUCCESS)
    set_low_priority.short_description = "Priority-ni LOW (10) et"

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css',
                'admin/css/icon-admin-enhanced.css',
            )
        }
        js = (
            'admin/js/icon-picker-integration.js',
            'admin/js/priority-manager.js',
        )

# =================================
# PRODUCT ADMIN (Enhanced with better editing)
# =================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportCsvMixin):
    """
    Məhsul modeli üçün Enhanced Admin Panel konfiqurasiyası.
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
    list_editable = ['price', 'stock', 'available']  # İnline editing aktiv
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['-created_at']
    list_per_page = 20
    date_hierarchy = 'created_at'
    actions = ['export_as_csv', 'make_available', 'make_unavailable', 'duplicate_products']

    fieldsets = (
        ('📋 Əsas Məlumatlar', {
            'fields': ('name', 'slug', 'category', 'description'),
            'classes': ('wide',)
        }),
        ('💰 Qiymət və Anbar', {
            'fields': ('price', 'stock', 'available'),
            'classes': ('wide',)
        }),
        ('🖼️ Şəkil', {
            'fields': ('image', 'get_image_preview'),
            'classes': ('wide',)
        }),
        ('📊 Sistem Məlumatları', {
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

    def duplicate_products(self, request, queryset):
        """Məhsulları kopyalama action-u"""
        duplicated = 0
        for product in queryset:
            product.pk = None
            product.name = f"{product.name} (Copy)"
            product.slug = f"{product.slug}-copy-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            product.save()
            duplicated += 1
        self.message_user(request, f'{duplicated} məhsul uğurla kopyalandı.', messages.SUCCESS)
    duplicate_products.short_description = "Seçilmiş məhsulları kopyala"

# =================================
# ADMIN SITE CUSTOMIZATION
# =================================

admin.site.site_header = '🛒 drop.az Professional Admin'
admin.site.site_title = 'drop.az Admin'
admin.site.index_title = '📊 Professional İdarəetmə Paneli'