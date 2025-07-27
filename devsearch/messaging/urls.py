from django.urls import path
from messaging import views

urlpatterns = [
    path('chat/<str:username>/', views.chat_view, name='chat'),
    path('inbox/', views.inbox_view, name='inbox'),
    path('single-message/<str:pk>/', views.single_view, name='single-message'),
]
