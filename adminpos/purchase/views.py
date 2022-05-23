from django.shortcuts import render,redirect
from .models import PurchaseInvoice,ProductPurchaseDetail
from products.models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DeleteView,DetailView
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponse
from django.http import JsonResponse
import datetime
from dateutil.relativedelta import relativedelta
# Create your views here.
@login_required
def PurchaseInvoiceView(request):
    if request.method=="POST":
        Invoicenum = int(request.POST['InvoiceNumber'])
        while 1:
            if not PurchaseInvoice.objects.filter(Invoiceno=int(Invoicenum)):
                break
            Invoicenum+=1
        Name = request.POST['si_Suppliername']
        Date = request.POST['InvoiceDate']
        Date=Date.replace("/","-")
        Date=datetime.datetime.strptime(Date,'%d-%m-%Y').strftime('%Y-%m-%d')
        Email = request.POST['si_Supplieremail']
        Contact = request.POST['si_Suppliercontact']
        Addr = request.POST['si_Supplieraddr']
        Type = request.POST['InvoiceType']
        Files = request.FILES.get('files')
        if Type == "0":
            Type = "Cash On Delivery"
        elif Type == "1":
            Type = "Bank Transfer"
        else:
            Type = "Easy Paisa"
        Total = request.POST.get('si_subtotal')
        Discount = request.POST['si_discount']
        if Discount == "":
            Discount=0
        Tax = request.POST['si_tax']
        if Tax == "":
            Tax=0
        Shipcharge = request.POST['si_shipping']
        if Shipcharge == "":
            Shipcharge=0
        Pcode = request.POST.getlist('code')
        Price = request.POST.getlist('price')
        Qty = request.POST.getlist('quantity')
        Pdiscount = request.POST.getlist('discount')
        #try:
        obj = PurchaseInvoice(Invoiceno=Invoicenum,Suppliername=Name,Invoicedate=Date,SupplierEmail=Email,Contactno=Contact,
                            Address=Addr,Invoicetype=Type,SubTotal=Total,Discount=Discount,Tax=Tax,Shippingcharge=Shipcharge,doc=Files)
        obj.save()
    #except:
     #   messages.error(request,"Invoice With this invoice number Already Exists!")
      #  return render(request,"AdminPos/PurchaseInvoice.html")
    #else:
        for i in range(len(Pcode)):
            obj2 = Product.objects.get(Product_Code=Pcode[i])
            obj2.Quantity = obj2.Quantity+int(Qty[i])
            obj1 = ProductPurchaseDetail(Invoiceno=obj,Pcode=obj2,product_name=obj2.Product_name,Price=Price[i],PurchaseQuantity=Qty[i],
                                       Discount=Pdiscount[i],product_desc=obj2.Product_Desc,product_code=obj2.Product_Code)
            obj2.save()
            obj1.save()
        messages.success(request,"Invoice with invoice number {} was Created Successfully".format(Invoicenum))
        context=dict()
        context['invoice_number']=PurchaseInvoice.objects.all().order_by('Invoiceno').last()
        if context['invoice_number'] is None:
            context['invoice_number']=1
        else:
            context['invoice_number']=int(context['invoice_number'].pk)+1
        return render(request,"AdminPos/PurchaseInvoice.html",context)
    else:
        context=dict()
        context['invoice_number']=PurchaseInvoice.objects.all().order_by('Invoiceno').last()
        if context['invoice_number'] is None:
            context['invoice_number']=1
        else:
            context['invoice_number']=int(context['invoice_number'].Invoiceno)+1
        return render(request,"AdminPos/PurchaseInvoice.html",context)

