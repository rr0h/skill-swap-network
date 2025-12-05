from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('create/<int:request_id>/', views.create_review, name='create_review'),
    path('user/<str:username>/', views.user_reviews, name='user_reviews'),
    path('skill/<int:skill_id>/', views.skill_reviews, name='skill_reviews'),
]
