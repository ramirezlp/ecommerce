from django.urls import path
from .views import HomePage
from .views import ProductDetailView, CategoryProductDetailView


app_name = "products"

urlpatterns = [
    path('', HomePage.as_view(), name='home-page'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('category/<int:pk>/<str:ordering>' , CategoryProductDetailView.as_view(), name='category-product-detail')
]
