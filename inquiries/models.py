from django.db import models
from django.contrib.auth.models import User

class Inquiry(models.Model):
    # Basic Contact & Customer Fields
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Links & Status
    customer = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='customer_orders'
    )
    
    # Tailor Assignment (Restricted to staff members)
    assigned_tailor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tailor_orders',
        limit_choices_to={'is_staff': True}
    )

    item = models.ForeignKey('portfolio.PortfolioItem', on_delete=models.SET_NULL, null=True, blank=True)
    
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Cutting', 'Cutting'),
        ('Stitching', 'Stitching'),
        ('Completed', 'Completed'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    reference_image = models.ImageField(upload_to='inquiry_references/', blank=True, null=True)
    internal_notes = models.TextField(blank=True, null=True)

    # Categories & Measurements
    CATEGORY_CHOICES = (
        ('Shirt', 'Shirt'),
        ('Pants', 'Pants'),
        ('Suit', 'Suit'),
    )
    item_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    
    chest = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 40 inches")
    inseam = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 32 inches")

    def __str__(self):
        tailor = self.assigned_tailor.username if self.assigned_tailor else "Unassigned"
        return f"Order #{self.id} from {self.name} - {self.subject} (Tailor: {tailor})"


class InquiryReply(models.Model):
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, related_name='replies')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply to {self.inquiry.subject} by {self.sender.username}"