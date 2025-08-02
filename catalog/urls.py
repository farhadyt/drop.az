# catalog/urls.py
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

# App namespace
app_name = 'catalog'

urlpatterns = [
    # =================================
    # MAIN PAGES
    # =================================
    
    # Ana səhifə
    path('', views.home, name='home'),
    
    # Məhsul siyahısı
    path('products/', views.product_list, name='product_list'),
    path('mehsullar/', views.product_list, name='product_list_az'),  # Azərbaycan dilində
    
    # Məhsul təfsilatı
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('mehsul/<slug:slug>/', views.product_detail, name='product_detail_az'),
    
    # Kateqoriya səhifələri
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('kateqoriya/<slug:slug>/', views.category_detail, name='category_detail_az'),

    path('categories/', views.categories_list, name='categories_list'),
    path('kateqoriyalar/', views.categories_list, name='categories_list_az'),
    
    # =================================
    # AJAX & API ENDPOINTS
    # =================================
    
    # Axtarış təklifləri (AJAX)
    path('api/search-suggestions/', views.search_suggestions, name='search_suggestions'),
    
    # Newsletter abunəliği (AJAX)
    path('api/newsletter-subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    
    # Məhsul statistikaları (AJAX)
    path('api/product-stats/', views.get_product_stats, name='product_stats'),
    
    # Məhsul filtrləri (AJAX)
    path('api/filter-products/', views.ProductFilterView.as_view(), name='filter_products'),
    
    # =================================
    # SPECIAL PAGES
    # =================================
    
    # Haqqımızda səhifəsi
    path('about/', TemplateView.as_view(
        template_name='pages/about.html',
        extra_context={
            'page_title': 'Haqqımızda',
            'meta_description': 'drop.az haqqında məlumat - missiyamız və dəyərlərimiz'
        }
    ), name='about'),
    
    # Əlaqə səhifəsi
    path('contact/', TemplateView.as_view(
        template_name='pages/contact.html',
        extra_context={
            'page_title': 'Əlaqə',
            'meta_description': 'drop.az ilə əlaqə saxlayın - telefon, e-mail və ünvan'
        }
    ), name='contact'),
    
    # Çatdırılma məlumatları
    path('delivery/', TemplateView.as_view(
        template_name='pages/delivery.html',
        extra_context={
            'page_title': 'Çatdırılma',
            'meta_description': 'drop.az çatdırılma şərtləri və qiymətləri'
        }
    ), name='delivery'),
    
    # Qaytarma şərtləri
    path('returns/', TemplateView.as_view(
        template_name='pages/returns.html',
        extra_context={
            'page_title': 'Qaytarma',
            'meta_description': 'drop.az qaytarma şərtləri və prosedurları'
        }
    ), name='returns'),
    
    # Ödəniş üsulları
    path('payment/', TemplateView.as_view(
        template_name='pages/payment.html',
        extra_context={
            'page_title': 'Ödəniş',
            'meta_description': 'drop.az ödəniş üsulları və təhlükəsizlik'
        }
    ), name='payment'),
    
    # FAQ - Tez-tez verilən suallar
    path('faq/', TemplateView.as_view(
        template_name='pages/faq.html',
        extra_context={
            'page_title': 'FAQ',
            'meta_description': 'drop.az tez-tez verilən suallar və cavablar'
        }
    ), name='faq'),
    
    # Zəmanət şərtləri
    path('warranty/', TemplateView.as_view(
        template_name='pages/warranty.html',
        extra_context={
            'page_title': 'Zəmanət',
            'meta_description': 'drop.az zəmanət şərtləri və xidmətləri'
        }
    ), name='warranty'),
    
    # =================================
    # LEGAL PAGES
    # =================================
    
    # İstifadə şərtləri
    path('terms/', TemplateView.as_view(
        template_name='legal/terms.html',
        extra_context={
            'page_title': 'İstifadə Şərtləri',
            'meta_description': 'drop.az istifadə şərtləri və qaydalar'
        }
    ), name='terms'),
    
    # Məxfilik siyasəti
    path('privacy/', TemplateView.as_view(
        template_name='legal/privacy.html',
        extra_context={
            'page_title': 'Məxfilik Siyasəti',
            'meta_description': 'drop.az məxfilik siyasəti və şəxsi məlumatların qorunması'
        }
    ), name='privacy'),
    
    # Çerez siyasəti
    path('cookies/', TemplateView.as_view(
        template_name='legal/cookies.html',
        extra_context={
            'page_title': 'Çerez Siyasəti',
            'meta_description': 'drop.az çerez siyasəti və istifadəsi'
        }
    ), name='cookies'),
    
    # =================================
    # SEARCH & FILTER URLS
    # =================================
    
    # Axtarış səhifəsi
    path('search/', views.product_list, name='search'),
    path('axtar/', views.product_list, name='search_az'),
    
    # Kateqoriya filter
    path('products/category/<slug:category_slug>/', views.product_list, name='products_by_category'),
    
    # Qiymət aralığı filter
    path('products/price/<int:min_price>-<int:max_price>/', views.product_list, name='products_by_price'),
    
    # Brend filter (gələcək üçün)
    # path('products/brand/<slug:brand_slug>/', views.product_list, name='products_by_brand'),
    
    # =================================
    # SEO & UTILITY URLS
    # =================================
    
    # XML Sitemap
    path('sitemap.xml', views.sitemap_view, name='sitemap'),
    
    # Robots.txt
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt',
        content_type='text/plain'
    ), name='robots'),
    
    # =================================
    # DEVELOPMENT & TESTING URLS
    # =================================
    
    # Test səhifəsi (yalnız DEBUG=True zamanı)
    # path('test/', TemplateView.as_view(template_name='test/test.html'), name='test'),
    
    # =================================
    # REDIRECTS (Köhnə URL-lərdən yenilərə)
    # =================================
    
    # Köhnə product URL-dən yeniyə redirect
    # path('products/<int:id>/', RedirectView.as_view(pattern_name='catalog:product_detail'), name='product_redirect'),
]

