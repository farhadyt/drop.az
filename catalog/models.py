# catalog/models.py

from django.db import models

class Category(models.Model):
    """Məhsul kateqoriyalarını təmsil edən model."""
    name = models.CharField(max_length=200, verbose_name="Kateqoriyanın adı")
    slug = models.SlugField(max_length=200, unique=True, help_text="Link üçün istifadə olunacaq unikal ad (məs: elektronika-mehsullari)")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name="Üst Kateqoriya")

    class Meta:
        # Bu, admin panelində cəm halında düzgün görünməsi üçündür.
        verbose_name = "Kateqoriya"
        verbose_name_plural = "Kateqoriyalar"

    def __str__(self):
        return self.name

class Product(models.Model):
    """Məhsulları təmsil edən model."""
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="Kateqoriya")
    name = models.CharField(max_length=200, verbose_name="Məhsulun adı")
    slug = models.SlugField(max_length=200, unique=True, help_text="Link üçün istifadə olunacaq unikal ad")
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, verbose_name="Şəkil")
    description = models.TextField(blank=True, verbose_name="Təsviri")
    
    # Qiymət üçün FloatField istifadə etmək yuvarlaqlaşdırma xətaları yarada bilər.
    # Ona görə DecimalField daha peşəkar və doğru seçimdir.
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Qiymət (AZN)")
    
    stock = models.PositiveIntegerField(verbose_name="Anbardakı say")
    available = models.BooleanField(default=True, verbose_name="Satışda mövcuddur?")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma tarixi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə tarixi")

    class Meta:
        verbose_name = "Məhsul"
        verbose_name_plural = "Məhsullar"
        ordering = ['-created_at'] # Məhsulları yaradılma tarixinə görə sıralayır

    def __str__(self):
        return self.name