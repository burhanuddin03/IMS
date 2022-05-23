from django.urls import path,include
from . import views

app_name = "sales_app"

urlpatterns=[
   path('',views.SaleInvoiceView,name="saleinvoice"),
   path('getproduct/',views.GetProductCode,name="getproduct"),
   path('getproductcode/',views.GetProductDetailsView,name='getproductdetails'),
   path('getproductname/',views.GetProductNameView,name='getproductnames'),
   path('getproductcode-name/',views.GetProductCodeName,name='getproductcodename'),
   path('list/',views.SaleInvoiceList.as_view(),name="sales_list"),
   path('delete/<int:pk>/',views.DeleteProductView.as_view(),name="sales_delete"),
   path('list/<int:pk>/invoice_detail/',views.SaleInvoiceDetailView.as_view(),name="sales_invoice_detail"),
   path('list/<int:pk>/invoice_detail/pdf/',views.GeneratePdf.as_view(),name="invoice_pdf_create"),
   path('sales-update/<int:pk>/',views.salesinvoiceupdateview,name='sales_update')


]