# catalog/models.py - ENHANCED VERSION WITH PRIORITY

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    """Məhsul kateqoriyalarını təmsil edən model."""
    
    # Əsas field-lər  
    name = models.CharField(max_length=200, verbose_name="Kateqoriyanın adı")
    slug = models.SlugField(max_length=200, unique=True, help_text="Link üçün istifadə olunacaq unikal ad (məs: elektronika-mehsullari)")
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children', 
        verbose_name="Üst Kateqoriya"
    )
    
    # YENİ PRIORITY FIELD
    priority = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(999)],
        verbose_name="Priority (Sıra)",
        help_text="0 = ən yüksək priority, böyük rəqəm = aşağı priority. Header-də bu sıra ilə göstəriləcək."
    )
    
    # Icon field-ləri
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
        ordering = ['priority', 'name']  # Priority-yə görə sıralama

    def __str__(self):
        return f"{self.name} (Priority: {self.priority})"

    def get_icon_html(self):
        """Icon-u HTML olaraq qaytarır - Admin və frontend üçün"""
        if self.icon_image:
            return f'<img src="{self.icon_image.url}" style="width: 24px; height: 24px; object-fit: cover; border-radius: 3px;" alt="{self.name}">'
        elif self.icon_class:
            color_style = f'color: {self.icon_color};' if self.icon_color else 'color: #007bff;'
            return f'<i class="{self.icon_class}" style="font-size: 18px; {color_style}"></i>'
        return '<i class="fas fa-folder" style="color: #6c757d; font-size: 18px;"></i>'

    def get_priority_level(self):
        """Priority səviyyəsini qaytarır"""
        if self.priority == 0:
            return "TOP"
        elif 1 <= self.priority <= 3:
            return "HIGH"
        elif 4 <= self.priority <= 7:
            return "MEDIUM"
        else:
            return "LOW"

    def get_priority_color(self):
        """Priority rəngini qaytarır"""
        if self.priority == 0:
            return "#6f42c1"  # Purple for TOP
        elif 1 <= self.priority <= 3:
            return "#28a745"  # Green for HIGH
        elif 4 <= self.priority <= 7:
            return "#ffc107"  # Yellow for MEDIUM
        else:
            return "#dc3545"  # Red for LOW

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

    def get_stock_status(self):
        """Stok statusunu qaytarır"""
        if self.stock == 0:
            return "out_of_stock"
        elif self.stock <= 5:
            return "low_stock"
        else:
            return "in_stock"

    def get_stock_status_display(self):
        """Stok statusu göstərimi"""
        status = self.get_stock_status()
        if status == "out_of_stock":
            return "Stokda yoxdur"
        elif status == "low_stock":
            return "Az qalıb"
        else:
            return "Stokda var"