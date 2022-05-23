from django.db import models
import uuid
from django.utils import timezone
import os

def get_image_file_name(instance,filename):

    ext=filename.split('.')[-1]
    filename="{}.{}".format(uuid.uuid4(),ext)

    return os.path.join('product_images/',filename)

class Category(models.Model):
	Category_name = models.CharField(max_length=250,blank=False,unique=True)

	def __str__(self):
		return self.Category_name


class Brand(models.Model):
	Brand_name = models.CharField(max_length=250,blank=False,unique=True)

	def __str__(self):
		return self.Brand_name

class VarianceType(models.Model):
	variance_name=models.CharField(max_length=100,blank=False,unique=True)

	def __str__(self):
		return self.variance_name


class Product(models.Model):
	Product_Code = models.CharField(blank=False,unique=True,max_length=50)
	Product_name = models.CharField(blank=False,max_length=250)
	Product_Category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='pro_cat')
	Product_Brand = models.ForeignKey(Brand,on_delete=models.CASCADE,related_name='pro_brand')
	Quantity = models.PositiveIntegerField(default=0,blank=True)
	Manufacturing_date = models.DateField(blank=True,null=True)
	variances=models.ManyToManyField(VarianceType,through='ProductVariance')
	Expiry_date = models.DateField(blank=True,null=True)
	Product_Desc = models.TextField(blank=True)
	Purchase_price = models.DecimalField(max_digits=19, decimal_places=10,blank=False)
	Selling_price = models.DecimalField(max_digits=19, decimal_places=10,blank=False)
	Product_Image = models.ImageField(upload_to=get_image_file_name,blank=True,null=True)
	Barcode = models.ImageField(upload_to='barcodes',blank=True)

	def __str__(self):
		return self.Product_Code

class ProductVariance(models.Model):
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	variance=models.ForeignKey(VarianceType,on_delete=models.SET_NULL,null=True)
	value=models.CharField(max_length=100,blank=False)

	def __str__(self):
		return self.product.Product_Code
	
	

