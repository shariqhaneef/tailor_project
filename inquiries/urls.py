from django.urls import path
from . import views


app_name = 'inquiries'

urlpatterns = [
    # Forms & Orders
    path('inquiry_form/', views.inquiry_create_view, name='inquiry_form'),
    path('custom-order/', views.inquiry_create_view, name='custom_order'),
    path('custom-tailoring/', views.custom_tailoring_view, name='custom_tailoring'),
    path('contact/', views.contact_view, name='contact'),

    # Dashboards & Updates
    path('dashboard/', views.dashboard_view, name='tailor_dashboard'),
    path('dashboard/update/<int:pk>/', views.OrderUpdateView.as_view(), name='order_update'),
    path('client-orders/<int:pk>/update/', views.ClientOrderUpdateView.as_view(), name='client_order_update'),
    path('reply/<int:inquiry_id>/', views.send_reply, name='send_reply'),
    path('client-reply/<int:inquiry_id>/', views.client_send_reply, name='client_send_reply'),
    path('claim-order/<int:pk>/', views.claim_order, name='claim_order'),
    
]