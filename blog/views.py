from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import User, Topic, Post, Comment, Author
from subscribe_email.models import Signup
from django.db.models import Q
from .forms import PostForm,CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User not exist')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
    context = {}
    return render(request,'login_register.html',context)


def logout_page(request):
    logout(request)
    return redirect('home')


def register_page(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Something wrong')
    context = {'form':form}
    return render(request,'register_page.html',context)


def Home(request):
    post = Post.objects.prefetch_related('Topic_post')
    #topic = Topic.objects.all()
    #last_post= Post.objects.all().order_by('-Created')
    if request.method == "POST":
        email = request.POST["email"]
        signup_model = Signup()
        signup_model.email = email
        signup_model.save()

    context = {'post': post}
    return render(request, "home.html", context)


def Blog(request):
    lasted_post = Post.objects.order_by('-Created')
    topic = Topic.objects.all()
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    post = Post.objects.filter(
        Q(Topic_post__Name__icontains=q) |
        Q(Post_name__icontains=q)
    ).distinct()

    paginator = Paginator(post,4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {'post': paginated_queryset,'lasted_post': lasted_post,'page_request_var': page_request_var,'topic':topic}
    return render(request,'blog.html',context)


def post_detail(request,pk):
    post = get_object_or_404(Post,id=pk)
    topic = Topic.objects.all()

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            redirect(reverse('post_detail', kwargs={'pk': post.pk}))
    context = {'post': post, 'topic': topic, 'form':form}
    return render(request,'single-post.html',context)


def post_create(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('blog')
    context = {'form': form}
    return render(request, 'create_post.html', context)


def post_update(request,pk):
    post = get_object_or_404(Post,id=pk)
    form = PostForm(instance=post)
    # if request.user != post.Author:
    #     return HttpResponse('Your are not allowed here!!')
    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES or None,instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog')

    context = {'form': form}
    return render(request, 'create_post.html', context)


@login_required(login_url='login')
def post_delete(request, pk):
    post = get_object_or_404(Post, id=pk)
    # if request.user != post.Author:
    #     return HttpResponse('Your are not allowed here!!')
    post.delete()
    return redirect('blog')


def Topic_detail(request, pk):
    topics = get_object_or_404(Topic, id=pk)
    post = Post.objects.filter(Topic_post=topics)
    context = {'topic_detail': topics, 'post': post}
    return render(request, 'topic_detail.html', context)

# def delete_comment(request, pk):
#     comment = Comment.objects.filter(post=pk).last()
#     post_id = comment.post.id
#     comment.delete()
#     return redirect(reverse('post_detail', args=[post_id]))

# def get_author(user):
#     qs = Author.objects.filter(user=user)
#     if qs.exists():
#         return qs[0]
#     return None

# def post_create(request):
#     title = 'Create'
#     form = PostForm(request.POST or None, request.FILES or None)
#     author = get_author(request.user)
#     if request.method == "POST":
#         if form.is_valid():
#             form.instance.author = author
#             form.save()
#             return redirect(reverse("post-detail", kwargs={
#                 'id': form.instance.id
#             }))
#     context = {
#         'title': title,
#         'form': form
#     }
#     return render(request, "create_post.html", context)








