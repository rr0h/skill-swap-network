from django.urls import path
from . import views

app_name = 'skills'

urlpatterns = [
    path('', views.skill_list, name='skill_list'),
    path('create/', views.skill_create, name='skill_create'),
    path('<int:pk>/', views.skill_detail, name='skill_detail'),
    path('<int:pk>/edit/', views.skill_update, name='skill_update'),
    path('<int:pk>/delete/', views.skill_delete, name='skill_delete'),
    path('search/ajax/', views.skill_search_ajax, name='skill_search_ajax'),
    
    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
]
