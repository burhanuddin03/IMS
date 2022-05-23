from django.contrib import admin
from .models import Brand,Category,Product,VarianceType,ProductVariance
# Register your models here.
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(VarianceType)
admin.site.register(ProductVariance)


