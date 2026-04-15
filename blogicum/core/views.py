from django.db.models import Q, Count
from django.utils import timezone
from django.core.paginator import Paginator

# Create your views here.


def count_comments(post):
    return post.annotate(comment_count=Count('comments'))


def is_published(post, username=None, is_q=False):
    if is_q:
        return post.filter(Q(is_published=True)
                           & Q(category__is_published=True)
                           & Q(pub_date__lte=timezone.now())
                           | Q(author__username=username))
    return post.filter(is_published__exact=True,
                       category__is_published=True,
                       pub_date__lte=timezone.now())


def page_paginator(request, post_list):
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
