from django.contrib import admin
from django.urls import path, include
from .views import (
    post_list, post_detai, post_share, post_search
)

urlpatterns = [
    path('', post_list, name='post-list'),
    path('<str:category>/<int:id>/', post_detai, name='post_detail'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path('share/<str:category>/<int:post_id>/', post_share, name='post_share'),
    path('search/', post_search, name='post_search'),

]