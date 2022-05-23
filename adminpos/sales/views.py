from django.shortcuts import render,redirect
from products.models import Product
from .models import SalesInvoice,ProductSalesDetail
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DeleteView,DetailView
from .models import SalesInvoice
from django.urls import reverse_lazy
from django.views import View
from django.http import Http404
import datetime
from dateutil.relativedelta import relativedelta
# Create your views here

@login_required
def SaleInvoiceView(request):        
    if request.method=="POST":
        Invoicenum = int(request.POST['InvoiceNumber'])
        while 1:
            if not SalesInvoice.objects.filter(Invoiceno=int(Invoicenum)):
                break
            Invoicenum+=1
        # return render(request,"AdminPos/index.html")
        # while SalesInvoice.objects.get(Invoiceno=Invoicenum) is not None:
            # Invoicenum+=1
        Name = request.POST['si_customername']
        Date = request.POST['InvoiceDate']
        Date=Date.replace("/","-")
        Date=datetime.datetime.strptime(Date,'%d-%m-%Y').strftime('%Y-%m-%d')
        Email = request.POST['si_customeremail']
        Contact = request.POST['si_customercontact']
        Addr = request.POST['si_customeraddr']
        Type = request.POST['InvoiceType']
        if Type == "0":
            Type = "Cash On Delivery"
        elif Type == "1":
            Type = "Bank Transfer"
        else:
            Type = "Easy Paisa"
        Total = request.POST['si_subtotal']
        Discount = request.POST['si_discount']
        if Discount == "":
            Discount=0
        Tax = request.POST['si_tax']
        if Tax == "":
            Tax=0
        Tax = str((float(Tax)/100)*float(Total))
        Shipcharge = request.POST['si_shipping']
        if Shipcharge == "":
            Shipcharge=0
        Pcode = request.POST.getlist('code')
        Price = request.POST.getlist('price')
        Qty = request.POST.getlist('quantity')
        Pdiscount = request.POST.getlist('discount')
        # try:
        obj = SalesInvoice(Invoiceno=Invoicenum,Customername=Name,Invoicedate=Date,CustomerEmail=Email,Contactno=Contact,
                            Address=Addr,Invoicetype=Type,SubTotal=Total,Discount=Discount,Tax=Tax,Shippingcharge=Shipcharge)
        obj.save()
        # except:
            # messages.error(request,"Invoice With this invoice number Already Exists!")
            # return render(request,"AdminPos/SalesInvoice.html")
        # else:
        for i in range(len(Pcode)):
            obj2 = Product.objects.get(Product_Code=Pcode[i])
            obj2.Quantity = obj2.Quantity-int(Qty[i])
            obj1 = ProductSalesDetail(Invoiceno=obj,Pcode=obj2,product_name=obj2.Product_name,Price=Price[i],SaleQuantity=Qty[i],
                                        Discount=Pdiscount[i],product_desc=obj2.Product_Desc,product_code=obj2.Product_Code)
            obj2.save()
            obj1.save()
        messages.success(request,"Invoice with invoice number {} was Created Successfully".format(Invoicenum))
        context=dict()
        context['invoice_number']=SalesInvoice.objects.all().order_by('Invoiceno').last()
        if context['invoice_number'] is None:
            context['invoice_number']=1
        else:
            context['invoice_number']=int(context['invoice_number'].Invoiceno)+1
        
        context['date']=datetime.datetime.now().strftime ("%d/%m/%Y")
        context['invoice_pk']=obj.pk
        return render(request,"AdminPos/SalesInvoice.html",context)
    else:
        context=dict()
        context['invoice_number']=SalesInvoice.objects.all().order_by('Invoiceno').last()
        if context['invoice_number'] is None:
            context['invoice_number']=1
        else:
            context['invoice_number']=int(context['invoice_number'].Invoiceno)+1
        
        context['date']=datetime.datetime.now().strftime ("%d/%m/%Y")
        return render(request,"AdminPos/SalesInvoice.html",context)

