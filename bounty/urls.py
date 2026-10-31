from django.urls import path

from . import views

urlpatterns = [
    path('api/criminals/', views.CriminalListView.as_view()),
    path('api/criminals/<int:pk>/', views.CriminalDetailView.as_view()),
    path('api/hunts/', views.HuntListView.as_view()),
    path('api/hunts/<int:pk>/', views.HuntDetailView.as_view()),
]
