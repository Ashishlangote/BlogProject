from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView,DetailView,CreateView,UpdateView,DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.db.models import Q

 

# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        
        search_input = self.request.GET.get('q')
        if search_input:
            queryset = queryset.filter(title__icontains=search_input)
        return queryset

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(SuccessMessageMixin,LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content']
    success_message = 'Post Created Successfully'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'login'
    
    model = Post
    template_name = 'post_update.html'
    fields = ['title', 'content']  

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request,'Post Updated Successfully!!!')
        return super().form_valid(form)  

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False          

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    login_url = '/login/'
    redirect_field_name = 'login'

    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False