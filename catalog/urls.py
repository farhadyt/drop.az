# catalog/urls.py - ENHANCED VERSION WITH CATEGORY NAVIGATION
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

# App namespace
app_name = 'catalog'

urlpatterns = [
    # =================================
    # MAIN PAGES
    # =================================
    
    # Ana səhifə (main home page with full layout)
    path('', views.home, name='home'),
    
    # =================================
    # CATEGORY PAGES
    # =================================
    
    # Bütün kateqoriyalar səhifəsi
    path('categories/', views.categories_view, name='categories'),
    path('kategoriyalar/', views.categories_view, name='categories_az'),
    
    # Spesifik kateqoriya səhifəsi (və onun məhsulları)
    path('categories/<slug:slug>/', views.category_detail, name='category_detail'),
    path('kategoriya/<slug:slug>/', views.category_detail, name='category_detail_az'),
    
    # Alt kateqoriya səhifəsi
    path('categories/<slug:parent_slug>/<slug:slug>/', views.subcategory_detail, name='subcategory_detail'),
    path('kategoriya/<slug:parent_slug>/<slug:slug>/', views.subcategory_detail, name='subcategory_detail_az'),
    
    # =================================
    # PRODUCT PAGES
    # =================================
    
    # Məhsul siyahısı
    path('products/', views.product_list, name='product_list'),
    path('mehsullar/', views.product_list, name='product_list_az'),

    # Hero versiyaları üçün (legacy)
    path('products-hero/', views.product_list_hero, name='product_list_hero'),
    path('product-hero/<slug:slug>/', views.product_detail_hero, name='product_detail_hero'),
    
    # =================================
    # HERO PAGE TEMPLATE VERSIONS - Yeni base_hero.html istifadə edən səhifələr
    # =================================
    
    # Kateqoriyalar - Hero versiyası
    path('categories-hero/', views.categories_hero, name='categories_hero'),
    path('kategoriyalar-hero/', views.categories_hero, name='categories_hero_az'),
    
    # Məhsullar - Hero versiyası  
    path('products-hero-new/', views.products_hero, name='products_hero'),
    path('mehsullar-hero/', views.products_hero, name='products_hero_az'),
    
    # Haqqımızda - Hero versiyası
    path('about-hero/', views.about_hero, name='about_hero'),
    path('haqqimizda-hero/', views.about_hero, name='about_hero_az'),
    
    # Məhsul təfsilatı
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('mehsul/<slug:slug>/', views.product_detail, name='product_detail_az'),
    
    # Kateqoriyaya görə məhsullar
    path('products/category/<slug:category_slug>/', views.products_by_category, name='products_by_category'),
    path('mehsullar/kategoriya/<slug:category_slug>/', views.products_by_category, name='products_by_category_az'),
    
    # =================================
    # AJAX & API ENDPOINTS
    # =================================
    
    # Axtarış təklifləri (AJAX)
    path('api/search-suggestions/', views.search_suggestions, name='search_suggestions'),
    
    # Newsletter abunəliyi (AJAX)
    path('api/newsletter-subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    
    # Məhsul statistikaları (AJAX)
    path('api/product-stats/', views.get_product_stats, name='product_stats'),
    
    # Kateqoriya statistikaları (AJAX)
    path('api/category-stats/', views.get_category_stats, name='category_stats'),
    
    # Məhsul filtrləri (AJAX)
    path('api/filter-products/', views.ProductFilterView.as_view(), name='filter_products'),
    
    # Kateqoriya məhsulları (AJAX)
    path('api/category-products/<slug:category_slug>/', views.CategoryProductsView.as_view(), name='category_products'),
    
    # =================================
    # SPECIAL PAGES
    # =================================
    
    # Haqqımızda səhifəsi
    path('about/', views.about_hero, name='about'),
    
    # Əlaqə səhifəsi
    path('contact/', views.contact_hero, name='contact'),
    
    # Çatdırılma məlumatları
    path('delivery/', views.delivery_hero, name='delivery'),
    
    # Qaytarma şərtləri
    path('returns/', views.returns_hero, name='returns'),
    
    # Ödəniş üsulları
    path('payment/', views.payment_hero, name='payment'),
    
    # FAQ - Tez-tez verilən suallar
    path('faq/', views.faq_hero, name='faq'),
    
    # Zəmanət şərtləri
    path('warranty/', views.warranty_hero, name='warranty'),
    
    # =================================
    # LEGAL PAGES
    # =================================
    
    # İstifadə şərtləri
    path('terms/', views.terms_hero, name='terms'),
    
    # Məxfilik siyasəti
    path('privacy/', views.privacy_hero, name='privacy'),
    
    # Çerez siyasəti
    path('cookies/', views.cookies_hero, name='cookies'),
    
    # =================================
    # SEARCH & FILTER URLS
    # =================================
    
    # Axtarış səhifəsi
    path('search/', views.product_list, name='search'),
    path('axtar/', views.product_list, name='search_az'),
    
    # Qiymət aralığı filter
    path('products/price/<int:min_price>-<int:max_price>/', views.product_list, name='products_by_price'),
    
    # Kateqoriya + qiymət filteri
    path('categories/<slug:category_slug>/price/<int:min_price>-<int:max_price>/', 
         views.products_by_category, name='category_products_by_price'),
    
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
    path('endirimler/', views.delivery_hero, name='sales_az'),  # Temporarily use delivery hero
    path('yenilikler/', views.delivery_hero, name='new_products_az'),  # Temporarily use delivery hero
    
    # =================================
    # BREADCRUMB & NAVIGATION HELPERS
    # =================================
    
    # Kateqoriya yolu (breadcrumb helper)
    path('api/category-breadcrumb/<slug:category_slug>/', views.get_category_breadcrumb, name='category_breadcrumb'),
    
    # Kateqoriya ağacı (navigation helper)
    path('api/category-tree/', views.get_category_tree, name='category_tree'),
]

# =================================
# API VERSIONING
# =================================

# API v1 patterns
api_v1_patterns = [
    path('v1/products/', views.product_list, name='api_v1_products'),
    path('v1/categories/', views.categories_view, name='api_v1_categories'),
    path('v1/category/<slug:slug>/', views.category_detail, name='api_v1_category_detail'),
    path('v1/search/', views.search_suggestions, name='api_v1_search'),
]

# API patterns-i əlavə et
urlpatterns += [path('api/', include(api_v1_patterns))]

# =================================
# ERROR HANDLING URLS
# =================================

# Custom error pages (if needed)
handler404 = 'catalog.views.handler404'
handler500 = 'catalog.views.handler500'