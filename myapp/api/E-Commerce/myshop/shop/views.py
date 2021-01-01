from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from shop.models import Customer,Product,ShippingAddress,CartItem,Order,Category
from django.contrib.auth.models import User
from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.db.models import F
from shop.forms import AddressForm,UserForm
from django.contrib.auth.forms import UserCreationForm
import datetime

from django.http import HttpResponseRedirect
import random
# Create your views here.

def index(request):
    dict1 = Product.objects.annotate(odd=F('id') % 2).filter(odd=False)
    dict2 = Product.objects.annotate(odd=F('id') % 2).filter(odd=True)



    return render(request,'shop/index.html',{'products1':dict1,'products2':dict2})

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'

def Add_To_Cart(request,pk):
    u=request.user
    p=Product.objects.all().get(id=str(pk))
    c=User.objects.get(username=u)
    cc=CartItem.objects.filter(cart=c)




    cart_item , status = CartItem.objects.get_or_create(cart=c,product=p)
    cart_item.total = cart_item.quantity * cart_item.product.price

    if status==False:

        cart_item.quantity+=1
        cart_item.total = cart_item.quantity * cart_item.product.price
        cart_item.save()






    return redirect(reverse('shop:cart'))

def cart(request):
    u=request.user

    c=User.objects.get(username=u)
    cc=CartItem.objects.filter(cart=c)
    ftotal = 0
    for i in cc:
        ftotal+=i.quantity * i.product.price
        i.save()



    return render(request,'shop/cart.html',{'insert':cc,'ftotal':ftotal})

def delete_from_cart(request,pk):
    u=request.user
    p=Product.objects.all().get(id=str(pk))
    c=User.objects.get(username=u)
    cc=CartItem.objects.filter(cart=c)
    i=CartItem.objects.all().get(cart=c,product=p)
    i.quantity=i.quantity-1
    i.total = i.quantity * i.product.price
    i.save()
    if i.quantity==0:
        i.delete()
    return redirect(reverse('shop:cart'))

def delete_entire(request,pk):
    u=request.user
    p=Product.objects.all().get(id=str(pk))
    c=User.objects.get(username=u)
    cc=CartItem.objects.filter(cart=c)
    i=CartItem.objects.all().get(cart=c,product=p)
    i.delete()
    return redirect(reverse('shop:cart'))

def checkout(request):
    u=request.user
    user = User.objects.get(username=u)


    c=User.objects.get(username=u)
    cc=CartItem.objects.filter(cart=c)
    ftotal = 0

    for i in cc:

        ftotal+=i.quantity * i.product.price




    return render(request,'shop/checkout.html',{'final':cc,'ftotal':ftotal,'user':user})




class AddressCreateView(CreateView):
    model = ShippingAddress
    form_class = AddressForm
    template_name = 'shop/address_form.html'
    success_url = reverse_lazy('shop:final')

    def form_valid(self,form):

        form.instance.customer=self.request.user
        return super().form_valid(form)
    def get_context_data(self,*args,**kwargs):
        context = super(AddressCreateView,self).get_context_data(*args,**kwargs)
        u=self.request.user
        s= ShippingAddress.objects.filter(customer__username=u).exists()
        p =ShippingAddress.objects.filter(customer__username=u)
        context['p']=p
        context['s']=s
        return context

def finalview(request):
    u=request.user

    c=User.objects.get(username=u)
    cc=CartItem.objects.filter(cart=c)
    ftotal = 0
    m = random.randint(14563789,24356729)

    for i in cc:
        ftotal+=i.quantity * i.product.price
        i.transaction_id = m

        i.ordered=True
        i.save()


    for new in cc:
        new_order = Order(
        order=new.cart,product=new.product,transaction_id=new.transaction_id,quantity=new.quantity,ordered=new.ordered
        )
        if new.total==0:
            new_order.total=new.product.price
        else:
             new_order.total=new.total
        new_order.save()
    cc.delete()





    return render(request,'shop/finalpage.html',{'final':cc,'ftotal':ftotal})

class AddressUpdateView(UpdateView):
    model = ShippingAddress
    template_name = 'shop/update.html'
    redirect_field_name='shop/address_form.html'
    fields = ('address','city','state','zipcode')

class AddressDetailView(DetailView):
    context_object_name='address'
    model = ShippingAddress

class CategoryListView(ListView):
    context_object_name = 'category'
    model = Category
    template_name = 'shop/shop.html'
    def get_context_data(self,*args,**kwargs):
        context = super(CategoryListView,self).get_context_data(*args,**kwargs)
        plist = Product.objects.all()
        context['plist']=plist
        return context



def CategoryView(request,cats):
    c=Category.objects.get(name=cats)
    cc = Category.objects.all()

    cats_list = Product.objects.filter(category=c)

    return render(request,'shop/categories.html',{'cats_list':cats_list,'category':cc})


class UserCreateView(CreateView):
    form_class = UserForm

    template_name = 'shop/registration.html'
    success_url = reverse_lazy('login')

def ProfileView(request):
    u=request.user

    o = Order.objects.filter(order__username=u)
    d = o[0].date

    j=Order.objects.first()
    return render(request,'shop/profile.html',{'order':o,'d':d,'j':j})
