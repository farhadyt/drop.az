# catalog/urls.py - COMPLETE FILE with Hero Pages
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

# App namespace
app_name = 'catalog'

urlpatterns = [
    # =================================
    # MAIN PAGES
    # =================================
    
    # Ana səhifə (original home page with full layout)
    path('', views.home, name='home'),
    
    # =================================
    # 🆕 HERO PAGES - NEW ADDITIONS
    # =================================
    
    # Bütün kateqoriyalar hero səhifəsi
    path('categories-hero/', views.categories_hero_view, name='categories_hero'),
    path('kateqoriyalar-hero/', views.categories_hero_view, name='categories_hero_az'),
    
    # Tək kateqoriya hero səhifəsi  
    path('category-hero/<slug:slug>/', views.category_hero_view, name='category_hero'),
    path('kateqoriya-hero/<slug:slug>/', views.category_hero_view, name='category_hero_az'),
    
    # =================================
    # ORIGINAL PAGES (backward compatibility)
    # =================================
    
    # Məhsul siyahısı
    path('products/', views.product_list, name='product_list'),
    path('mehsullar/', views.product_list, name='product_list_az'),
    
    # Məhsul təfsilatı
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('mehsul/<slug:slug>/', views.product_detail, name='product_detail_az'),
    
    # Original kateqoriya səhifələri
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('kateqoriya/<slug:slug>/', views.category_detail, name='category_detail_az'),

    path('categories/', views.categories_list, name='categories_list'),
    path('kateqoriyalar/', views.categories_list, name='categories_list_az'),
    
    # =================================
    # AJAX & API ENDPOINTS
    # =================================
    
    # Axtarış təklifləri (AJAX)
    path('api/search-suggestions/', views.search_suggestions, name='search_suggestions'),
    
    # Newsletter abunəliyi (AJAX)
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
    # LANGUAGE-SPECIFIC URLS
    # =================================
    
    # Azərbaycan dilində URL-lər
    path('ana-sehife/', views.home, name='home_az'),
    path('mehsullar/', views.product_list, name='products_az'),
    path('endirimler/', TemplateView.as_view(template_name='pages/sales.html'), name='sales_az'),
    path('yenilikler/', TemplateView.as_view(template_name='pages/new_products.html'), name='new_products_az'),
]

# =================================
# API VERSIONING
# =================================

# API v1 patterns
api_v1_patterns = [
    path('v1/products/', views.product_list, name='api_v1_products'),
    path('v1/categories/', views.categories_hero_view, name='api_v1_categories'),
    path('v1/search/', views.search_suggestions, name='api_v1_search'),
]

# API patterns-i əlavə et
urlpatterns += [path('api/', include(api_v1_patterns))]