from django.contrib import admin
from .models import Product,Inventory,Sale
# Register your models here.



# admin.site.register(Product)
# admin.site.register(Inventory)
# admin.site.register(Sale)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','created_at']
    search_fields = ['name']
    ordering = ['created_at']
    
    
    readonly_fields = ['id']
    list_filter =['created_at','price']
    



@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product','seller','stock','reorder_level']
    search_fields = ['product__name','seller__username']
    ordering = ['product__name']
    list_filter = ['stock','reorder_level']
    
    
    
    
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['product','sale_date','quantity_sold']
    search_fields = ['product__name']
    ordering = ['sale_date']
    list_filter = ['sale_date']
    readonly_fields = ['id','sale_date']
    fieldsets =[
        ('Sale Info', {'fields': ['product', 'quantity_sold']}),
    ]
    exclude = ['id']
    add_fieldsets =[
        ('Sale Info', {'fields': ['product', 'quantity_sold']}),
        
    ]