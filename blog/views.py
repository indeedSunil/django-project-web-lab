# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import Post, Task
from .forms import PostForm, TaskForm, RegisterForm

def home(request):
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
    client_ip  = request.META.get('REMOTE_ADDR', 'Unknown')

    context = {
        'user_agent': user_agent,
        'client_ip':  client_ip,
        'user':       request.user,
    }
    return render(request, 'blog/home.html', context)

def api_posts(request):
    posts = list(Post.objects.values('id', 'title', 'created_at'))
    return JsonResponse({'posts': posts})

def post_list(request):
    posts = Post.objects.filter(is_published=True).select_related('author')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, is_published=True)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Create'})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Update'})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('post_list')

    return render(request, 'blog/post_confirm_delete.html', {'post': post})

@login_required
def task_form(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            request.session['last_task'] = task.title
            messages.success(request, f'Task "{task.title}" created!')
            return redirect('task_list')
    else:
        form = TaskForm()

    last_task = request.session.get('last_task', None)
    return render(request, 'blog/task_form.html', {
        'form': form,
        'last_task': last_task
    })

@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user).order_by('status')
    return render(request, 'blog/task_list.html', {'tasks': tasks})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created! Welcome, {user.username}.')
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'blog/login.html')

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('login')

    return render(request, 'blog/logout_confirm.html')
