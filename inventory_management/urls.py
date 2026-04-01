from django.urls import path
from .views import ProductView,SaleView

urlpatterns = [
    path("addproduct/",ProductView.as_view(),name='addproduct'),
    path("showproduct/",ProductView.as_view(),name='showproduct'),
    path("showproduct/<uuid:id>/",ProductView.as_view(),name='showoneproduct'),
    
    path("saleproduct/",SaleView.as_view()),
    path("showsales/",SaleView.as_view())
]
