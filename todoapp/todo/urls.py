from django.urls import path
from . import views
from .views import TaskListView,TaskDetailView,TaskCreateView,TaskUpdateView,TaskDeleteView,CustomLoginView,CustomRegisterView
from django.contrib.auth.views import LogoutView


urlpatterns = [path('',TaskListView.as_view(), name='task-list'),
               path('task/<int:pk>/',TaskDetailView.as_view(), name='task-detail'),
               path('create/new/',TaskCreateView.as_view(), name='task-create'),
               path('update/<int:pk>/',TaskUpdateView.as_view(), name='task-update'),
               path('task-delete/<int:pk>/',TaskDeleteView.as_view(), name='task-delete'),
               path('login/',CustomLoginView.as_view(), name='login'),
               path('logout/',LogoutView.as_view(next_page='login'), name='logout'),
               path('register/',CustomRegisterView.as_view(),name='register'),]