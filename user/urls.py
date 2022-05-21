# @Time       : 2022/4/14 20:21
# @Author     : HUII
# @File       : urls.py
# @Description:
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views.login import TestView, LoginView

urlpatterns = [
    path('login', LoginView.as_view(), name='user_login'),
    path('test', TestView.as_view(), name='test'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
