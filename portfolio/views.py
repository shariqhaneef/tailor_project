from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import PortfolioItem, Category, ServicePrice

class PortfolioCreateView(UserPassesTestMixin, CreateView):
    model = PortfolioItem
    fields = '__all__' 
    template_name = 'portfolio/portfolio_add.html'
    success_url = '/portfolio/' 
    
    def test_func(self):
        # Security: Only staff/master artisans can upload portfolio items
        return self.request.user.is_staff

def portfolio_home(request):
    category_slug = request.GET.get('category')
    categories = Category.objects.filter(is_active=True)
    
    # Filter items dynamically if a category is selected
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        items = PortfolioItem.objects.filter(category=active_category)
    else:
        active_category = None
        items = PortfolioItem.objects.all()

    context = {
        'items': items,
        'categories': categories,
        'active_category': active_category,
    }
    return render(request, 'portfolio/home.html', context)

def item_detail(request, item_id):
    item = get_object_or_404(PortfolioItem, id=item_id)
    return render(request, 'portfolio/item_detail.html', {'item': item})

def pricing_view(request):
    services = ServicePrice.objects.all()
    categories = Category.objects.filter(is_active=True)
    context = {
        'services': services,
        'categories': categories,
    }
    return render(request, 'portfolio/pricing.html', context)