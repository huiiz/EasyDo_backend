# @Time       : 2022/4/14 20:07
# @Author     : HUII
# @File       : urls.py
# @Description:
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *
urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
