from django.urls import path
from .views import portfolio_home, item_detail, PortfolioCreateView, pricing_view

urlpatterns = [
    path('', portfolio_home, name='portfolio_home'),
    path('<int:item_id>/', item_detail, name='item_detail'),
    path('add/', PortfolioCreateView.as_view(), name='portfolio_add'),
    path('pricing/', pricing_view, name='pricing'),
]


