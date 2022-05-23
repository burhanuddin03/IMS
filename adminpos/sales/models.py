from django.db import models
from products.models import Product 
# Create your models here.

class SalesInvoice(models.Model):
	Invoiceno = models.CharField(blank=False,unique=True,max_length=50)
	Products = models.ManyToManyField(Product, through='ProductSalesDetail')
	Customername = models.CharField(blank=False,max_length=250)
	Invoicedate = models.DateField(blank=False)
	CustomerEmail = models.EmailField(blank=True)
	Contactno = models.CharField(blank=True,max_length=12)
	Address = models.TextField(blank=True)
	Invoicetype = models.CharField(blank=False,max_length=50)
	SubTotal = models.DecimalField(max_digits=19, decimal_places=10,blank=False)
	Discount = models.PositiveIntegerField(blank=True,default=0)
	Tax = models.DecimalField(max_digits=19, decimal_places=10,blank=True,default=0)
	Shippingcharge = models.PositiveIntegerField(blank=True,default=0)

	def __str__(self):
		return self.Invoiceno



class ProductSalesDetail(models.Model):
	Invoiceno = models.ForeignKey(SalesInvoice,on_delete=models.CASCADE,related_name='productdetail')
	Pcode = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
	product_name=models.CharField(blank=False,max_length=250)
	product_code=models.CharField(blank=False,max_length=50,default="")
	product_desc=models.TextField(blank=True)
	Price = models.DecimalField(max_digits=19, decimal_places=10,blank=False)
	SaleQuantity = models.PositiveIntegerField(blank=False)
	Discount = models.PositiveIntegerField(blank=True,default=0)

	def __str__(self):
		return self.Invoiceno.Invoiceno
