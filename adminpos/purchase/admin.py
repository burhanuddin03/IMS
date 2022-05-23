from django.contrib import admin
from .models import PurchaseInvoice,ProductPurchaseDetail
# Register your models here.
admin.site.register(PurchaseInvoice)
admin.site.register(ProductPurchaseDetail)