# catalog/models.py - FINAL VERSION

from django.db import models

class Category(models.Model):
    """Məhsul kateqoriyalarını təmsil edən model."""
    
    # Mövcud field-lər  
    name = models.CharField(max_length=200, verbose_name="Kateqoriyanın adı")
    slug = models.SlugField(max_length=200, unique=True, help_text="Link üçün istifadə olunacaq unikal ad (məs: elektronika-mehsullari)")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name="Üst Kateqoriya")
    
    # YENİ ICON FIELD-LƏR
    icon_class = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="Icon Class",
        help_text="FontAwesome icon class (məs: fas fa-heart, fas fa-laptop, fas fa-tshirt)"
    )
    
    icon_image = models.ImageField(
        upload_to='category_icons/', 
        blank=True, 
        null=True,
        verbose_name="Custom Icon Şəkil",
        help_text="32x32 və ya 64x64 ölçülü PNG/SVG icon yükləyin"
    )
    
    icon_color = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        default="#007bff",
        verbose_name="Icon Rəngi",
        help_text="Hex rəng kodu daxil edin (məs: #ff0000 qırmızı üçün)"
    )

    class Meta:
        verbose_name = "Kateqoriya"
        verbose_name_plural = "Kateqoriyalar"

    def __str__(self):
        return self.name

    def get_icon_html(self):
        """Icon-u HTML olaraq qaytarır - Admin və frontend üçün"""
        if self.icon_image:
            return f'<img src="{self.icon_image.url}" style="width: 24px; height: 24px; object-fit: cover; border-radius: 3px;" alt="{self.name}">'
        elif self.icon_class:
            color_style = f'color: {self.icon_color};' if self.icon_color else 'color: #007bff;'
            return f'<i class="{self.icon_class}" style="font-size: 18px; {color_style}"></i>'
        return '<i class="fas fa-folder" style="color: #6c757d; font-size: 18px;"></i>'

class Product(models.Model):
    """Məhsulları təmsil edən model."""
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="Kateqoriya")
    name = models.CharField(max_length=200, verbose_name="Məhsulun adı")
    slug = models.SlugField(max_length=200, unique=True, help_text="Link üçün istifadə olunacaq unikal ad")
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, verbose_name="Şəkil")
    description = models.TextField(blank=True, verbose_name="Təsviri")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Qiymət (AZN)")
    stock = models.PositiveIntegerField(verbose_name="Anbardakı say")
    available = models.BooleanField(default=True, verbose_name="Satışda mövcuddur?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma tarixi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə tarixi")

    class Meta:
        verbose_name = "Məhsul"
        verbose_name_plural = "Məhsullar"
        ordering = ['-created_at']

    def __str__(self):
        return self.name