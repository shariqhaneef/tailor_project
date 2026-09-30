from django import forms
from django.contrib.auth import get_user_model
from portfolio.models import Category
from .models import Inquiry

User = get_user_model()  # <--- This fixes the NameError

class InquiryForm(forms.ModelForm):
    item_category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        empty_label="Select Garment Silhouette",
        widget=forms.Select(attrs={'class': 'form-select studio-input'})
    )

    assigned_tailor = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True),
        required=False,
        empty_label="Any Available Master Artisan",
        widget=forms.Select(attrs={'class': 'form-select studio-input'})
    )

    class Meta:
        model = Inquiry
        fields = ['item_category', 'assigned_tailor', 'name', 'email', 'phone', 'chest', 'inseam', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us what you are looking for...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.setdefault('class', 'form-control studio-input')


class ContactForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us what you are looking for...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.setdefault('class', 'form-control studio-input')