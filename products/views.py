from django.shortcuts import render,redirect
from .models import Brand,Category,Product,VarianceType
from .forms import BrandAddForm,CategoryAddForm,ProductAddForm,VarianceAddForm,ProductUpdateForm
from django.views.generic import CreateView,ListView,DeleteView,UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
import datetime
from django.core import serializers
from django.http import JsonResponse
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required
# Create your views here.

class ProductAddView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    template_name='AdminPos/ProductAdd.html'
    success_url=reverse_lazy('Product_app:addproduct')
    form_class=ProductAddForm
    success_message='%(Product_Code)s was successfully added!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variances']=VarianceType.objects.all()
        return context

class ProductVarianceAddView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    template_name='AdminPos/ProductVarianceAdd.html'
    success_url=reverse_lazy('Product_app:product_variance')
    form_class=VarianceAddForm
    success_message='%(variance_name)s was successfully added!'

class CategoryAddView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    template_name='AdminPos/ProductCat.html'
    success_url=reverse_lazy('Product_app:addcategories')
    form_class=CategoryAddForm
    success_message='%(Category_name)s was successfully added!'

@login_required
def delete_category(request):
    if request.method=='POST':
        name=request.POST['Category_name']
        obj=None
        try:
            obj=Category.objects.get(Category_name__iexact=name)
        except:
            obj=None
        if obj==None:
            messages.error(request,'Category doesnot exists with this name')
            return redirect('Product_app:addcategories')
        else:
            obj.delete()
            messages.success(request,'Category deleted with this name')
            return redirect('Product_app:addcategories')
    else:
        raise Http404()


class BrandAddView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    template_name='AdminPos/ProductBrand.html'
    success_url=reverse_lazy('Product_app:addbrands')
    form_class=BrandAddForm
    success_message='%(Brand_name)s was successfully added!'

@login_required
def delete_brand(request):
    if request.method=='POST':
        name=request.POST['Brand_name']
        obj=None
        try:
            obj=Brand.objects.get(Brand_name__iexact=name)
        except:
            obj=None
        if obj==None:
            messages.error(request,'Brand doesnot exists with this name')
            return redirect('Product_app:addbrands')
        else:
            obj.delete()
            messages.success(request,'Brand deleted with this name')
            return redirect('Product_app:addbrands')
    else:
        raise Http404()    
    
class ProductListView(LoginRequiredMixin,ListView):
    #paginate_by = 8
    model=Product
    template_name="AdminPos/ProductList.html"
    context_object_name="Product_List"

    def get_queryset(self):
        return Product.objects.all().order_by('-pk')
    

class DeleteProductView(LoginRequiredMixin,DeleteView):
    model=Product
    success_url=reverse_lazy("Product_app:productlist")

class ProductUpdateView(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model=Product
    form_class=ProductUpdateForm
    success_url=reverse_lazy('Product_app:productlist')
    success_message='Product Successfully Updated!'
    template_name='AdminPos/ProductUpdate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variances']=VarianceType.objects.all()
        product=Product.objects.get(pk=self.kwargs.get('pk'))
        context['pk']=product.pk
        context['manf_date']=context['exp_date']=''
        if product.Manufacturing_date!=None:
            context['manf_date']=datetime.datetime.strptime(product.Manufacturing_date.strftime('%Y-%m-%d'),'%Y-%m-%d').strftime('%d/%m/%Y')
        if product.Expiry_date!=None:
            context['exp_date']=datetime.datetime.strptime(product.Expiry_date.strftime('%Y-%m-%d'),'%Y-%m-%d').strftime('%d/%m/%Y')    
        return context

    def get_form_kwargs(self,*args, **kwargs):
        kwargs=super().get_form_kwargs(*args, **kwargs)
        kwargs['product_code']=self.object.Product_Code
        return kwargs

def get_particular_variance(request):
    if request.is_ajax():
        pk=request.GET['pk']
        product=Product.objects.get(pk=pk)
        item=product.productvariance_set.all()
        data=serializers.serialize('json', item)
        return JsonResponse(data,safe=False)



