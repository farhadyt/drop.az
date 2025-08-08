# catalog/context_processors.py - ENHANCED VERSION FOR 3-LEVEL NAVIGATION
from django.db.models import Q, Count
from django.core.cache import cache
import logging

from .models import Category

logger = logging.getLogger(__name__)

def categories_context(request):
    """
    3-səviyyəli navigation üçün kateqoriyalar və global məlumatları 
    bütün template-lərə göndərir. Full Width Mega Menu üçün optimizasiya edilib.
    BÜTÜN kateqoriyalar göstərilir (boş olsa belə).
    """
    try:
        # Cache key
        cache_key = 'header_categories_fullwidth_v3'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        # Header navigation üçün əsas kateqoriyalar (maksimum 15 əsas kateqoriya)
        main_categories = Category.objects.filter(
            parent__isnull=True  # Yalnız əsas kateqoriyalar
        ).prefetch_related(
            'children__children',  # 3-cü səviyyə də prefetch
            'children__products'   # Performance üçün
        ).annotate(
            # Aktiv məhsul sayını hesabla (özü + uşaqları + nəvələri)
            direct_product_count=Count(
                'products',
                filter=Q(products__available=True)
            ),
            children_product_count=Count(
                'children__products',
                filter=Q(children__products__available=True)
            ),
            grandchildren_product_count=Count(
                'children__children__products',
                filter=Q(children__children__products__available=True)
            )
        ).order_by('name')
        
        # Navigation data hazırla - BÜTÜN kateqoriyalar (boş olsa belə)
        navigation_categories = []
        for category in main_categories:
            # Total məhsul sayı (direct + children + grandchildren)
            total_products = (
                category.direct_product_count + 
                category.children_product_count + 
                category.grandchildren_product_count
            )
            
            # BÜTÜN kateqoriyaları göstər, məhsul sayından asılı olmayaraq
            if category.slug:  # Yalnız slug yoxlaması
                # Alt kateqoriyaları hazırla (Level 2)
                children_data = []
                for child in category.children.all():
                    if child.slug:  # slug yoxlaması
                        # Child-ın məhsul sayı (direct + grandchildren)
                        child_direct_count = child.products.filter(available=True).count()
                        child_grandchildren_count = 0
                        
                        # Grandchildren məlumatları (Level 3)
                        grandchildren_data = []
                        for grandchild in child.children.all():
                            if grandchild.slug:
                                grandchild_product_count = grandchild.products.filter(available=True).count()
                                # Boş olanları da əlavə et
                                grandchildren_data.append({
                                    'id': grandchild.id,
                                    'name': grandchild.name,
                                    'slug': grandchild.slug,
                                    'product_count': grandchild_product_count,
                                    'url': f'/categories/{grandchild.slug}/'
                                })
                                child_grandchildren_count += grandchild_product_count
                        
                        # Total child məhsul sayı
                        child_total_products = child_direct_count + child_grandchildren_count
                        
                        # BÜTÜN alt kateqoriyaları əlavə et (boş olsa belə)
                        children_data.append({
                            'id': child.id,
                            'name': child.name,
                            'slug': child.slug,
                            'product_count': child_total_products,
                            'direct_product_count': child_direct_count,
                            'url': f'/categories/{child.slug}/',
                            'children': grandchildren_data,  # 3-cü səviyyə
                            'has_children': len(grandchildren_data) > 0
                        })
                
                # Maksimum 10 alt kateqoriya göstər (performans üçün)
                children_data = children_data[:10]
                
                navigation_categories.append({
                    'category': category,
                    'children': children_data,
                    'has_children': len(children_data) > 0,
                    'total_product_count': total_products,
                    'direct_product_count': category.direct_product_count,
                    'url': f'/categories/{category.slug}/'
                })
        
        # Maksimum 15 əsas kateqoriya göstər
        navigation_categories = navigation_categories[:15]
        
        # Ümumi statistikalar - BÜTÜN kateqoriyalar
        total_active_categories = Category.objects.count()  # Hamısı
        
        # 3-səviyyəli kateqoriya statistikaları
        categories_with_children = Category.objects.filter(
            parent__isnull=True,
            children__isnull=False
        ).distinct().count()
        
        categories_with_grandchildren = Category.objects.filter(
            parent__isnull=True,
            children__children__isnull=False
        ).distinct().count()
        
        # Context məlumatları
        context_data = {
            'header_categories': navigation_categories,
            'total_categories_count': total_active_categories,
            'main_categories_count': len(navigation_categories),
            'categories_with_children': categories_with_children,
            'categories_with_grandchildren': categories_with_grandchildren,
            'category_navigation_enabled': True,
            'navigation_levels': 3,  # 3-səviyyəli olduğunu göstər
            'mega_menu_full_width': True,  # Full width mega menu aktiv
        }
        
        # 5 dəqiqə cache et (300 saniyə)
        cache.set(cache_key, context_data, 300)
        
        logger.info(f"Full Width 3-Level Categories context loaded: {len(navigation_categories)} main categories (including empty ones)")
        
        return context_data
        
    except Exception as e:
        logger.error(f"Error in categories_context: {str(e)}")
        
        # Xəta olduqda minimal məlumat qaytar
        return {
            'header_categories': [],
            'total_categories_count': 0,
            'main_categories_count': 0,
            'categories_with_children': 0,
            'categories_with_grandchildren': 0,
            'category_navigation_enabled': False,
            'navigation_levels': 1,
            'mega_menu_full_width': False,
        }

