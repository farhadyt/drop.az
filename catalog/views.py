# catalog/views.py - ENHANCED VERSION WITH CATEGORY NAVIGATION
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
            'low_stock_products': Product.objects.filter(available=True, stock__lte=5).count(),
            'out_of_stock_products': Product.objects.filter(stock=0).count(),
            'average_price': Product.objects.filter(available=True).aggregate(avg_price=Avg('price'))['avg_price'] or 0,
            'total_categories': Category.objects.annotate(
                active_product_count=Count('products', filter=Q(products__available=True))
            ).filter(active_product_count__gt=0).count()
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
# CATEGORY VIEWS
# =================================
def categories_view(request):
    """
    Bütün kateqoriyalar səhifəsi
    """
    try:
        # Əsas kateqoriyalar (parent olmayan)
        main_categories = Category.objects.filter(
            parent__isnull=True
        ).prefetch_related(
            'children__products'
        ).annotate(
            total_products=Count('products', filter=Q(products__available=True)) +
                          Count('children__products', filter=Q(children__products__available=True))
        ).filter(total_products__gt=0).order_by('name')

        # Ümumi statistikalar
        category_stats = {
            'total_categories': Category.objects.count(),
            'main_categories_count': main_categories.count(),
            'total_products': Product.objects.filter(available=True).count(),
        }

        context = {
            'main_categories': main_categories,
            'category_stats': category_stats,
            'page_title': 'Kateqoriyalar',
            'meta_description': 'drop.az məhsul kateqoriyaları - bütün kateqoriyalarımızı incələyin və uyğun məhsulları tapın'
        }
        
        logger.info(f"Categories page loaded with {main_categories.count()} main categories")
        return render(request, 'catalog/categories.html', context)
        
    except Exception as e:
        logger.error(f"Error in categories_view: {str(e)}")
        messages.error(request, 'Kateqoriyalar yüklənərkən xəta baş verdi.')
        return render(request, 'catalog/categories.html', {'main_categories': [], 'category_stats': {}})

