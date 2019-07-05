from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-rating_likes']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# class CommentCreateView(LoginRequiredMixin, CreateView):
#     model = Comment
#     fields = ['text', 'post']

#     def form_valid(self, form):
#         import pdb;pdb.set_trace()
#         form.instance.user = self.request.user
#         return super().form_valid(form)


class CommentView(LoginRequiredMixin, View):

    def post(self, request):
        post_id = self.request.POST.get('post_id')
        comment_text = self.request.POST.get('comment')
        user = self.request.user
        if user.is_authenticated:
            if post_id and comment_text:
                Comment.objects.create(post_id=post_id, text=comment_text, user=user)
                return JsonResponse({'message': 'success'})
            else:
                return JsonResponse({'message': 'required parameters not found.'})
        return JsonResponse({'message': 'user not logged in.'})


def post_like_count(request, post_id):
    post = Post.objects.get(id=post_id)
    likes_count = post.rating_likes
    return JsonResponse({'likes_count': likes_count})


def comment_like_count(request, post_id):
    post = Comment.objects.get(id=post_id)
    likes_count = post.rating_likes
    return JsonResponse({'likes_count': likes_count})


def delete_comment(request):
    if request.method == "POST":
        comment_id = request.POST.get('comment_id')
        user = request.user
        if user.is_authenticated and user.is_superuser:
            Comment.objects.filter(id=comment_id).delete()
            return JsonResponse({'message': "comment_deleted"})
        return JsonResponse({'likes_count': likes_count})
    else:
        pass
    

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
