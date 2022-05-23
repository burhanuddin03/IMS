from django.urls import path,include
from . import views


app_name = "Product_app"

urlpatterns = [
    path('',views.ProductAddView.as_view(),name="addproduct"),
    path('categories/',views.CategoryAddView.as_view(),name="addcategories"),
    path('brands/',views.BrandAddView.as_view(),name="addbrands"),
    path('lists/',views.ProductListView.as_view(),name="productlist"),
    path('delete/<int:pk>/',views.DeleteProductView.as_view(),name="product_delete"),
    path('update/<int:pk>/',views.ProductUpdateView.as_view(),name="product_update"),
    path('product-variance-add/',views.ProductVarianceAddView.as_view(),name='product_variance'),
    path('get-product-variance/',views.get_particular_variance,name='get_product_variance'),
    path('delete-category/',views.delete_category,name='delete_category'),
    path('delete-brand/',views.delete_brand,name='delete_brand')
]