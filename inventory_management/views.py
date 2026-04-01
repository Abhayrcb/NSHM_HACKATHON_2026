from django.shortcuts import render
from rest_framework.views import APIView

from inventory_management.context_processors import get_sales_data
from .serializers import ProductSerializers,SaleSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsSeller
from .models import Product,Sale,Inventory

from django.db import transaction
# Create your views here.


class ProductView(APIView):
    # permission_classes = [IsAuthenticatedOrReadOnly,IsSeller]
    def post(self,request):
        serializer = ProductSerializers(data=request.data,context={'request':request})
        
        if serializer.is_valid():
            product = serializer.save()
            res= {
                "success":True,
                "message":"Successfully added",
                "data":serializer.data,
                "errors":None
            }
            return Response(res,status=status.HTTP_201_CREATED)
        res= {
                "success":False,
                "message":"Object Cretaion Failed",
                "data":None,
                "errors":serializer.errors
            }
        return Response(res,status=status.HTTP_403_FORBIDDEN)
    
    def get(self,request,id=None):
        if id:
            product = Product.objects.select_related('inventory').get(id=id)
            serializer = ProductSerializers(product)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        products = Product.objects.select_related('inventory')
        serializer = ProductSerializers(products,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
    
    
class SaleView(APIView):
    def post(self,request):
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            id = serializer.validated_data.get('product_id')
            quantity = serializer.validated_data.get('quantity')
            
            with transaction.atomic():
                product = Product.objects.select_related('inventory').get(id=id)
                
                if product.inventory.stock <= 0 or product.inventory.stock < quantity:
                    return Response({"message":"we don't have enough stock"})
                
        
                sale = Sale.objects.create(
                    product=product,
                    quantity_sold = quantity
                )
                product.inventory.stock -= quantity
                product.inventory.save()
            return Response({"message":"order placed successfully"})
        
        return Response({"message":serializer.errors})
    
    def get(self,request):
        res = get_sales_data()
        return Response(res['sales_data'],status=status.HTTP_200_OK)
        