@login_required
def purchaseinvoiceupdate(request,pk):
    if request.method=='GET':
        invoice=None
        try:
            invoice=PurchaseInvoice.objects.get(pk=pk)
        except:
            invoice=None
        if invoice==None:
            raise Http404()
        else:
            all_products=invoice.productdetail.all()
            total=[]
            for product in all_products:
                total.append((product.Price*product.PurchaseQuantity)-product.Discount)
            grosstotal=(invoice.SubTotal+invoice.Shippingcharge+invoice.Tax)-invoice.Discount
            return render(request,'AdminPos/purchaseupdateinvoice.html',{'products':zip(all_products,total),'invoice':invoice,'nettotal':grosstotal})
    else:
        Invoicenum = request.POST['InvoiceNumber']
        Name = request.POST['si_Suppliername']
        Date = request.POST['InvoiceDate']
        Date=Date.replace("/","-")
        Date=datetime.datetime.strptime(Date,'%d-%m-%Y').strftime('%Y-%m-%d')
        Email = request.POST['si_Supplieremail']
        Contact = request.POST['si_Suppliercontact']
        Addr = request.POST['si_Supplieraddr']
        Type = request.POST['InvoiceType']
        Files = request.FILES.get('files')
        if Type == "0":
            Type = "Cash On Delivery"
        elif Type == "1":
            Type = "Bank Transfer"
        else:
            Type = "Easy Paisa"
        Total = request.POST.get('si_subtotal')
        Discount = request.POST['si_discount']
        if Discount == "":
            Discount=0
        Tax = request.POST['si_tax']
        if Tax == "":
            Tax=0
        Shipcharge = request.POST['si_shipping']
        if Shipcharge == "":
            Shipcharge=0
        Pcode = request.POST.getlist('code')
        Price = request.POST.getlist('price')
        Qty = request.POST.getlist('quantity')
        Pdiscount = request.POST.getlist('discount')
        Pname=request.POST.getlist('name')
        try:
            invoice=PurchaseInvoice.objects.get(pk=pk)
        except:
            invoice=None
        if invoice==None:
            raise Http404()
        else:
            invoice.Invoiceno=Invoicenum
            invoice.Suppliername=Name
            invoice.Invoicedate=Date
            invoice.SupplierEmail=Email
            invoice.Contactno=Contact
            invoice.Address=Addr
            invoice.Invoicetype=Type
            invoice.SubTotal=Total
            invoice.Discount=Discount
            invoice.Tax=Tax
            invoice.Shippingcharge=Shipcharge
            invoice.doc=Files
            invoice.save()
            all_products=invoice.productdetail.all()
            for product in all_products:
                if product.Pcode!=None:
                    obj=Product.objects.get(pk=product.Pcode.pk)
                    num=obj.Quantity-product.PurchaseQuantity
                    if num<0:
                        obj.Quantity=0
                    else:
                        obj.Quantity=num    
                    obj.save()           
            all_products.delete()
            for i in range(len(Pcode)):
                obj2=None
                try:
                    obj2 = Product.objects.get(Product_Code=Pcode[i])
                except:
                    obj2=None
                if obj2!=None:
                    obj2.Quantity = obj2.Quantity+int(Qty[i])
                    obj1 = ProductPurchaseDetail(Invoiceno=invoice,Pcode=obj2,product_name=obj2.Product_name,Price=Price[i],PurchaseQuantity=Qty[i],
                                            Discount=Pdiscount[i],product_desc=obj2.Product_Desc,product_code=obj2.Product_Code)
                    obj2.save()
                    obj1.save()
                else:
                    obj1 = ProductPurchaseDetail(Invoiceno=invoice,Pcode=obj2,product_name=Pname[i].Product_name,Price=Price[i],PurchaseQuantity=Qty[i],
                                            Discount=Pdiscount[i],product_desc='',product_code=Pcode[i])
                    obj1.save()

            messages.success(request,"Invoice with invoice number {} was updated Successfully".format(Invoicenum))
            return redirect('purchase_app:purchase_list')


