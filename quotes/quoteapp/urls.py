from django.urls import path

from . import views

app_name = 'quoteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('page/<int:page>', views.main, name='main_paginate'),
    path('tag/<str:search_tag>/page/<int:page>/', views.tag, name='tag_paginate'),
    path('author/<str:search_author>/', views.author, name='author'),
    path('add_tag/', views.add_tag, name='add_tag'),
    path('tag_done/', views.tag_done, name='tag_done'),
    path('add_author/', views.add_author, name='add_author'),
    path('author_done/', views.author_done, name='author_done'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('quote_done/', views.quote_done, name='quote_done'),
    path('edit/', views.edit, name='edit'),
    path('accounts/login/', views.required, name='required'),
]