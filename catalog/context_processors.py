# catalog/context_processors.py
from django.db.models import Q, Count
import logging

from .models import Category

logger = logging.getLogger(__name__)

def categories_context(request):
    """
    Header üçün kateqoriyalar və global məlumatları bütün template-lərə göndərir
    """
    try:
        # Header üçün əsas kateqoriyalar (maksimum 6 əsas kateqoriya)
        header_categories = Category.objects.filter(
            parent__isnull=True  # Yalnız əsas kateqoriyalar
        ).prefetch_related('children').annotate(
            active_product_count=Count(
                'products',
                filter=Q(products__available=True)
            )
        ).filter(
            active_product_count__gt=0  # Yalnız məhsulu olan kateqoriyalar
        ).order_by('name')[:6]  # Maksimum 6 əsas kateqoriya
        
        # Hər kateqoriya üçün əlavə məlumat
        categories_data = []
        for category in header_categories:
            children = category.children.annotate(
                active_product_count=Count(
                    'products',
                    filter=Q(products__available=True)
                )
            ).filter(active_product_count__gt=0)[:5]  # Maksimum 5 alt kateqoriya
            
            categories_data.append({
                'category': category,
                'children': children,
                'has_children': children.exists()
            })
        
        # Ümumi statistikalar
        total_categories_count = Category.objects.annotate(
            active_product_count=Count(
                'products',
                filter=Q(products__available=True)
            )
        ).filter(active_product_count__gt=0).count()
        
        return {
            'header_categories': categories_data,
            'total_categories_count': total_categories_count
        }
        
    except Exception as e:
        logger.error(f"Error in categories_context: {str(e)}")
        return {
            'header_categories': [],
            'total_categories_count': 0
        }