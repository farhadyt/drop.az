# catalog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg, Min, Max
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import json
import logging

from .models import Product, Category

# Logger setup
logger = logging.getLogger(__name__)

# =================================
# HOME PAGE VIEW
# =================================
def home(request):
    """
    Ana səhifə view-ı
    Bütün aktiv məhsulları göstərir və statistikaları hesablayır
    """
    try:
        # Yalnız satışda olan məhsulları götürürük
        products = Product.objects.filter(available=True).select_related('category').order_by('-created_at')
        
        # Statistikalar
        stats = {
            'total_products': Product.objects.filter(available=True).count(),
            'total_categories': Category.objects.count(),
            'low_stock_products': Product.objects.filter(available=True, stock__lte=5).count(),
            'out_of_stock_products': Product.objects.filter(stock=0).count(),
        }
        
        # Kateqoriyalar
        categories = Category.objects.annotate(
            product_count=Count('products', filter=Q(products__available=True))
        ).filter(product_count__gt=0)
        
        # Featured məhsullar (ən yeni 8 məhsul)
        featured_products = products[:8]
        
        context = {
            'products': featured_products,
            'categories': categories,
            'stats': stats,
            'page_title': 'Əsas Səhifə',
            'meta_description': 'drop.az - Azərbaycanda ən yaxşı alış-veriş platforması. Keyfiyyətli məhsullar və sürətli çatdırılma.'
        }
        
        logger.info(f"Home page loaded with {len(featured_products)} products")
        return render(request, 'catalog/home.html', context)
        
    except Exception as e:
        logger.error(f"Error in home view: {str(e)}")
        messages.error(request, 'Səhifə yüklənərkən xəta baş verdi.')
        return render(request, 'catalog/home.html', {'products': [], 'categories': [], 'stats': {}})

# =================================
# PRODUCT LIST VIEW
# =================================
def product_list(request):
    """
    Məhsul siyahısı view-ı
    Filtrləmə, axtarış və paginasiya dəstəyi
    """
    try:
        products = Product.objects.filter(available=True).select_related('category')
        
        # Axtarış funksionallığı
        search_query = request.GET.get('search', '').strip()
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )
        
        # Kateqoriya filtri
        category_id = request.GET.get('category')
        if category_id:
            try:
                category = get_object_or_404(Category, id=category_id)
                products = products.filter(category=category)
            except:
                pass
        
        # Qiymət aralığı filtri
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if min_price:
            try:
                products = products.filter(price__gte=float(min_price))
            except ValueError:
                pass
        if max_price:
            try:
                products = products.filter(price__lte=float(max_price))
            except ValueError:
                pass
        
        # Stok filtri
        in_stock_only = request.GET.get('in_stock')
        if in_stock_only:
            products = products.filter(stock__gt=0)
        
        # Sıralama
        sort_by = request.GET.get('sort', '-created_at')
        valid_sort_options = [
            'name', '-name', 
            'price', '-price', 
            'created_at', '-created_at',
            'stock', '-stock'
        ]
        if sort_by in valid_sort_options:
            products = products.order_by(sort_by)
        else:
            products = products.order_by('-created_at')
        
        # Paginasiya
        paginator = Paginator(products, 12)  # Hər səhifədə 12 məhsul
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Kateqoriyalar (sidebar üçün)
        categories = Category.objects.annotate(
            product_count=Count('products', filter=Q(products__available=True))
        ).filter(product_count__gt=0)
        
        # Qiymət aralığı (filter üçün)
        price_range = Product.objects.filter(available=True).aggregate(
            min_price=Min('price'),
            max_price=Max('price')
        )
        
        context = {
            'page_obj': page_obj,
            'products': page_obj,
            'categories': categories,
            'search_query': search_query,
            'selected_category': category_id,
            'price_range': price_range,
            'current_filters': {
                'search': search_query,
                'category': category_id,
                'min_price': min_price,
                'max_price': max_price,
                'in_stock': in_stock_only,
                'sort': sort_by
            },
            'page_title': 'Məhsullar',
            'meta_description': f'drop.az məhsulları - {products.count()} məhsul tapıldı'
        }
        
        logger.info(f"Product list loaded: {products.count()} products found")
        return render(request, 'catalog/product_list.html', context)
        
    except Exception as e:
        logger.error(f"Error in product_list view: {str(e)}")
        messages.error(request, 'Məhsullar yüklənərkən xəta baş verdi.')
        return render(request, 'catalog/product_list.html', {'page_obj': None, 'products': []})

