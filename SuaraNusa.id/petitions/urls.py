from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    path('petitions/', views.PetitionListView.as_view(), name='petition_list'),
    path('petitions/new/', views.PetitionCreateView.as_view(), name='petition_create'),
    path('petitions/<int:pk>/', views.PetitionDetailView.as_view(), name='petition_detail'),
    path('petitions/<int:pk>/support/', views.support_petition, name='petition_support'),
    
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
]