class PurchaseInvoiceList(LoginRequiredMixin,ListView):
    template_name='AdminPos/PurchaseInvoiceList.html'
    context_name_data='purchaseinvoice_list'
    model=PurchaseInvoice

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_list=[]
        for invoice in context['purchaseinvoice_list']:
            total=int(invoice.SubTotal)-int(invoice.Discount)+int(invoice.Tax)+int(invoice.Shippingcharge)
            total_list.append(total)
        context['total_sale']=round(sum(total_list),3)
        context['sdate'],context['edate'],context['tspan']=('','',0)
        if 'sdate' in self.request.GET:
            context['sdate']=self.request.GET['sdate']
        if 'edate' in self.request.GET:
            context['edate']=self.request.GET['edate']
        if 'timespan' in self.request.GET:
            context['timespan']=self.request.GET['timespan']

        context["purchaseinvoice_list"] = zip(context['purchaseinvoice_list'],total_list)
        return context

    def get_queryset(self):
        query_dict=self.request.GET
        if 'timespan' not in query_dict and 'sdate' not in query_dict and 'edate' not in query_dict:
            return PurchaseInvoice.objects.all().order_by('-pk')    
        else:
            sdate,edate,timespan=(query_dict['sdate'],query_dict['edate'],query_dict['timespan'])
            if sdate!='' and edate!='':
                sdate=datetime.datetime.strptime(sdate,'%d/%m/%Y').strftime('%Y-%m-%d')
                edate=datetime.datetime.strptime(edate,'%d/%m/%Y').strftime('%Y-%m-%d')
                return PurchaseInvoice.objects.filter(Invoicedate__gte=sdate,Invoicedate__lte=edate).order_by('-pk')
            elif edate!='':
                edate=datetime.datetime.strptime(edate,'%d/%m/%Y').strftime('%Y-%m-%d')
                return PurchaseInvoice.objects.filter(Invoicedate__lte=edate).order_by('-pk')
            elif sdate!='':
                sdate=datetime.datetime.strptime(sdate,'%d/%m/%Y').strftime('%Y-%m-%d')
                return PurchaseInvoice.objects.filter(Invoicedate__gte=sdate).order_by('-pk')
            else:
                today=datetime.date.today()
                past_X=None
                if int(timespan)==1:
                    return PurchaseInvoice.objects.all().order_by('-pk')
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
                    return PurchaseInvoice.objects.filter(Invoicedate__gte=past_X.strftime('%Y-%m-%d'),Invoicedate__lte=today.strftime('%Y-%m-%d')).order_by('-pk')
                else:
                    PurchaseInvoice.objects.all().order_by('-pk')

class DeleteProductView(LoginRequiredMixin,DeleteView):
    model=PurchaseInvoice
    success_url=reverse_lazy("purchase_app:purchase_list")

class PurchaseInvoiceDetailView(LoginRequiredMixin,DetailView):
    template_name='AdminPos/InvoicePurchaseDetail.html'
    context_object_name='invoice'
    model=PurchaseInvoice

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_subtotal_list=list()
        invoice=context['invoice']
        invoice_all_products=invoice.productdetail.all()
        for product in invoice_all_products:
            individual_subtotal=int(product.PurchaseQuantity)*int(product.Price)-int(product.Discount)
            product_subtotal_list.append(individual_subtotal)
        invoice_total=int(invoice.SubTotal)-int(invoice.Discount)+int(invoice.Tax)+int(invoice.Shippingcharge)
        context["invoice_total"]=invoice_total
        context['product_list']=zip(invoice_all_products,product_subtotal_list) 
        return context

class GeneratePdf(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        product_subtotal_list=list()
        invoice=PurchaseInvoice.objects.get(pk=self.kwargs.get('pk'))
        invoice_all_products=invoice.productdetail.all()
        for product in invoice_all_products:
            individual_subtotal=int(product.PurchaseQuantity)*int(product.Price)-int(product.Discount)
            product_subtotal_list.append(individual_subtotal)
        invoice_total=int(invoice.SubTotal)-int(invoice.Discount)+int(invoice.Tax)+int(invoice.Shippingcharge)
        context={}
        context['invoice']=invoice
        context["invoice_total"]=invoice_total
        context['product_list']=zip(invoice_all_products,product_subtotal_list)         
        return render(request,'AdminPos/InvoicePurchasePrint.html',context)

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
            returned_dict={'Product_name':obj.Product_name,'Purchase_price':obj.Purchase_price,'Quantity':obj.Quantity}            
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
            returned_dict={'Product_Code':obj.Product_Code,'Purchase_price':obj.Purchase_price,'Quantity':obj.Quantity}            
            return JsonResponse(returned_dict,status=200)
        except:
            obj=None
        return obj
