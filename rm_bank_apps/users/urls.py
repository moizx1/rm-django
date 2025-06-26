from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user),
    path('me/', views.get_my_profile),
    path('me/update/', views.update_my_profile),
    path('me/change-password/', views.change_password),
]