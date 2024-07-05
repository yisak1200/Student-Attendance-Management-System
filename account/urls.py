from django.urls import path
from .views import LoginView,LogoutView
urlpatterns = [
    path('',LoginView.as_view(),name='login_page'),
    path('',LogoutView.as_view(),name = 'logout')
]