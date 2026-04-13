from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.db.models import Q
from .models import Post, Category, User, Comment
from .forms import CommentForm, PostForm, ProfileForm
from django.utils import timezone


class HomepageView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.select_related('category').filter(
            pub_date__lte=timezone.now(),
            is_published__exact=True,
            category__is_published=True
        )


def post_detail(request, pk):
    template_name = 'blog/detail.html'
    post = get_object_or_404(Post.objects.select_related('category').filter(
        (Q(is_published=True) & Q(category__is_published=True) &
         Q(pub_date__lte=timezone.now())
         | Q(author__username=request.user.username)) & Q(pk=pk)))
    comments = Comment.objects.filter(post=post)
    form = CommentForm()
    context = {'post': post, 'form': form, 'comments': comments}
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category = get_object_or_404(Category.objects.filter(
        is_published__exact=True), slug=category_slug)
    post_list = Post.objects\
        .select_related('category').filter(category__slug=category_slug,
                                           pub_date__lte=timezone.now(),
                                           is_published__exact=True)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'page_obj': page_obj}
    return render(request, template_name, context)


def profile(request, username):
    template_name = 'blog/profile.html'
    user = get_object_or_404(User, username=username)
    post_list = Post.objects\
        .select_related('category', 'author').filter(
            ((Q(is_published=True) & Q(category__is_published=True)
             & Q(pub_date__lte=timezone.now()))
             | Q(author__username=request.user.username)) &
            Q(author__username=username))
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'profile': user, 'page_obj': page_obj}
    return render(request, template_name, context)


@login_required
def delete_post(request, pk):
    instance = get_object_or_404(Post, pk=pk)
    if request.user != instance.author:
        return redirect('blog:post_detail', pk=pk)
    # В форму передаём только объект модели;
    # передавать в форму параметры запроса не нужно.
    form = PostForm(instance=instance)
    context = {'form': form}
    # Если был получен POST-запрос...
    if request.method == 'POST':
        # ...удаляем объект:
        instance.delete()
        # ...и переадресовываем пользователя на страницу со списком записей.
        return redirect('blog:index')
    # Если был получен GET-запрос — отображаем форму.
    template_name = 'blog/create.html'
    return render(request, template_name, context)


@login_required  # Доступ только авторизованным пользователям
def edit_profile(request):
    template_name = 'blog/user.html'
    form = ProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)
    context = {'form': form}
    return render(request, template_name, context)


@login_required
def delete_comment(request, pk, comment_pk):
    post = get_object_or_404(Post, pk=pk)
    instance = get_object_or_404(Comment, pk=comment_pk)
    if request.user != instance.author:
        return redirect('blog:post_detail', pk=pk)
    # В форму передаём только объект модели;
    # передавать в форму параметры запроса не нужно.
    context = {'comment': instance}
    # Если был получен POST-запрос...
    if request.method == 'POST':
        # ...удаляем объект:
        instance.delete()
        post.comment_count -= 1
        post.save()
        # ...и переадресовываем пользователя на страницу со списком записей.
        return redirect('blog:post_detail', pk=pk)
    # Если был получен GET-запрос — отображаем форму.
    template_name = 'blog/comment.html'
    return render(request, template_name, context)


@login_required
def add_comment(request, pk, comment_pk=None):
    if comment_pk is not None:
        # Получаем объект модели или выбрасываем 404 ошибку.
        instance = get_object_or_404(Comment, pk=comment_pk)
        if request.user != instance.author:
            return redirect('blog:post_detail', pk=pk)
    # Если в запросе не указан pk комментария
    # (если получен запрос к странице создания записи):
    else:
        # Связывать форму с объектом не нужно, установим значение None.
        instance = None
    # Получаем объект поста или выбрасываем 404 ошибку.
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST or None, instance=instance)
    if form.is_valid():
        # Создаём объект комментария, но не сохраняем его в БД.
        comment = form.save(commit=False)
        # В поле author передаём объект автора комментария.
        comment.author = request.user
        # В поле post передаём объект поста.
        comment.post = post
        post.comment_count += 1
        post.save()
        # Сохраняем объект в БД.
        comment.save()
    elif comment_pk is not None:
        template_name = 'blog/comment.html'
        context = {'form': form, 'comment': instance}
        return render(request, template_name, context)
    # Перенаправляем пользователя назад, на страницу поста.
    return redirect('blog:post_detail', pk=pk)


@login_required
def create_post(request, pk=None):
    if pk is not None:
        # Получаем объект модели или выбрасываем 404 ошибку.
        instance = get_object_or_404(Post, pk=pk)
        if request.user != instance.author:
            return redirect('blog:post_detail', pk=pk)
    # Если в запросе не указан pk
    # (если получен запрос к странице создания записи):
    else:
        # Связывать форму с объектом не нужно, установим значение None.
        instance = None
    form = PostForm(request.POST or None,
                    files=request.FILES or None, instance=instance)
    if form.is_valid():
        # Создаём объект поста, но не сохраняем его в БД.
        post = form.save(commit=False)
        # В поле author передаём объект автора поста.
        post.author = request.user
        # Сохраняем объект в БД.
        post.save()
        # Перенаправляем пользователя назад, на страницу поста.
        if pk is not None:
            return redirect('blog:post_detail', pk=pk)
        return redirect('blog:profile', username=request.user.username)
    template_name = 'blog/create.html'
    context = {'form': form}
    return render(request, template_name, context)
