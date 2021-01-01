from django.shortcuts import render,get_object_or_404
from myapp.models import Profile,Post
from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from myapp.forms import ProfileForm,PostForm,UserForm
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        u = User.objects.get(username=request.user)
        if Profile.objects.filter(user__username=u).exists():
            p = Profile.objects.get(user__username=u)
        else:
            p=1

        pp = Profile.objects.all()







        return render(request,'myapp/index.html',{'myprofile':p,'u':u,'profilejay':pp})
    else:
        return render(request,'myapp/index.html')




class ProfileCreateView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    form_class=ProfileForm
    model = Profile

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)



class ProfileDetailView(LoginRequiredMixin,DetailView):
    context_object_name = 'profile'
    model = Profile




    def get_context_data(self,*args,**kwargs):
        context = super(ProfileDetailView,self).get_context_data(*args,**kwargs)
        p=Profile.objects.get(id=self.kwargs['pk'])


        jay=p.user.id
        aa = Post.objects.filter(user_id=jay)

        context['aa'] = aa
        return context

class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    model = Profile
    redirect_field_name='myapp/profile_detail.html'
    fields = ('name','surname','bio','profile_image','city','country','age')



def create_view(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
    u=User.objects.get(username=request.user)
    aa=u.profile.id

    # add the dictionary during initialization
    form = PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():

        f=form.save(commit=False)
        f.user=u
        f.save()
        return HttpResponseRedirect(reverse('myapp:detail',args=[aa]))

    context['form']= form
    return render(request, "myapp/post_form.html", context)





def update_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed id
    obj = get_object_or_404(Post, id = id)
    p=Post.objects.get(id=id)
    pp=p.user.profile.id

    # pass the object as instance in form
    form = PostForm(request.POST or None,request.FILES or None, instance = obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('myapp:detail',args=[pp]))

    # add form dictionary to context
    context["form"] = form

    return render(request, "myapp/post_form.html", context)

class UserCreateView(CreateView):
    form_class = UserForm

    template_name = 'myapp/registration.html'
    success_url = reverse_lazy('login')

def delete_view(request,id):
    p=Post.objects.get(id=id)
    pp=p.user.profile.id
    obj = get_object_or_404(Post, id = id)
    obj.delete()

    return HttpResponseRedirect(reverse('myapp:detail',args=[pp]))
