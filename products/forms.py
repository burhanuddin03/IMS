from django import forms
from . import models
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
from django.shortcuts import get_object_or_404
from django.conf import settings


class CategoryAddForm(forms.ModelForm):

    class Meta:
        model=models.Category
        fields='__all__'

        widgets={
            'Category_name':forms.TextInput(attrs={'class':'form-control input-md','id':'product_cat','placeholder':'Product Category'})
        }

    
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['Category_name'].help_text='Note that the field is case-insensitive.'

    def clean_Category_name(self):
        cat_name=self.cleaned_data['Category_name']
        if models.Category.objects.filter(Category_name__iexact=cat_name).exists():
            raise forms.ValidationError('Category with this Category name already exist.')
        return cat_name

class VarianceAddForm(forms.ModelForm):

    class Meta:
        model=models.VarianceType
        fields='__all__'

        widgets={
            'variance_name':forms.TextInput(attrs={'class':'form-control input-md','id':'product_cat','placeholder':'Variance Type'})
        }

    
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['variance_name'].help_text='Note that the field is case-insensitive.'

    def clean_variance_name(self):
        var_name=self.cleaned_data['variance_name']
        if models.VarianceType.objects.filter(variance_name__iexact=var_name).exists():
            raise forms.ValidationError('Such Product Variance already exists..')
        return var_name

class BrandAddForm(forms.ModelForm):

    class Meta:
        model=models.Brand
        fields='__all__'

        widgets={
            'Brand_name':forms.TextInput(attrs={'class':'form-control input-md','id':'product_brand','placeholder':'Product Brand'})
        }

    
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['Brand_name'].help_text='Note that the field is case-insensitive.'    

    def clean_Brand_name(self):
        brand_name=self.cleaned_data['Brand_name']
        if models.Brand.objects.filter(Brand_name__iexact=brand_name).exists():
            raise forms.ValidationError('Brand with this name already exist.')
        return brand_name

class ProductAddForm(forms.ModelForm):
    Manufacturing_date=forms.DateField(widget=forms.DateInput(attrs={'class':'form-control input-md','value':'','id':'manufacturing_date','placeholder':'dd/mm/yyyy','step':'1'}),input_formats=settings.DATE_INPUT_FORMATS,required=False)
    Expiry_date=forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,widget=forms.DateInput(attrs={'class':'form-control input-md','value':'','id':'expiry_date','placeholder':'dd/mm/yyyy','step':'1'}),required=False)

    class Meta:
        model=models.Product
        exclude=('Barcode','variances')

        widgets={
            'Product_Code':forms.TextInput(attrs={'class':'form-control input-md','id':'product_id','placeholder':'Product Code'}),
	        'Product_name':forms.TextInput(attrs={'class':'form-control input-md','id':'product_name','placeholder':'Product Name'}),
            'Product_Category':forms.Select(attrs={'class':'select2bs4 select2 form-control','id':'product_categorie'}),
            'Product_Brand':forms.Select(attrs={'class':'select2bs4 select2 form-control','id':'product_brand'}),
            'Quantity': forms.NumberInput(attrs={'class':'form-control input-md','id':'available_quantity','placeholder':'Quantity','step':'1'}),
            'Product_Desc':forms.Textarea(attrs={'class':'form-control input-md','id':'product_description','placeholder':'Description'}),
            'Purchase_price':forms.NumberInput(attrs={'class':'form-control','placeholder':'Purchase Price'}),
            'Selling_price':forms.NumberInput(attrs={'class':'form-control','placeholder':'Sell Price'}),
            'Product_Image':forms.FileInput(attrs={'id':'user_userimage'})
        }

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Product_Desc'].label='Description'
        self.fields['Product_Code'].help_text='Note that the field is case-sensitive'
        self.fields['Quantity'].help_text='Note: Products having Zero quantity wont be able to add in Sales invoice.'
    
    def save(self,commit=True):
        obj = super().save(commit=True)
        all_variances=self.data.getlist('VNameI')
        all_values=self.data.getlist('VValueI')
        product_name=''
        for i in range(len(all_variances)):
            varn=get_object_or_404(models.VarianceType,variance_name__iexact=all_variances[i])
            pd_varn_obj=models.ProductVariance(product=obj,variance=varn,value=all_values[i])
            product_name+=(' '+all_values[i])
            pd_varn_obj.save()
        
        #barcode generation start
        EAN = barcode.get_barcode_class('ean13')
        ean = EAN(obj.Product_Code,writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        obj.Barcode.save('barcode-{}.png'.format(obj.Product_Code),File(buffer),save=False)
        #end
        
        if product_name!='' or product_name!=' ' :
            obj.Product_name+=product_name
            obj.save()
        
        return obj

    def clean_Quantity(self):
        if self.cleaned_data['Quantity'] == None:
            return 0
        else:
            return self.cleaned_data['Quantity']    


class ProductUpdateForm(ProductAddForm):


    def __init__(self,*args, **kwargs):
        self.product_code=kwargs.pop('product_code',None)
        super().__init__(*args, **kwargs)

    def save(self,commit=True):
        obj=super(ProductAddForm, self).save(commit=False)
        pcode=obj.Product_Code
        all_variances=self.data.getlist('VNameI')
        all_values=self.data.getlist('VValueI')
        queryset_variance=obj.productvariance_set.all()
        if queryset_variance.count()!=0:
            queryset_variance.delete()
        obj.save()

        product_name=''
        for i in range(len(all_variances)):
            varn=get_object_or_404(models.VarianceType,variance_name__iexact=all_variances[i])
            pd_varn_obj=models.ProductVariance(product=obj,variance=varn,value=all_values[i])
            product_name+=('-'+all_values[i])
            pd_varn_obj.save()
        
        if self.product_code!=pcode:
            print('hello')
            #barcode generation start
            EAN = barcode.get_barcode_class('ean13')
            ean = EAN(obj.Product_Code,writer=ImageWriter())
            buffer = BytesIO()
            ean.write(buffer)
            obj.Barcode.save('barcode-{}.png'.format(obj.Product_Code),File(buffer),save=False)
            #end
            
        if product_name!='' or product_name!=' ' :
            name=''
            if '-' in obj.Product_name: 
                name=obj.Product_name.split('-',1)[0]
            else:
                name=obj.Product_name    
            obj.Product_name=name+product_name
            obj.save()
        
        return obj

            






