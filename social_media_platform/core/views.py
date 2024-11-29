from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Comment, Like, Follow
from .forms import PostForm, CommentForm
from django.db.models import Q

@login_required
def home(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/home.html', {'page_obj': page_obj})

def search(request):
    query = request.GET.get('q')
    if query:
        users = get_user_model().objects.filter(Q(username__icontains=query) | Q(profile__bio__icontains=query))
        posts = Post.objects.filter(Q(content__icontains=query) | Q(user__username__icontains=query))
    else:
        users = []
        posts = []
    return render(request, 'core/search.html', {'users': users, 'posts': posts, 'query': query})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'core/create_post.html', {'form': form})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        comment_form = CommentForm()
    return render(request, 'core/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    Like.objects.get_or_create(user=request.user, post=post)
    return redirect('post_detail', pk=pk)

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(get_user_model(), username=username)
    Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
    return redirect('profile', username=username)