def navigation_breadcrumb(request):
    """
    Hazırki səhifə üçün breadcrumb məlumatları yaradır (3-səviyyə dəstəyi ilə)
    """
    try:
        breadcrumb = []
        
        # URL path-dən breadcrumb yaradılması
        path_parts = request.path.strip('/').split('/')
        
        # Ana səhifə həmişə əlavə et
        breadcrumb.append({
            'name': 'Ana Səhifə',
            'url': '/',
            'is_current': len(path_parts) == 1 and path_parts[0] == ''
        })
        
        # Kateqoriya səhifələri üçün
        if len(path_parts) >= 2 and path_parts[0] == 'categories':
            breadcrumb.append({
                'name': 'Kateqoriyalar',
                'url': '/categories/',
                'is_current': len(path_parts) == 2
            })
            
            # Spesifik kateqoriya
            if len(path_parts) >= 3 and path_parts[2]:
                try:
                    category_slug = path_parts[2]
                    category = Category.objects.select_related('parent__parent').get(slug=category_slug)
                    
                    # Parent kateqoriyalar chain-i (3-səviyyə daxil olmaqla)
                    category_chain = []
                    current_cat = category
                    while current_cat:
                        category_chain.insert(0, current_cat)
                        current_cat = current_cat.parent
                    
                    # Breadcrumb-a əlavə et
                    for i, cat in enumerate(category_chain):
                        if cat.slug:
                            breadcrumb.append({
                                'name': cat.name,
                                'slug': cat.slug,
                                'url': f'/categories/{cat.slug}/',
                                'is_current': i == len(category_chain) - 1,
                                'level': len(category_chain) - i  # Hansı səviyyə olduğunu göstər
                            })
                        
                except Category.DoesNotExist:
                    pass
        
        # Məhsul səhifələri üçün
        elif len(path_parts) >= 2 and path_parts[0] == 'product':
            breadcrumb.append({
                'name': 'Məhsullar',
                'url': '/products/',
                'is_current': False
            })
            
            if len(path_parts) >= 3 and path_parts[2]:
                try:
                    from .models import Product
                    product_slug = path_parts[2]
                    product = Product.objects.select_related(
                        'category__parent__parent'  # 3-səviyyə parent
                    ).get(slug=product_slug)
                    
                    # Kateqoriya chain (3-səviyyə daxil olmaqla)
                    current_cat = product.category
                    category_chain = []
                    while current_cat:
                        category_chain.insert(0, current_cat)
                        current_cat = current_cat.parent
                    
                    # Kateqoriyaları əlavə et
                    for cat in category_chain:
                        if cat.slug:
                            breadcrumb.append({
                                'name': cat.name,
                                'url': f'/categories/{cat.slug}/',
                                'is_current': False
                            })
                    
                    # Məhsul
                    if product.slug:
                        breadcrumb.append({
                            'name': product.name,
                            'url': f'/product/{product.slug}/',
                            'is_current': True
                        })
                    
                except:
                    pass
        
        return {
            'breadcrumb': breadcrumb,
            'breadcrumb_count': len(breadcrumb),
            'max_breadcrumb_level': max([item.get('level', 1) for item in breadcrumb]) if breadcrumb else 1
        }
        
    except Exception as e:
        logger.error(f"Error in navigation_breadcrumb: {str(e)}")
        return {
            'breadcrumb': [],
            'breadcrumb_count': 0,
            'max_breadcrumb_level': 1
        }

