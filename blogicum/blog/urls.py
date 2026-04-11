"""blogicum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path('', views.HomepageView.as_view(), name='index'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/edit/', views.create_post, name='edit_post'),
    path('posts/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('posts/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('posts/<int:pk>/edit_comment/<int:comment_pk>/',
         views.add_comment, name='edit_comment'),
    path('posts/<int:pk>/delete_comment/<int:comment_pk>/',
         views.delete_comment, name='delete_comment'),
    path('category/<slug:category_slug>/',
         views.category_posts, name='category_posts'),
    path('profile/edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
]
