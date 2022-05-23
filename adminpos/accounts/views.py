from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import CreateView,TemplateView,ListView,DeleteView,UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from .forms import UserRegisterForm,UserUpdateForm
from django.contrib.auth import get_user_model
from django.http import Http404
from django.contrib.auth.views import PasswordChangeView
import datetime
from sales.models import SalesInvoice,ProductSalesDetail
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
import json
from .forms import UserPasswordChangeForm
# Create your views here.

def next_weekday(d, weekday):
    if d.weekday()==weekday:
        return d
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: 
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def previous_weekday(d, weekday):
    if d.weekday()==weekday:
        return d
    days_ahead = d.weekday() - weekday
    if days_ahead <= 0: 
        days_ahead -= 7
    return d - datetime.timedelta(days_ahead)
@login_required
def DashboardView(request):
    d = datetime.date.today()
    next_sunday = next_weekday(d, 6)
    previous_monday = previous_weekday(d, 0)
    pre= previous_monday
    week_data=dict()
    while pre!=next_sunday+datetime.timedelta(1):
        val = SalesInvoice.objects.filter(Invoicedate=pre).aggregate(Sum('SubTotal'))['SubTotal__sum']
        if val is None:
            week_data[pre.weekday()] = 0
        else:
            week_data[pre.weekday()] =float(val)
        pre+=datetime.timedelta(1)
    week_data2=dict()
    # pre2 = previous_monday - datetime.timedelta(1)
    pre3 = previous_weekday(d,0)-datetime.timedelta(1)
    pre3 = previous_weekday(pre3,0)
    while pre3!=previous_weekday(d,0):
        val = SalesInvoice.objects.filter(Invoicedate=pre3).aggregate(Sum('SubTotal'))['SubTotal__sum']
        if val is None:
            week_data2[pre3.weekday()] = 0
        else:
            week_data2[pre3.weekday()] =float(val)
        pre3+=datetime.timedelta(1)
    a = ProductSalesDetail.objects.values('product_code','product_name','Price').annotate(Sum('SaleQuantity')).order_by('-SaleQuantity__sum')

    print(week_data2)
    totals = SalesInvoice.objects.filter(Invoicedate=datetime.date.today()).aggregate(Sum('SubTotal'))['SubTotal__sum']
    for i in a:
        i['Price']=float(i['Price'])
    current_week=json.dumps(week_data)
    last_week=json.dumps(week_data2)

    
    return render(request,'AdminPos/index.html',{"current":current_week,"last":last_week,"product_sum":a[:4],"totalsum":totals})


class UserRegisterView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    template_name='AdminPos/UserRegister.html'
    success_url=reverse_lazy('accounts:user_register')
    success_message="%(username)s's account was Successfully Created!"
    form_class=UserRegisterForm

    def post(self,request,*args, **kwargs):
        if request.user.is_admin:
            return super().post(request,*args, **kwargs)
        raise Http404()    


class GetUserList(LoginRequiredMixin,ListView):
    model=get_user_model()
    template_name="AdminPos/UserProfile.html"
    context_object_name="Users_List"
    
    def get_queryset(self):
        return get_user_model().objects.exclude(username__iexact=self.request.user.username).order_by('username')

class DeleteUser(LoginRequiredMixin,DeleteView):
    model=get_user_model()
    success_url=reverse_lazy("accounts:users_list")

    def post(self,request,*args, **kwargs):
        if request.user.is_admin:
            return super().post(request,*args, **kwargs)
        raise Http404()    

class UserUpdateView(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model = get_user_model()
    template_name = "AdminPos/UserUpdate.html"
    success_message="Profile Successfully Updated.."
    form_class=UserUpdateForm
    success_url=reverse_lazy('accounts:users_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_user']=self.request.user
        return kwargs

    def get(self,request,*args, **kwargs):
        if request.user.pk == self.kwargs.get('pk'):
            return super().get(request,*args, **kwargs)
        raise Http404()    

class UserPasswordUpdateView(LoginRequiredMixin,PasswordChangeView):
    template_name='AdminPos/UserPasswordUpdate.html'
    success_url=reverse_lazy('accounts:user_password_update')
    form_class=UserPasswordChangeForm

    def get_form_kwargs(self,*args, **kwargs):
        kwargs=super().get_form_kwargs(*args, **kwargs)
        kwargs['pk']=self.kwargs.get('pk')
        return kwargs

    def get_success_url(self,**kwargs):
        return reverse_lazy('accounts:user_password_update',args=(self.kwargs.get('pk'),))