def site_settings(request):
    """
    Sayt üçün ümumi tənzimləmələr və məlumatlar
    """
    try:
        return {
            'site_name': 'drop.az',
            'site_tagline': 'Azərbaycanda ən yaxşı alış-veriş platforması',
            'support_phone': '+994 XX XXX XX XX',
            'support_email': 'info@drop.az',
            'support_whatsapp': '+994XXXXXXXXX',
            'working_hours': 'B.e - Cümə: 09:00-18:00, Şənbə-Bazar: 10:00-16:00',
            'company_address': 'Bakı, Azərbaycan',
            'social_links': {
                'facebook': '#',
                'instagram': '#',
                'youtube': '#',
                'whatsapp': '#'
            },
            'features': {
                'free_shipping_limit': 50,  # AZN
                'express_delivery_hours': '2-3',
                'support_available': '24/7',
                'ssl_encrypted': True,
                'warranty_days': 30
            },
            'navigation_features': {
                'mega_menu_enabled': True,
                'mega_menu_full_width': True,  # Full width aktiv
                'levels_supported': 3,
                'mobile_accordion': True,
                'search_suggestions': True,
                'hover_delay': 300,  # milliseconds
                'animation_speed': 250  # milliseconds
            }
        }
        
    except Exception as e:
        logger.error(f"Error in site_settings: {str(e)}")
        return {}

def user_session_data(request):
    """
    İstifadəçi session məlumatları (cart, favorites, recent views)
    """
    try:
        # Session-dan məlumatları al
        cart_items = request.session.get('cart_items', [])
        favorite_items = request.session.get('favorite_items', [])
        recently_viewed = request.session.get('recently_viewed', [])
        recent_searches = request.session.get('recent_searches', [])
        
        return {
            'session_data': {
                'cart_count': len(cart_items),
                'favorites_count': len(favorite_items),
                'recently_viewed_count': len(recently_viewed),
                'recent_searches': recent_searches[:5],  # Son 5 axtarış
                'has_session_data': len(cart_items) > 0 or len(favorite_items) > 0
            }
        }
        
    except Exception as e:
        logger.error(f"Error in user_session_data: {str(e)}")
        return {
            'session_data': {
                'cart_count': 0,
                'favorites_count': 0,
                'recently_viewed_count': 0,
                'recent_searches': [],
                'has_session_data': False
            }
        }

def performance_data(request):
    """
    Performance və debug məlumatları (development üçün)
    """
    try:
        if hasattr(request, 'user') and request.user.is_staff:
            from django.db import connection
            from django.conf import settings
            
            return {
                'debug_info': {
                    'is_debug': getattr(settings, 'DEBUG', False),
                    'db_queries_count': len(connection.queries) if settings.DEBUG else 0,
                    'cache_enabled': hasattr(settings, 'CACHES'),
                    'request_path': request.path,
                    'request_method': request.method,
                    'navigation_system': 'Full Width 3-Level Mega Menu v3',
                    'cache_status': 'Active' if cache.get('header_categories_fullwidth_v3') else 'Empty',
                    'mega_menu_version': 'v3.0 - Shows All Categories'
                }
            }
        else:
            return {'debug_info': {}}
            
    except Exception as e:
        logger.error(f"Error in performance_data: {str(e)}")
        return {'debug_info': {}}