@login_required
def salesinvoiceupdateview(request,pk):
    if request.method=='GET':
        invoice=None
        try:
            invoice=SalesInvoice.objects.get(pk=pk)
        except:
            invoice=None
        if invoice==None:
            raise Http404()
        else:
            all_products=invoice.productdetail.all()
            total=[]
            for product in all_products:
                total.append((product.Price*product.SaleQuantity)-product.Discount)
            grosstotal=(invoice.SubTotal+invoice.Shippingcharge+invoice.Tax)-invoice.Discount
            tax=round((invoice.Tax/invoice.SubTotal)*100,2)
            return render(request,'AdminPos/salesupdateinvoice.html',{'tax':tax,'products':zip(all_products,total),'invoice':invoice,'nettotal':grosstotal})
    else:
        Invoicenum = request.POST['InvoiceNumber']
        Name = request.POST['si_customername']
        Date = request.POST['InvoiceDate']
        Date=Date.replace("/","-")
        Date=datetime.datetime.strptime(Date,'%d-%m-%Y').strftime('%Y-%m-%d')
        Email = request.POST['si_customeremail']
        Contact = request.POST['si_customercontact']
        Addr = request.POST['si_customeraddr']
        Type = request.POST['InvoiceType']
        if Type == "0":
            Type = "Cash On Delivery"
        elif Type == "1":
            Type = "Bank Transfer"
        else:
            Type = "Easy Paisa"
        Total = request.POST['si_subtotal']
        Discount = request.POST['si_discount']
        if Discount == "":
            Discount=0
        Tax = request.POST['si_tax']
        if Tax == "":
            Tax=0
        Tax = str((float(Tax)/100)*float(Total))
        Shipcharge = request.POST['si_shipping']
        if Shipcharge == "":
            Shipcharge=0
        Pcode = request.POST.getlist('code')
        Price = request.POST.getlist('price')
        Qty = request.POST.getlist('quantity')
        Pdiscount = request.POST.getlist('discount')
        Pname=request.POST.getlist('name')
        invoice=None
        try:
            invoice=SalesInvoice.objects.get(pk=pk)
        except:
            invoice=None
        if invoice==None:
            raise Http404()
        else:
            invoice.Invoiceno=Invoicenum
            invoice.Customername=Name
            invoice.Invoicedate=Date
            invoice.CustomerEmail=Email
            invoice.Contactno=Contact
            invoice.Address=Addr
            invoice.Invoicetype=Type
            invoice.SubTotal=Total
            invoice.Discount=Discount
            invoice.Tax=Tax
            invoice.Shippingcharge=Shipcharge
            invoice.save()
            all_products=invoice.productdetail.all()
            for product in all_products:
                if product.Pcode!=None:
                    obj=Product.objects.get(pk=product.Pcode.pk)
                    obj.Quantity+=product.SaleQuantity
                    obj.save()           
            all_products.delete()
            for i in range(len(Pcode)):
                obj2=None
                try:
                    obj2 = Product.objects.get(Product_Code=Pcode[i])
                except:
                    obj2=None
                if obj2!=None:    
                    obj2.Quantity = obj2.Quantity-int(Qty[i])
                    obj1 = ProductSalesDetail(Invoiceno=invoice,Pcode=obj2,product_name=obj2.Product_name,Price=Price[i],SaleQuantity=Qty[i],
                                            Discount=Pdiscount[i],product_desc=obj2.Product_Desc,product_code=obj2.Product_Code)
                    obj2.save()
                    obj1.save()
                else:
                    obj1 = ProductSalesDetail(Invoiceno=invoice,Pcode=obj2,product_name=Pname[i],Price=Price[i],SaleQuantity=Qty[i],
                                            Discount=Pdiscount[i],product_desc='',product_code=Pcode[i])
                    obj1.save()

            messages.success(request,"Invoice with invoice number {} was updated Successfully".format(invoice.Invoiceno))
            return redirect('sales_app:sales_list')    

def GetProductCode(request):
    if request.is_ajax():
        term=request.GET.get('term')
        query_set=Product.objects.filter(Product_Code__startswith=term)
        retured_list=list(query_set.values('id','Product_Code'))
        return JsonResponse(retured_list,safe=False)

def GetProductDetailsView(request):
    if request.method == 'GET':
        try:
            obj=Product.objects.get(id=request.GET.get('id'))
            returned_dict={'Product_name':obj.Product_name,'Selling_price':obj.Selling_price,'Quantity':obj.Quantity}            
            return JsonResponse(returned_dict,status=200)
        except:
            obj=None
        return obj 

def GetProductNameView(request):
    if request.is_ajax():
        term=request.GET.get('term')
        query_set=Product.objects.filter(Product_name__startswith=term)
        retured_list=list(query_set.values('id','Product_name'))
        return JsonResponse(retured_list,safe=False)

def GetProductCodeName(request):
    if request.method == 'GET':
        try:
            obj=Product.objects.get(id=request.GET.get('id'))
            returned_dict={'Product_Code':obj.Product_Code,'Selling_price':obj.Selling_price,'Quantity':obj.Quantity}            
            return JsonResponse(returned_dict,status=200)
        except:
            obj=None
        return obj