def category_detail(request, slug):
    """
    Spesifik kateqoriya səhifəsi və onun məhsulları
    """
    try:
        category = get_object_or_404(Category, slug=slug)
        
        # Bu kateqoriya və alt kateqoriyalarının məhsulları
        if category.children.exists():
            # Ana kateqoriya - özü və uşaqlarının məhsulları
            category_ids = [category.id] + list(category.children.values_list('id', flat=True))
            products = Product.objects.filter(
                category_id__in=category_ids,
                available=True
            ).select_related('category').order_by('-created_at')
            
            # Alt kateqoriyalar
            subcategories = category.children.annotate(
                product_count=Count('products', filter=Q(products__available=True))
            ).filter(product_count__gt=0)
        else:
            # Alt kateqoriya - yalnız öz məhsulları
            products = Product.objects.filter(
                category=category,
                available=True
            ).select_related('category').order_by('-created_at')
            subcategories = None

        # Filtrləmə
        search_query = request.GET.get('search', '').strip()
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )

        # Qiymət aralığı
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

        # Sıralama
        sort_by = request.GET.get('sort', '-created_at')
        valid_sort_options = ['name', '-name', 'price', '-price', 'created_at', '-created_at']
        if sort_by in valid_sort_options:
            products = products.order_by(sort_by)

        # Paginasiya
        paginator = Paginator(products, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Breadcrumb
        breadcrumb = []
        current_cat = category
        while current_cat:
            breadcrumb.insert(0, current_cat)
            current_cat = current_cat.parent

        context = {
            'category': category,
            'subcategories': subcategories,
            'page_obj': page_obj,
            'products': page_obj,
            'breadcrumb': breadcrumb,
            'search_query': search_query,
            'total_products': products.count(),
            'page_title': f'{category.name} - Kateqoriya',
            'meta_description': f'{category.name} kateqoriyasında {products.count()} məhsul - drop.az'
        }
        
        logger.info(f"Category detail loaded: {category.name} with {products.count()} products")
        return render(request, 'catalog/categories.html', context)
        
    except Exception as e:
        logger.error(f"Error in category_detail: {str(e)}")
        messages.error(request, 'Kateqoriya tapılmadı.')
        return redirect('catalog:categories')

def subcategory_detail(request, parent_slug, slug):
    """
    Alt kateqoriya səhifəsi
    """
    try:
        parent_category = get_object_or_404(Category, slug=parent_slug)
        subcategory = get_object_or_404(Category, slug=slug, parent=parent_category)
        
        # Alt kateqoriyanın məhsulları
        products = Product.objects.filter(
            category=subcategory,
            available=True
        ).select_related('category').order_by('-created_at')

        # Filtrləmə və paginasiya (category_detail kimi)
        search_query = request.GET.get('search', '').strip()
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )

        paginator = Paginator(products, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Breadcrumb
        breadcrumb = [parent_category, subcategory]

        context = {
            'category': subcategory,
            'parent_category': parent_category,
            'subcategories': None,
            'page_obj': page_obj,
            'products': page_obj,
            'breadcrumb': breadcrumb,
            'search_query': search_query,
            'total_products': products.count(),
            'page_title': f'{subcategory.name} - {parent_category.name}',
            'meta_description': f'{subcategory.name} alt kateqoriyasında {products.count()} məhsul - drop.az'
        }
        
        return render(request, 'catalog/categories.html', context)
        
    except Exception as e:
        logger.error(f"Error in subcategory_detail: {str(e)}")
        messages.error(request, 'Alt kateqoriya tapılmadı.')
        return redirect('catalog:categories')

def products_by_category(request, category_slug):
    """
    Kateqoriyaya görə məhsul siyahısı (ayrı URL)
    """
    try:
        category = get_object_or_404(Category, slug=category_slug)
        
        # Kateqoriya məhsulları
        products = Product.objects.filter(
            category=category,
            available=True
        ).select_related('category').order_by('-created_at')

        # Product list view-dakı eyni filtrləmə
        search_query = request.GET.get('search', '').strip()
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )

        paginator = Paginator(products, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'category': category,
            'page_obj': page_obj,
            'products': page_obj,
            'search_query': search_query,
            'page_title': f'{category.name} Məhsulları',
            'meta_description': f'{category.name} kateqoriyasından {products.count()} məhsul'
        }
        
        return render(request, 'catalog/product_list.html', context)
        
    except Exception as e:
        logger.error(f"Error in products_by_category: {str(e)}")
        return redirect('catalog:categories')

