from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("products/", ProductView.as_view()),
    path('user/', UserView.as_view()),
    path('login/', obtain_auth_token),
    path('register/', Register.as_view()),
    path('cart/', CartView.as_view()),
    path('favorit/', FavoritView.as_view()),

]
