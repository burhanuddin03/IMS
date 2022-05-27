from django.urls import path,include
from . import views

app_name = "purchase_app"

urlpatterns=[
	path('',views.PurchaseInvoiceView,name="purchaseinvoice"),
	path('getproduct/',views.GetProductCode,name="getproduct"),
    path('getproductcode/',views.GetProductDetailsView,name='getproductdetails'),
    path('getproductname/',views.GetProductNameView,name='getproductnames'),
    path('getproductcode-name/',views.GetProductCodeName,name='getproductcodename'),
    path('list/',views.PurchaseInvoiceList.as_view(),name="purchase_list"),
    path('delete/<int:pk>/',views.DeleteProductView.as_view(),name="purchase_delete"),
    path('list/<int:pk>/invoice_detail/',views.PurchaseInvoiceDetailView.as_view(),name="purchase_invoice_detail"),
    path('list/<int:pk>/invoice_detail/pdf/',views.GeneratePdf.as_view(),name="invoice_pdf_create"),
    path('purchase-invoice/<int:pk>/update/',views.purchaseinvoiceupdate,name='purchase_update')

]