# =================================
# CUSTOM ERROR HANDLERS
# =================================

# Bu URL patterns yalnız DEBUG=False zamanı işləyir
# settings.py-də handler404 və handler500 təyin edilməlidir

# =================================
# DYNAMIC URL PATTERNS (İdarəetmə panelindən əlavə edilən)
# =================================

# Bu hissə gələcəkdə dinamik səhifələr üçün istifadə oluna bilər
# Məsələn: blog, yeniliklər, kampaniyalar və s.

# =================================
# LANGUAGE-SPECIFIC URLS
# =================================

# Azərbaycan dilində URL-lər
az_patterns = [
    path('ana-sehife/', views.home, name='home_az'),
    path('mehsullar/', views.product_list, name='products_az'),
    path('kateqoriyalar/', TemplateView.as_view(template_name='pages/categories.html'), name='categories_az'),
    path('endirimler/', TemplateView.as_view(template_name='pages/sales.html'), name='sales_az'),
    path('yenilikler/', TemplateView.as_view(template_name='pages/new_products.html'), name='new_products_az'),
]

# Ana URL patterns-ə əlavə et
urlpatterns += az_patterns

# =================================
# API VERSIONING (Gələcək üçün)
# =================================

# API v1 patterns
api_v1_patterns = [
    path('v1/products/', views.product_list, name='api_v1_products'),
    path('v1/categories/', views.category_detail, name='api_v1_categories'),
    path('v1/search/', views.search_suggestions, name='api_v1_search'),
]

# API patterns-i əlavə et
urlpatterns += [path('api/', include(api_v1_patterns))]

# =================================
# ADMIN HELPER URLS
# =================================

# Admin üçün köməkçi URL-lər (yalnız staff istifadəçilər üçün)
admin_patterns = [
    # path('admin-tools/clear-cache/', views.clear_cache, name='admin_clear_cache'),
    # path('admin-tools/export-products/', views.export_products, name='admin_export_products'),
    # path('admin-tools/import-products/', views.import_products, name='admin_import_products'),
]

# =================================
# SOCIAL MEDIA & SHARING URLS
# =================================

# Social media sharing üçün URL-lər
social_patterns = [
    # path('share/facebook/<slug:slug>/', views.share_facebook, name='share_facebook'),
    # path('share/twitter/<slug:slug>/', views.share_twitter, name='share_twitter'),
    # path('share/whatsapp/<slug:slug>/', views.share_whatsapp, name='share_whatsapp'),
]

# =================================
# WEBHOOK URLS (Third-party integrations üçün)
# =================================

# Webhook URL-ləri (ödəniş sistemləri, çatdırılma xidmətləri və s.)
webhook_patterns = [
    # path('webhooks/payment/', views.payment_webhook, name='payment_webhook'),
    # path('webhooks/delivery/', views.delivery_webhook, name='delivery_webhook'),
]

# =================================
# MOBILE APP API URLS
# =================================

# Mobil tətbiq üçün API endpoint-lər
mobile_api_patterns = [
    # path('mobile/api/products/', views.mobile_product_list, name='mobile_products'),
    # path('mobile/api/categories/', views.mobile_category_list, name='mobile_categories'),
    # path('mobile/api/auth/', views.mobile_auth, name='mobile_auth'),
]

# =================================
# URL NAME REFERENCE
# =================================

"""
URL Names və istifadə nümunələri:

Template-lərdə istifadə:
{% url 'catalog:home' %}
{% url 'catalog:product_detail' slug='iphone-14' %}
{% url 'catalog:category_detail' slug='telefonlar' %}

Views-da istifadə:
from django.urls import reverse
url = reverse('catalog:product_detail', kwargs={'slug': 'iphone-14'})

JavaScript-də istifadə:
fetch('{% url "catalog:search_suggestions" %}?q=iphone')
"""

# =================================
# URL OPTIMIZATION NOTES
# =================================

"""
SEO üçün URL optimallaşdırması:

1. Qısa və təsviri URL-lər
2. Slug field-lərin istifadəsi
3. Azərbaycan dilində URL seçimləri
4. Canonicalization (dublika URL-lərin qarşısının alınması)
5. 301 redirects köhnə URL-lər üçün
6. URL structure-un consistent olması

Nümunə yaxşı URL-lər:
/mehsul/iphone-14-pro-max/
/kateqoriya/telefonlar/
/mehsullar/?search=iphone&category=telefonlar
"""