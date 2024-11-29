from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse,Http404
from .models import Post, Comment
from .models import UserProfile,Follow
from .forms import PostForm, UserProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'core/home.html', {'posts': posts})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})


def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'like_count': post.likes.count()})

def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content')
        Comment.objects.create(post=post, author=request.user, content=content)
        return JsonResponse({'message': 'Comment added successfully!'})
    



# def profile(request, username):
#     # Get the user by their username
#     user = get_object_or_404(User, username=username)
    
#     # Get the associated UserProfile
#     user_profile = get_object_or_404(UserProfile, user=user)
    
#     # Pass the profile, followers, and following to the template
#     return render(request, 'core/profile.html', {
#         'profile': user_profile,
#         'followers': user_profile.followers.all(),
#         'following': user_profile.following.all(),
#     })

def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, followed=user).exists()
    
    followers = user.followers.all()
    following = user.following.all()
    
    return render(request, 'core/profile.html', {
        'profile': user_profile,
        'is_following': is_following,
        'followers': followers,
        'following': following,
    })

@login_required
def follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user != user_to_follow:
        Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
    return redirect('profile', username=user_to_follow.username)

@login_required
def unfollow(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()
    return redirect('profile', username=username)




@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=user.username)
    else:
        form = UserProfileForm(instance=user.userprofile)
    return render(request, 'core/edit_profile.html', {'form': form})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'core/create_post.html', {'form': form})


# def follow(request, username):
#     # Get the user to be followed
#     user_to_follow = get_object_or_404(User, username=username)

#     # Ensure the request user has a profile
#     if not hasattr(request.user, 'profile'):
#         # If the request user doesn't have a profile, create one
#         UserProfile.objects.create(user=request.user)

#     # Ensure the user to follow has a profile
#     if not hasattr(user_to_follow, 'profile'):
#         # If the user to follow doesn't have a profile, create one
#         UserProfile.objects.create(user=user_to_follow)

#     # Add the follow relationship
#     request.user.profile.following.add(user_to_follow.profile)
#     user_to_follow.profile.followers.add(request.user.profile)

#     return redirect('profile', username=user_to_follow.username)

# def unfollow(request, username):
#     user_to_unfollow = get_object_or_404(User, username=username)
#     if request.method == 'POST':
#         # Remove the follow relationship
#         request.user.profile.following.remove(user_to_unfollow.profile)
#         user_to_unfollow.profile.followers.remove(request.user.profile)
#         user_to_unfollow.profile.save()
#         request.user.profile.save()

#     return redirect('profile', username=username)


@login_required
def feed(request):
    # Get the users followed by the current user
    followed_users = Follow.objects.filter(follower=request.user).values_list('followed', flat=True)
    posts = Post.objects.filter(Q(author__in=followed_users) | Q(author=request.user)).order_by('-created_at')
    return render(request, 'core/feed.html', {'posts': posts})