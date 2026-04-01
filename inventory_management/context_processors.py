from .models import Product,Sale
from django.db.models import Sum

def get_sales_data():
        products=Product.objects.select_related('inventory').select_related('inventory__seller').all()
        
        res = []
        for product in products:
            sales = Sale.objects.values('sale_date').annotate(total_sold=Sum('quantity_sold')).filter(product=product).order_by('sale_date')
            sales_data = []
            
            for sale in sales:
                sales_data.append({
                    "quantity_sold":sale['total_sold'],
                    "sale_date":sale['sale_date']
                })
            res.append({
                "product_name":product.name,
                "seller_id":product.inventory.seller.id,
                "seller_name":product.inventory.seller.username,
                "seller_email":product.inventory.seller.email,
                "sales":sales_data
            })
        return {"sales_data":res}