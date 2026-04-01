from rest_framework import serializers
from .models import Product,Inventory
import re
from django.db.transaction import atomic


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model =Inventory
        fields = ["stock","reorder_level"]
    
    
class ProductSerializers(serializers.ModelSerializer):
    inventory = InventorySerializer()
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "image",
            "inventory"
        ]
        
    def validate(self,attr):
        pattern = r"^.{5,}$"
        if not re.match(pattern,attr['name']):
            raise serializers.ValidationError("product name should not be empty")
        return attr
        
        
    def create(self, validated_data):
        request = self.context.get('request')
        seller = request.user
        inventory_data = validated_data.pop('inventory')
        print(inventory_data)
        
        with atomic():
            product =  Product.objects.create(
            name=validated_data.get('name'),
            description = validated_data.get("description"),
            price = validated_data.get("price"),
            image = validated_data.get("image")
            )
        
        
            stock = inventory_data.get('stock')
            reorder_level = inventory_data.get('reorder_level')
            inventory = Inventory.objects.create(
            seller = seller,
            product = product,
            stock = stock,
            reorder_level =reorder_level
            )
            
        return product
    
    
    
class SaleSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField()
    
    def validate(self, attrs):
        if attrs['quantity']<1:
            raise serializers.ValidationError("order Quantity must be atleast 1")
        return attrs