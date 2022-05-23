from django.contrib import admin
from .models import SalesInvoice,ProductSalesDetail
# Register your models here.
admin.site.register(SalesInvoice)
admin.site.register(ProductSalesDetail)