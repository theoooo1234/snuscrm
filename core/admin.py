from django.contrib import admin
from .models import Company, Product, Variant, Order, OrderLine

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "created_at")
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ("sku", "product", "strength_mg_g", "stock_units", "price")
    list_filter = ("product",)
    search_fields = ("sku",)

class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "status", "created_at")
    list_filter = ("status",)
    inlines = [OrderLineInline]