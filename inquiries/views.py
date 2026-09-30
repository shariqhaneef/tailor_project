from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from django.db import models

from .models import Inquiry, InquiryReply
from .forms import InquiryForm, ContactForm


# ==========================================
# 1. SMART DUAL-ROLE DASHBOARD ROUTER
# ==========================================
@login_required
def dashboard_view(request):
    """
    Directs Tailors (is_staff=True) to the Workshop Workbench,
    and Customers (is_staff=False) to their Client Hub.
    """
    if request.user.is_staff:
        all_inquiries = Inquiry.objects.prefetch_related('replies').all().order_by('-created_at')
        orders = all_inquiries.filter(item_category__isnull=False).exclude(item_category='')
        contact_messages = all_inquiries.filter(models.Q(item_category__isnull=True) | models.Q(item_category=''))
        
        context = {
            'orders': orders,
            'contact_messages': contact_messages,
            'all_inquiries': all_inquiries,
        }
        return render(request, 'inquiries/tailor_dashboard.html', context)

    # Customer Profile Update Handler
    if request.method == 'POST' and 'update_profile' in request.POST:
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, 'Your profile details have been saved successfully.')
        return redirect('dashboard')

    customer_orders = Inquiry.objects.filter(customer=request.user).prefetch_related('replies').order_by('-created_at')
    return render(request, 'users/dashboard.html', {'orders': customer_orders})


# ==========================================
# 2. INQUIRY & ORDER CREATION VIEWS
# ==========================================
def inquiry_create_view(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST, request.FILES)
        if form.is_valid():
            inquiry = form.save(commit=False)
            if request.user.is_authenticated:
                inquiry.customer = request.user
                if not inquiry.name:
                    inquiry.name = request.user.get_full_name() or request.user.username
                if not inquiry.email:
                    inquiry.email = request.user.email
            inquiry.save()
            messages.success(request, 'Your bespoke request was submitted! TailorCraft will contact you soon.')
            return redirect('dashboard' if request.user.is_authenticated else 'home')
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'name': request.user.get_full_name() or request.user.username,
                'email': request.user.email,
            }
        form = InquiryForm(initial=initial_data)

    return render(request, 'inquiries/inquiry_form.html', {'form': form})


@login_required
def custom_tailoring_view(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST, request.FILES)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.customer = request.user
            if not inquiry.name:
                inquiry.name = request.user.get_full_name() or request.user.username
            if not inquiry.email:
                inquiry.email = request.user.email
            inquiry.save()
            return redirect('dashboard')
    else:
        form = InquiryForm(initial={'email': request.user.email, 'name': request.user.username})

    return render(request, 'inquiries/custom_tailoring.html', {'form': form})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save(commit=False)
            # Ensure it's registered as a direct consultation
            contact_msg.save()
            messages.success(request, "Consultation inquiry successfully transmitted to the master tailor's desk.")
            return redirect('inquiries:contact')
    else:
        form = ContactForm(initial={
            'name': request.user.get_full_name() or request.user.username if request.user.is_authenticated else '',
            'email': request.user.email if request.user.is_authenticated else '',
        })

    context = {
        'form': form,
    }
    return render(request, 'inquiries/contact.html', context)


# ==========================================
# 3. TAILOR WORKBENCH & ORDER CONTROLS
# ==========================================
class TailorDashboardView(UserPassesTestMixin, ListView):
    model = Inquiry
    template_name = 'inquiries/tailor_dashboard.html'
    context_object_name = 'all_inquiries'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return Inquiry.objects.prefetch_related('replies').all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        context['orders'] = qs.filter(item_category__isnull=False).exclude(item_category='')
        context['contact_messages'] = qs.filter(models.Q(item_category__isnull=True) | models.Q(item_category=''))
        return context


class OrderUpdateView(UserPassesTestMixin, UpdateView):
    model = Inquiry
    fields = ['status', 'internal_notes']
    template_name = 'inquiries/tailor_order_update.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        return self.request.user.is_staff


class ClientOrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Inquiry
    fields = ['item_category', 'chest', 'inseam', 'subject', 'message']
    template_name = 'inquiries/client_order_update.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        # Allow customers to edit metrics only while status is Pending
        return Inquiry.objects.filter(customer=self.request.user, status='Pending')


@login_required
def send_reply(request, inquiry_id):
    if not request.user.is_staff:
        messages.error(request, "Access restricted to master artisans.")
        return redirect('dashboard')
        
    inquiry = get_object_or_404(Inquiry, pk=inquiry_id)
    
    if request.method == 'POST':
        reply_text = request.POST.get('reply_text')
        if reply_text:
            InquiryReply.objects.create(
                inquiry=inquiry,
                sender=request.user,
                reply_text=reply_text
            )
            messages.success(request, f"Fitting response sent to client for Order #{inquiry.id}.")
            
    return redirect('dashboard')

@login_required
def claim_order(request, pk):
    if not request.user.is_staff:
        return redirect('dashboard')
    order = get_object_or_404(Inquiry, pk=pk)
    order.assigned_tailor = request.user
    order.save()
    messages.success(request, f'Order #{order.id} has been claimed to your workbench.')
    return redirect('dashboard')

@login_required
def client_send_reply(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id, customer=request.user)
    
    if request.method == 'POST':
        reply_text = request.POST.get('reply_text')
        if reply_text:
            InquiryReply.objects.create(
                inquiry=inquiry,
                sender=request.user,
                reply_text=reply_text
            )
            messages.success(request, "Your message has been sent to the tailor's desk.")
            
    return redirect('dashboard')