# =================================
# EXISTING PRODUCT VIEWS (unchanged)
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
        category_slug = request.GET.get('category')
        if category_slug:
            try:
                category = Category.objects.get(slug=category_slug)
                products = products.filter(category=category)
            except Category.DoesNotExist:
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
        paginator = Paginator(products, 12)
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
                'category': category_slug,
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
        ).exclude(id=product.id).order_by('-created_at')[:4]
        
        # Son baxılan məhsullar (session-da saxlanır)
        recently_viewed = request.session.get('recently_viewed', [])
        if product.id not in recently_viewed:
            recently_viewed.insert(0, product.id)
            recently_viewed = recently_viewed[:5]
            request.session['recently_viewed'] = recently_viewed
        
        # Breadcrumb
        breadcrumb = []
        current_cat = product.category
        while current_cat:
            breadcrumb.insert(0, current_cat)
            current_cat = current_cat.parent
        
        context = {
            'product': product,
            'related_products': related_products,
            'breadcrumb': breadcrumb,
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
# AJAX VIEWS - ENHANCED
# =================================
@require_http_methods(["GET"])
def search_suggestions(request):
    """
    AJAX axtarış təklifləri (kateqoriyalar da daxil)
    """
    try:
        query = request.GET.get('q', '').strip()
        suggestions = []
        
        if len(query) >= 2:
            # Məhsul adları
            products = Product.objects.filter(
                name__icontains=query,
                available=True
            ).select_related('category')[:5]
            
            for product in products:
                suggestions.append({
                    'type': 'product',
                    'title': product.name,
                    'subtitle': product.category.name,
                    'url': f'/product/{product.slug}/',
                    'image': product.image.url if product.image else None,
                    'price': str(product.price)
                })
            
            # Kateqoriya adları
            categories = Category.objects.filter(
                name__icontains=query
            ).annotate(
                product_count=Count('products', filter=Q(products__available=True))
            ).filter(product_count__gt=0)[:3]
            
            for category in categories:
                suggestions.append({
                    'type': 'category',
                    'title': category.name,
                    'subtitle': f'{category.product_count} məhsul',
                    'url': f'/categories/{category.slug}/',
                    'image': None,
                    'price': None
                })
        
        return JsonResponse({'suggestions': suggestions})
        
    except Exception as e:
        logger.error(f"Error in search_suggestions: {str(e)}")
        return JsonResponse({'suggestions': []})

@require_http_methods(["GET"])
def get_category_stats(request):
    """
    Kateqoriya statistikaları API
    """
    try:
        stats = {
            'total_categories': Category.objects.count(),
            'main_categories': Category.objects.filter(parent__isnull=True).count(),
            'categories_with_products': Category.objects.annotate(
                product_count=Count('products', filter=Q(products__available=True))
            ).filter(product_count__gt=0).count(),
            'avg_products_per_category': Category.objects.annotate(
                product_count=Count('products', filter=Q(products__available=True))
            ).aggregate(avg_count=Avg('product_count'))['avg_count'] or 0
        }
        
        return JsonResponse({'success': True, 'stats': stats})
        
    except Exception as e:
        logger.error(f"Error in get_category_stats: {str(e)}")
        return JsonResponse({'success': False, 'message': 'Statistikalar alına bilmədi'})

@require_http_methods(["GET"])
def get_category_breadcrumb(request, category_slug):
    """
    Kateqoriya breadcrumb API
    """
    try:
        category = get_object_or_404(Category, slug=category_slug)
        
        breadcrumb = []
        current_cat = category
        while current_cat:
            breadcrumb.insert(0, {
                'name': current_cat.name,
                'slug': current_cat.slug,
                'url': f'/categories/{current_cat.slug}/'
            })
            current_cat = current_cat.parent
        
        return JsonResponse({'success': True, 'breadcrumb': breadcrumb})
        
    except Exception as e:
        logger.error(f"Error in get_category_breadcrumb: {str(e)}")
        return JsonResponse({'success': False, 'message': 'Breadcrumb alına bilmədi'})

@require_http_methods(["GET"])
def get_category_tree(request):
    """
    Kateqoriya ağacı API (navigation üçün)
    """
    try:
        main_categories = Category.objects.filter(
            parent__isnull=True
        ).prefetch_related('children').annotate(
            product_count=Count('products', filter=Q(products__available=True))
        ).filter(product_count__gt=0)
        
        tree = []
        for category in main_categories:
            children = []
            for child in category.children.all():
                child_product_count = child.products.filter(available=True).count()
                if child_product_count > 0:
                    children.append({
                        'name': child.name,
                        'slug': child.slug,
                        'url': f'/categories/{child.slug}/',
                        'product_count': child_product_count
                    })
            
            tree.append({
                'name': category.name,
                'slug': category.slug,
                'url': f'/categories/{category.slug}/',
                'product_count': category.product_count,
                'children': children
            })
        
        return JsonResponse({'success': True, 'tree': tree})
        
    except Exception as e:
        logger.error(f"Error in get_category_tree: {str(e)}")
        return JsonResponse({'success': False, 'message': 'Kateqoriya ağacı alına bilmədi'})

# =================================
# CLASS-BASED VIEWS - ENHANCED
# =================================
class CategoryProductsView(View):
    """
    Kateqoriya məhsulları üçün AJAX view
    """
    
    def get(self, request, category_slug):
        try:
            category = get_object_or_404(Category, slug=category_slug)
            
            products = Product.objects.filter(
                category=category,
                available=True
            ).select_related('category')
            
            # Filtrləmə
            search_query = request.GET.get('search', '').strip()
            if search_query:
                products = products.filter(
                    Q(name__icontains=search_query) | 
                    Q(description__icontains=search_query)
                )
            
            # AJAX sorğusu üçün JSON cavab
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                product_data = []
                for product in products[:20]:
                    product_data.append({
                        'id': product.id,
                        'name': product.name,
                        'price': float(product.price),
                        'image': product.image.url if product.image else None,
                        'slug': product.slug,
                        'stock': product.stock,
                        'available': product.available,
                        'category': product.category.name
                    })
                
                return JsonResponse({
                    'success': True,
                    'products': product_data,
                    'total_count': products.count(),
                    'category': {
                        'name': category.name,
                        'slug': category.slug
                    }
                })
            
            return JsonResponse({'success': False, 'message': 'AJAX sorğusu tələb olunur'})
            
        except Exception as e:
            logger.error(f"Error in CategoryProductsView: {str(e)}")
            return JsonResponse({'success': False, 'message': 'Kateqoriya məhsulları alına bilmədi'})

# =================================
# EXISTING VIEWS (kept unchanged)
# =================================
@require_http_methods(["POST"])
@csrf_exempt
def newsletter_subscribe(request):
    """Newsletter abunəliyi"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        
        if not email:
            return JsonResponse({'success': False, 'message': 'E-mail tələb olunur'})
        
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return JsonResponse({'success': False, 'message': 'Düzgün e-mail daxil edin'})
        
        try:
            send_mail(
                subject='drop.az Newsletter Abunəliyi',
                message=f'Yeni abunəlik: {email}',
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@drop.az'),
                recipient_list=[getattr(settings, 'ADMIN_EMAIL', 'admin@drop.az')],
                fail_silently=False,
            )
        except:
            pass
        
        logger.info(f"Newsletter subscription: {email}")
        return JsonResponse({'success': True, 'message': 'Uğurla abunə oldunuz! 🎉'})
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Yanlış format'})
    except Exception as e:
        logger.error(f"Error in newsletter_subscribe: {str(e)}")
        return JsonResponse({'success': False, 'message': 'Xəta baş verdi'})

@require_http_methods(["GET"])
def get_product_stats(request):
    """Məhsul statistikaları API"""
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

class ProductFilterView(View):
    """Məhsul filtrlənməsi üçün class-based view"""
    
    def get(self, request):
        try:
            filters = {'available': True}
            
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
            
            products = Product.objects.filter(**filters).select_related('category')
            
            if search_query:
                products = products.filter(
                    Q(name__icontains=search_query) | 
                    Q(description__icontains=search_query)
                )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                product_data = []
                for product in products[:20]:
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
# HERO VERSIONS & UTILITY FUNCTIONS
# =================================
def product_list_hero(request):
    """Hero versiyası - Məhsul siyahısı"""
    try:
        products = Product.objects.filter(available=True).select_related('category').order_by('-created_at')
        
        search_query = request.GET.get('search', '').strip()
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
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
        
        related_products = Product.objects.filter(
            category=product.category,
            available=True
        ).exclude(id=product.id).order_by('-created_at')[:4]
        
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

def sitemap_view(request):
    """XML sitemap generator"""
    try:
        from django.urls import reverse
        from django.utils import timezone
        
        urls = []
        
        urls.append({
            'location': request.build_absolute_uri(reverse('catalog:home')),
            'lastmod': timezone.now(),
            'changefreq': 'daily',
            'priority': '1.0'
        })
        
        # Kateqoriyalar
        categories = Category.objects.all()
        for category in categories:
            urls.append({
                'location': request.build_absolute_uri(f'/categories/{category.slug}/'),
                'lastmod': timezone.now(),
                'changefreq': 'weekly',
                'priority': '0.8'
            })
        
        # Məhsullar
        products = Product.objects.filter(available=True)
        for product in products:
            urls.append({
                'location': request.build_absolute_uri(f'/product/{product.slug}/'),
                'lastmod': product.updated_at,
                'changefreq': 'weekly',
                'priority': '0.7'
            })
        
        xml_content = render(request, 'sitemap.xml', {'urls': urls}, content_type='application/xml')
        return xml_content
        
    except Exception as e:
        logger.error(f"Error generating sitemap: {str(e)}")
        return HttpResponse('<?xml version="1.0" encoding="UTF-8"?><urlset></urlset>', content_type='application/xml')

def handler404(request, exception):
    """404 səhifəsi"""
    return render(request, 'errors/404.html', {
        'page_title': 'Səhifə tapılmadı',
        'error_code': '404'
    }, status=404)

def handler500(request):
    """500 səhifəsi"""
    return render(request, 'errors/500.html', {
        'page_title': 'Server xətası',
        'error_code': '500'
    }, status=500)