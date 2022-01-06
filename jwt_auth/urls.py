from django.conf.urls import url
from django.urls import path, include
from .api import RegisterView,ChangePasswordView,UpdateProfileView,LogoutView,UserView

urlpatterns = [
      path('register/', RegisterView.as_view()),
      path('change_password/', ChangePasswordView.as_view()),
      path('update_profile/', UpdateProfileView.as_view()),
      path('get_profile/', UserView.as_view()),
      path('logout/', LogoutView.as_view()),
]