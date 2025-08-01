from django.contrib import admin
from django.urls import path
from projects import views

urlpatterns = [
    path('', views.projects, name = 'projects'),
    path('project/<str:pk>/', views.project, name = 'project'),
    path('create_project/', views.create_project, name = 'create_project'),
    path('update_project/<str:pk>/', views.update_project, name = 'update_project'),
    path('delete_project/<str:pk>/', views.delete_project, name = 'delete_project'),
    path('search_project/', views.search_project, name='search_project'),
]
