# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('',                    views.home,          name='home'),

    # Posts (CRUD)
    path('posts/',              views.post_list,     name='post_list'),
    path('posts/<int:pk>/',     views.post_detail,   name='post_detail'),
    path('posts/create/',       views.post_create,   name='post_create'),
    path('posts/<int:pk>/edit/',views.post_update,   name='post_update'),
    path('posts/<int:pk>/delete/', views.post_delete, name='post_delete'),

    # Tasks (Forms + Sessions)
    path('tasks/',              views.task_list,     name='task_list'),
    path('tasks/new/',          views.task_form,     name='task_form'),

    # Authentication
    path('register/',           views.register_view, name='register'),
    path('login/',              views.login_view,    name='login'),
    path('logout/',             views.logout_view,   name='logout'),

    # API endpoint (JSON response demo)
    path('api/posts/',          views.api_posts,     name='api_posts'),
]
