# catalog/views.py - CLEAN VERSION WITHOUT CATEGORIES
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

from .models import Product

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
        products = Product.objects.filter(available=True).order_by('-created_at')
        
        # Statistikalar
        stats = {
            'total_products': Product.objects.filter(available=True).count(),
            'low_stock_products': Product.objects.filter(available=True, stock__lte=5).count(),
            'out_of_stock_products': Product.objects.filter(stock=0).count(),
            'average_price': Product.objects.filter(available=True).aggregate(avg_price=Avg('price'))['avg_price'] or 0,
        }
        
        # Featured məhsullar (ən yeni 8 məhsul)
        featured_products = products[:8]
        
        context = {
            'products': featured_products,
            'stats': stats,
            'page_title': 'Əsas Səhifə',
            'meta_description': 'drop.az - Azərbaycanda ən yaxşı alış-veriş platforması. Keyfiyyətli məhsullar və sürətli çatdırılma.'
        }
        
        logger.info(f"Home page loaded with {len(featured_products)} products")
        return render(request, 'catalog/home.html', context)
        
    except Exception as e:
        logger.error(f"Error in home view: {str(e)}")
        messages.error(request, 'Səhifə yüklənərkən xəta baş verdi.')
        return render(request, 'catalog/home.html', {'products': [], 'stats': {}})

# =================================
# PRODUCT LIST VIEW
# =================================
def product_list(request):
    """
    Məhsul siyahısı view-ı
    Filtrləmə, axtarış və paginasiya dəstəyi
    """
    try:
        products = Product.objects.filter(available=True)
        
        # Axtarış funksionallığı
        search_query = request.GET.get('search', '').strip()
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
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
        
        # Qiymət aralığı (filter üçün)
        price_range = Product.objects.filter(available=True).aggregate(
            min_price=Min('price'),
            max_price=Max('price')
        )
        
        context = {
            'page_obj': page_obj,
            'products': page_obj,
            'search_query': search_query,
            'price_range': price_range,
            'current_filters': {
                'search': search_query,
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
        
        # Oxşar məhsullar (ən yeni məhsullardan)
        related_products = Product.objects.filter(
            available=True
        ).exclude(id=product.id).order_by('-created_at')[:4]
        
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
            )[:8]
            
            for product in products:
                suggestions.append({
                    'type': 'product',
                    'title': product.name,
                    'url': f'/product/{product.slug}/',
                    'image': product.image.url if product.image else None,
                    'price': str(product.price)
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
        
        # Newsletter servisinə əlavə et (burada database-ə yazılacaq)
        # Fəaliyyətdə e-mail göndərmək
        try:
            send_mail(
                subject='drop.az Newsletter Abunəliyi',
                message=f'Yeni abunəlik: {email}',
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@drop.az'),
                recipient_list=[getattr(settings, 'ADMIN_EMAIL', 'admin@drop.az')],
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
            'low_stock_count': Product.objects.filter(available=True, stock__lte=5).count(),
            'out_of_stock_count': Product.objects.filter(stock=0).count(),
            'average_price': Product.objects.filter(available=True).aggregate(
                avg_price=Avg('price')
            )['avg_price'] or 0,
            'newest_products_count': Product.objects.filter(available=True).order_by('-created_at')[:10].count(),
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
            
            min_price = request.GET.get('min_price')
            max_price = request.GET.get('max_price')
            if min_price:
                filters['price__gte'] = float(min_price)
            if max_price:
                filters['price__lte'] = float(max_price)
            
            in_stock = request.GET.get('in_stock')
            if in_stock:
                filters['stock__gt'] = 0
            
            search_query = request.GET.get('search', '').strip()
            
            # Məhsulları filtrləyirik
            products = Product.objects.filter(**filters)
            
            if search_query:
                products = products.filter(
                    Q(name__icontains=search_query) | 
                    Q(description__icontains=search_query)
                )
            
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
                        'stock': product.stock,
                        'available': product.available
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

def product_list_hero(request):
    """Hero versiyası - Məhsul siyahısı"""
    try:
        # product_list funksiyasının eyni məntiqini istifadə et
        products = Product.objects.filter(available=True).order_by('-created_at')
        
        # Axtarış
        search_query = request.GET.get('search', '').strip()
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        # Filtrləmə
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
        
        # Paginasiya
        paginator = Paginator(products, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'page_obj': page_obj,
            'products': page_obj,
            'search_query': search_query,
            'page_title': 'Məhsullar - Hero',
            'meta_description': f'drop.az məhsulları hero versiyası - {products.count()} məhsul tapıldı'
        }
        
        return render(request, 'catalog/product_list_hero.html', context)
    except Exception as e:
        logger.error(f"Error in product_list_hero: {str(e)}")
        return redirect('catalog:home')

def product_detail_hero(request, slug):
    """Hero versiyası - Məhsul təfsilatı"""
    try:
        product = get_object_or_404(Product, slug=slug, available=True)
        
        # Oxşar məhsullar
        related_products = Product.objects.filter(
            available=True
        ).exclude(id=product.id).order_by('-created_at')[:4]
        
        # Son baxılan məhsullar
        recently_viewed = request.session.get('recently_viewed', [])
        if product.id not in recently_viewed:
            recently_viewed.insert(0, product.id)
            recently_viewed = recently_viewed[:5]
            request.session['recently_viewed'] = recently_viewed
        
        context = {
            'product': product,
            'related_products': related_products,
            'page_title': f'{product.name} - Hero',
            'meta_description': product.description[:160] if product.description else f'{product.name} - drop.az hero versiyası'
        }
        
        return render(request, 'catalog/product_detail_hero.html', context)
    except Exception as e:
        logger.error(f"Error in product_detail_hero: {str(e)}")
        return redirect('catalog:home')