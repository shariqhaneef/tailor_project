from django.contrib import admin
from .models import ServicePrice, PortfolioItem, Category

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'base_price', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('category',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_emoji', 'base_starting_price', 'is_active', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(ServicePrice)