class SaleInvoiceList(LoginRequiredMixin,ListView):
    template_name='AdminPos/SalesInvoiceList.html'
    context_name_data='salesinvoice_list'
    model=SalesInvoice

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_list=[]
        for invoice in context['salesinvoice_list']:
            total=float(invoice.SubTotal)-float(invoice.Discount)+float(invoice.Tax)+float(invoice.Shippingcharge)
            total_list.append(total)
        context['total_sale']=round(sum(total_list),3)
        context['sdate'],context['edate'],context['tspan']=('','',0)
        if 'sdate' in self.request.GET:
            context['sdate']=self.request.GET['sdate']
        if 'edate' in self.request.GET:
            context['edate']=self.request.GET['edate']
        if 'timespan' in self.request.GET:
            context['timespan']=self.request.GET['timespan']
        context["salesinvoice_list"] = zip(context['salesinvoice_list'],total_list)
        return context

    def get_queryset(self):
        query_dict=self.request.GET
        if 'timespan' not in query_dict and 'sdate' not in query_dict and 'edate' not in query_dict:
            return SalesInvoice.objects.all().order_by('-pk')    
        else:
            sdate,edate,timespan=(query_dict['sdate'],query_dict['edate'],query_dict['timespan'])
            if sdate!='' and edate!='':
                sdate=datetime.datetime.strptime(sdate,'%d/%m/%Y').strftime('%Y-%m-%d')
                edate=datetime.datetime.strptime(edate,'%d/%m/%Y').strftime('%Y-%m-%d')
                return SalesInvoice.objects.filter(Invoicedate__gte=sdate,Invoicedate__lte=edate).order_by('-pk')
            elif edate!='':
                edate=datetime.datetime.strptime(edate,'%d/%m/%Y').strftime('%Y-%m-%d')
                return SalesInvoice.objects.filter(Invoicedate__lte=edate).order_by('-pk')
            elif sdate!='':
                sdate=datetime.datetime.strptime(sdate,'%d/%m/%Y').strftime('%Y-%m-%d')
                return SalesInvoice.objects.filter(Invoicedate__gte=sdate).order_by('-pk')
            else:
                today=datetime.date.today()
                past_X=None
                if int(timespan)==1:
                    return SalesInvoice.objects.all().order_by('-pk')
                elif int(timespan)==2:
                    past_X=today + relativedelta(days=-15)
                elif int(timespan)==3:
                    past_X=today + relativedelta(months=-1)
                elif int(timespan)==4:
                    past_X=today + relativedelta(months=-3)
                elif int(timespan)==5:
                    past_X=today + relativedelta(months=-6)
                elif int(timespan)==6:
                    past_X=today + relativedelta(months=-12)    
                if past_X!=None:
                    return SalesInvoice.objects.filter(Invoicedate__gte=past_X.strftime('%Y-%m-%d'),Invoicedate__lte=today.strftime('%Y-%m-%d')).order_by('-pk')
                else:
                    SalesInvoice.objects.all().order_by('-pk')



class DeleteProductView(LoginRequiredMixin,DeleteView):
    model=SalesInvoice
    success_url=reverse_lazy("sales_app:sales_list")

class SaleInvoiceDetailView(LoginRequiredMixin,DetailView):
    template_name='AdminPos/invoice_detail.html'
    context_object_name='invoice'
    model=SalesInvoice

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_subtotal_list=list()
        invoice=context['invoice']
        invoice_all_products=invoice.productdetail.all()
        for product in invoice_all_products:
            individual_subtotal=int(product.SaleQuantity)*int(product.Price)-int(product.Discount)
            product_subtotal_list.append(individual_subtotal)
        invoice_total=int(invoice.SubTotal)-int(invoice.Discount)+int(invoice.Tax)+int(invoice.Shippingcharge)
        context["invoice_total"]=invoice_total
        context['product_list']=zip(invoice_all_products,product_subtotal_list) 
        return context

class GeneratePdf(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        product_subtotal_list=list()
        invoice=SalesInvoice.objects.get(pk=self.kwargs.get('pk'))
        invoice_all_products=invoice.productdetail.all()
        for product in invoice_all_products:
            individual_subtotal=int(product.SaleQuantity)*int(product.Price)-int(product.Discount)
            product_subtotal_list.append(individual_subtotal)
        invoice_total=int(invoice.SubTotal)-int(invoice.Discount)+int(invoice.Tax)+int(invoice.Shippingcharge)
        context={}
        context['stotal']=round(invoice.SubTotal,2)
        context['discount']=round(invoice.Discount,2)
        context['tax']=round(invoice.Tax,2)
        context['scharges']=round(invoice.Shippingcharge,2)
        context['invoice']=invoice
        context["invoice_total"]=invoice_total
        context['product_list']=zip(invoice_all_products,product_subtotal_list)         
        return render(request,'AdminPos/invoice-print2.html',context)
        

