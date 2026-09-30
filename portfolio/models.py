from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    base_starting_price = models.DecimalField(max_digits=8, decimal_places=2, default=1299.00)
    icon_emoji = models.CharField(max_length=10, default="👔", help_text="Emoji icon for studio UI")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.icon_emoji} {self.name}"

    class Meta:
        verbose_name_plural = "Categories"

class PortfolioItem(models.Model):
    title = models.CharField(max_length=200)
    # Replace old string category field with a ForeignKey relationship
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='items')
    base_price = models.DecimalField(max_digits=8, decimal_places=2, default=1299.00)
    mrp = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    description = models.TextField()
    
    # Images for 360 rotation & reel
    image = models.ImageField(upload_to='portfolio_images/')
    image2 = models.ImageField(upload_to='portfolio_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='portfolio_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='portfolio_images/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class ServicePrice(models.Model):
    garment_name = models.CharField(max_length=100) # e.g., Custom Suit, Shirt, Trouser
    description = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    estimated_time = models.CharField(max_length=50, blank=True, null=True) # e.g., "3-5 Business Days"
    image = models.ImageField(upload_to='pricing/', blank=True, null=True)

    def __str__(self):
        return f"{self.garment_name} - ₹{self.base_price}"



