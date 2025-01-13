from django.utils import timezone
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, View
from Admin.forms import CategoryForm, PostForm, TagForm
from newspaper.models import Category, Post, Tag
from django.contrib.auth.mixins import LoginRequiredMixin



class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/dashboard.html'

class PublishedPostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "admin/publishedpost.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(
        published_at__isnull = False , status = "active"
    ).order_by("-published_at")

class DraftPostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "admin/Draft.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(
        published_at__isnull = True 
    )

class HiddenPostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "admin/hidden.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(
      status = "in_active"
    )

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "admin/postdetail.html"
    context_object_name = "post"

    def get_queryset(self):
        queryset = Post.objects.filter(pk=self.kwargs["pk"])
        return queryset


class CategoryView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "admin/category.html"
    context_object_name = "categories"
    queryset = Category.objects.all()

class TagView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = "admin/tag.html"
    context_object_name = "tags"
    queryset = Tag.objects.all()

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "admin/create_post.html"
    form_class = PostForm
    def get_success_url(self):
        return reverse_lazy("admin-post-detail", kwargs={"pk": self.object.pk})
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "admin/create_post.html"
    form_class = PostForm

    def get_success_url(self):
        post = self.get_object()
        return reverse_lazy("admin-post-detail", kwargs={"pk": post.pk})
        
    

class PostdeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect("published-post")



class PostpublishView(LoginRequiredMixin,  View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk , published_at__isnull = True )
        post.published_at = timezone.now()
        post.save()
        return redirect("published-post")
    
class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    template_name = "admin/create_tag.html"
    form_class = TagForm
    success_url = reverse_lazy("tags")
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class TagdeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Tag.objects.get(pk=pk)
        post.delete()
        return redirect("tags")
    
class TagUpdateView(LoginRequiredMixin, UpdateView):
    model = Tag
    template_name = "admin/create_tag.html"
    form_class = TagForm
    success_url = reverse_lazy("tags")

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = "admin/create_categories.html"
    form_class = CategoryForm
    success_url = reverse_lazy("categories")
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class CategorydeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Category.objects.get(pk=pk)
        post.delete()
        return redirect("categories")
    
class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = "admin/create_categories.html"
    form_class = CategoryForm
    success_url = reverse_lazy("categories")

class PostActiveView(LoginRequiredMixin,  View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk , status = "in_active" )
        post.status = "active"
        post.save()
        return redirect("published-post")

class PostInActiveView(LoginRequiredMixin,  View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk , status = "active" )
        post.status = "in_active"
        post.save()
        return redirect("hidden-post")

        