from django.shortcuts import render
from . forms import UserCreateForm, UserProfileInfoForm,PostForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from . import models
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from braces.views import SelectRelatedMixin
from django.urls import reverse_lazy
from .models import Post

from django.core.files.storage import FileSystemStorage
# Create your views here.
def index(request):
    my_dict = {'insert_me':"Hello I am from views.py!"}
    return render(request,'base.html',context=my_dict)


def register(request):
    registered = False
    if request.method == 'POST':
        profile_form = UserProfileInfoForm(data=request.POST)
        user_form = UserCreateForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
            return redirect('/login')
        else:
            print(user_form.errors,profile_form.errors)

    else:
        profile_form = UserProfileInfoForm()
        user_form = UserCreateForm()
    return render(request,'signup.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect('/homepage')
            else:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'Login.html', {})


@login_required
def CreatePost(request):
    if request.method == 'POST':
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            post_form.instance.auther = request.user
            post = post_form.save()
            return redirect('/')
        else:
            print(post_form.errors)
    else:
        post_form=PostForm()
    return render(request,'create_post.html',{'post_form':post_form})



class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )




class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ("user")
    success_url = reverse_lazy("homepage")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)


class ListPosts(generic.ListView):
    model = Post
    template_name = "homepage.html"


def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        print(uploaded_file.name)
        print(uploaded_file.size)
        fs = FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
    return render(request,'upload.html')