# =================================
# PRODUCT DETAIL VIEW
# =================================
def product_detail(request, slug):
    """
    Məhsul təfsilatı view-ı
    """
    try:
        product = get_object_or_404(Product, slug=slug, available=True)
        
        # Oxşar məhsullar (eyni kateqoriyadan)
        related_products = Product.objects.filter(
            category=product.category,
            available=True
        ).exclude(id=product.id)[:4]
        
        # Son baxılan məhsullar (session-da saxlanır)
        recently_viewed = request.session.get('recently_viewed', [])
        if product.id not in recently_viewed:
            recently_viewed.insert(0, product.id)
            recently_viewed = recently_viewed[:5]  # Son 5 məhsul
            request.session['recently_viewed'] = recently_viewed
        
        context = {
            'product': product,
            'related_products': related_products,
            'page_title': product.name,
            'meta_description': product.description[:160] if product.description else f'{product.name} - drop.az'
        }
        
        logger.info(f"Product detail viewed: {product.name} (ID: {product.id})")
        return render(request, 'catalog/product_detail.html', context)
        
    except Exception as e:
        logger.error(f"Error in product_detail view: {str(e)}")
        messages.error(request, 'Məhsul tapılmadı.')
        return redirect('catalog:home')

# =================================
# CATEGORY VIEW
# =================================
def category_detail(request, slug):
    """
    Tək kateqoriya səhifəsi - yenilənmiş versiya
    """
    try:
        category = get_object_or_404(Category, slug=slug)
        
        # Kateqoriyadakı məhsullar
        products_query = Product.objects.filter(
            category=category, 
            available=True
        ).select_related('category').order_by('-created_at')
        
        # Axtarış funksiyası
        search_query = request.GET.get('search', '').strip()
        if search_query:
            products_query = products_query.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        # Qiymət filtri
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if min_price:
            try:
                products_query = products_query.filter(price__gte=float(min_price))
            except ValueError:
                pass
        if max_price:
            try:
                products_query = products_query.filter(price__lte=float(max_price))
            except ValueError:
                pass
        
        # Sıralama
        sort_by = request.GET.get('sort', '-created_at')
        valid_sort_options = [
            'name', '-name', 'price', '-price', 'created_at', '-created_at'
        ]
        if sort_by in valid_sort_options:
            products_query = products_query.order_by(sort_by)
        
        # Paginasiya
        paginator = Paginator(products_query, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Alt kateqoriyalar
        subcategories = category.children.annotate(
            active_product_count=Count(
                'products', 
                filter=Q(products__available=True)
            )
        ).filter(active_product_count__gt=0).order_by('name')
        
        # Parent və sibling kateqoriyalar
        parent_category = category.parent
        sibling_categories = []
        if parent_category:
            sibling_categories = parent_category.children.exclude(
                id=category.id
            ).annotate(
                active_product_count=Count(
                    'products',
                    filter=Q(products__available=True)
                )
            ).filter(active_product_count__gt=0).order_by('name')[:5]
        
        # Qiymət statistikası
        price_stats = products_query.aggregate(
            min_price=Min('price'),
            max_price=Max('price'),
            avg_price=Avg('price')
        )
        
        context = {
            'category': category,
            'products': page_obj,
            'page_obj': page_obj,
            'subcategories': subcategories,
            'parent_category': parent_category,
            'sibling_categories': sibling_categories,
            'search_query': search_query,
            'price_stats': price_stats,
            'current_filters': {
                'search': search_query,
                'min_price': min_price,
                'max_price': max_price,
                'sort': sort_by
            },
            'page_title': f'{category.name} - Kateqoriya',
            'meta_description': f'{category.name} kateqoriyasında {products_query.count()} məhsul.',
            'breadcrumbs': get_category_breadcrumbs(category)
        }
        
        return render(request, 'catalog/category_detail.html', context)
        
    except Exception as e:
        logger.error(f"Error in category_detail view: {str(e)}")
        messages.error(request, 'Kateqoriya tapılmadı.')
        return redirect('catalog:home')

# =================================
# CATEGORIES LIST VIEW
# =================================
def categories_list(request):
    """
    Bütün kateqoriyalar səhifəsi
    """
    try:
        main_categories = Category.objects.filter(
            parent__isnull=True
        ).prefetch_related('children').annotate(
            active_product_count=Count(
                'products',
                filter=Q(products__available=True)
            ),
            total_subcategories=Count('children')
        ).filter(
            active_product_count__gt=0
        ).order_by('name')
        
        context = {
            'main_categories': main_categories,
            'page_title': 'Bütün Kateqoriyalar',
            'meta_description': 'drop.az-da mövcud olan bütün məhsul kateqoriyaları'
        }
        
        return render(request, 'catalog/categories_list.html', context)
        
    except Exception as e:
        logger.error(f"Error in categories_list view: {str(e)}")
        messages.error(request, 'Kateqoriyalar yüklənərkən xəta baş verdi.')
        return render(request, 'catalog/categories_list.html', {
            'main_categories': [],
            'page_title': 'Kateqoriyalar'
        })

# =================================
# AJAX VIEWS
# =================================
@require_http_methods(["GET"])
def search_suggestions(request):
    """
    AJAX axtarış təklifləri
    """
    try:
        query = request.GET.get('q', '').strip()
        suggestions = []
        
        if len(query) >= 2:
            # Məhsul adları
            products = Product.objects.filter(
                name__icontains=query,
                available=True
            )[:5]
            
            for product in products:
                suggestions.append({
                    'type': 'product',
                    'title': product.name,
                    'url': f'/product/{product.slug}/',
                    'image': product.image.url if product.image else None
                })
            
            # Kateqoriya adları
            categories = Category.objects.filter(
                name__icontains=query
            )[:3]
            
            for category in categories:
                suggestions.append({
                    'type': 'category',
                    'title': category.name,
                    'url': f'/category/{category.slug}/',
                    'image': None
                })
        
        return JsonResponse({'suggestions': suggestions})
        
    except Exception as e:
        logger.error(f"Error in search_suggestions: {str(e)}")
        return JsonResponse({'suggestions': []})

@require_http_methods(["POST"])
@csrf_exempt
def newsletter_subscribe(request):
    """
    Newsletter abunəliyi
    """
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        
        if not email:
            return JsonResponse({'success': False, 'message': 'E-mail tələb olunur'})
        
        # Email validasiyası
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return JsonResponse({'success': False, 'message': 'Düzgün e-mail daxil edin'})
        
        # Burada newsletter servisi ilə inteqrasiya olacaq
        # Məsələn: Mailchimp, SendGrid və s.
        
        # Fəaliyyətdə e-mail göndərmək
        try:
            send_mail(
                subject='drop.az Newsletter Abunəliyi',
                message=f'Yeni abunəlik: {email}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
        except:
            pass  # E-mail xətası olsa da istifadəçiyə uğurlu mesaj göstəririk
        
        logger.info(f"Newsletter subscription: {email}")
        return JsonResponse({
            'success': True, 
            'message': 'Uğurla abunə oldunuz! 🎉'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Yanlış format'})
    except Exception as e:
        logger.error(f"Error in newsletter_subscribe: {str(e)}")
        return JsonResponse({'success': False, 'message': 'Xəta baş verdi'})

@require_http_methods(["GET"])
def get_product_stats(request):
    """
    Məhsul statistikaları API
    """
    try:
        stats = {
            'total_products': Product.objects.filter(available=True).count(),
            'total_categories': Category.objects.count(),
            'low_stock_count': Product.objects.filter(available=True, stock__lte=5).count(),
            'out_of_stock_count': Product.objects.filter(stock=0).count(),
            'average_price': Product.objects.filter(available=True).aggregate(
                avg_price=Avg('price')
            )['avg_price'] or 0
        }
        
        return JsonResponse({'success': True, 'stats': stats})
        
    except Exception as e:
        logger.error(f"Error in get_product_stats: {str(e)}")
        return JsonResponse({'success': False, 'message': 'Statistikalar alına bilmədi'})

# =================================
# CLASS-BASED VIEWS
# =================================
class ProductFilterView(View):
    """
    Məhsul filtrlənməsi üçün class-based view
    """
    
    def get(self, request):
        try:
            # Filter parametrləri
            filters = {
                'available': True
            }
            
            category_id = request.GET.get('category')
            if category_id:
                filters['category_id'] = category_id
            
            min_price = request.GET.get('min_price')
            max_price = request.GET.get('max_price')
            if min_price:
                filters['price__gte'] = float(min_price)
            if max_price:
                filters['price__lte'] = float(max_price)
            
            in_stock = request.GET.get('in_stock')
            if in_stock:
                filters['stock__gt'] = 0
            
            # Məhsulları filtrləyirik
            products = Product.objects.filter(**filters).select_related('category')
            
            # AJAX sorğusu üçün JSON cavab
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                product_data = []
                for product in products[:20]:  # İlk 20 məhsul
                    product_data.append({
                        'id': product.id,
                        'name': product.name,
                        'price': float(product.price),
                        'image': product.image.url if product.image else None,
                        'slug': product.slug,
                        'category': product.category.name,
                        'stock': product.stock
                    })
                
                return JsonResponse({
                    'success': True,
                    'products': product_data,
                    'total_count': products.count()
                })
            
            # Normal HTTP sorğusu üçün
            return render(request, 'catalog/product_list.html', {
                'products': products,
                'total_count': products.count()
            })
            
        except Exception as e:
            logger.error(f"Error in ProductFilterView: {str(e)}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Filtr xətası'})
            else:
                messages.error(request, 'Filtr tətbiq edilərkən xəta baş verdi.')
                return redirect('catalog:product_list')

# =================================
# UTILITY FUNCTIONS
# =================================
def get_recently_viewed_products(request):
    """
    Son baxılan məhsulları qaytarır
    """
    try:
        recently_viewed_ids = request.session.get('recently_viewed', [])
        if recently_viewed_ids:
            # ID sırasını saxlamaq üçün
            products = Product.objects.filter(
                id__in=recently_viewed_ids,
                available=True
            )
            # Sıranı bərpa edirik
            products_dict = {p.id: p for p in products}
            ordered_products = [products_dict[pid] for pid in recently_viewed_ids if pid in products_dict]
            return ordered_products
        return []
    except Exception as e:
        logger.error(f"Error getting recently viewed products: {str(e)}")
        return []

def add_to_recently_viewed(request, product_id):
    """
    Məhsulu son baxılan siyahısına əlavə edir
    """
    try:
        recently_viewed = request.session.get('recently_viewed', [])
        if product_id in recently_viewed:
            recently_viewed.remove(product_id)
        recently_viewed.insert(0, product_id)
        recently_viewed = recently_viewed[:10]  # Son 10 məhsul
        request.session['recently_viewed'] = recently_viewed
        request.session.modified = True
    except Exception as e:
        logger.error(f"Error adding to recently viewed: {str(e)}")

def get_category_breadcrumbs(category):
    """
    Kateqoriya üçün breadcrumb yaradır
    """
    breadcrumbs = []
    current = category
    
    while current:
        breadcrumbs.insert(0, {
            'name': current.name,
            'url': f'/category/{current.slug}/',
            'slug': current.slug
        })
        current = current.parent
    
    return breadcrumbs

# =================================
# SITEMAP VIEW
# =================================
def sitemap_view(request):
    """
    XML sitemap generator
    """
    try:
        from django.urls import reverse
        from django.utils import timezone
        
        urls = []
        
        # Ana səhifə
        urls.append({
            'location': request.build_absolute_uri(reverse('catalog:home')),
            'lastmod': timezone.now(),
            'changefreq': 'daily',
            'priority': '1.0'
        })
        
        # Məhsullar
        products = Product.objects.filter(available=True)
        for product in products:
            urls.append({
                'location': request.build_absolute_uri(f'/product/{product.slug}/'),
                'lastmod': product.updated_at,
                'changefreq': 'weekly',
                'priority': '0.8'
            })
        
        # Kateqoriyalar
        categories = Category.objects.all()
        for category in categories:
            urls.append({
                'location': request.build_absolute_uri(f'/category/{category.slug}/'),
                'lastmod': timezone.now(),
                'changefreq': 'weekly',
                'priority': '0.6'
            })
        
        xml_content = render(request, 'sitemap.xml', {'urls': urls}, content_type='application/xml')
        return xml_content
        
    except Exception as e:
        logger.error(f"Error generating sitemap: {str(e)}")
        return HttpResponse('<?xml version="1.0" encoding="UTF-8"?><urlset></urlset>', content_type='application/xml')

# =================================
# ERROR HANDLING VIEWS
# =================================
def handler404(request, exception):
    """
    404 səhifəsi
    """
    return render(request, 'errors/404.html', {
        'page_title': 'Səhifə tapılmadı',
        'error_code': '404'
    }, status=404)

def handler500(request):
    """
    500 səhifəsi
    """
    return render(request, 'errors/500.html', {
        'page_title': 'Server xətası',
        'error_code': '500'
    }, status=500)