# @Time       : 2022/4/14 20:07
# @Author     : HUII
# @File       : urls.py
# @Description:
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from system.views.article_manage import ArticleManageViewSet, GetTagsView, CategoryViewSet
from system.views.change_manager_type import ManagerTypeChangeViewSet
from system.views.create_invite_code import CreateInviteCodeView
from system.views.manager import LoginView, UserInfoViewSet, LogoutView, RegisterViewSet
from system.views.user_list import UserListViewSet

router = DefaultRouter()
router.register('info', UserInfoViewSet)
router.register('register', RegisterViewSet)
router.register('article', ArticleManageViewSet)
router.register('cates', CategoryViewSet)
router.register('ulist', UserListViewSet)
router.register('utype', ManagerTypeChangeViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('login', LoginView.as_view(), name='manager_login'),
    path('logout', LogoutView.as_view(), name='manager_logout'),
    path('createinvite', CreateInviteCodeView.as_view(), name='create_invite'),
    path('tags', GetTagsView.as_view(), name='get_tags'),
    # path('utype', ManagerTypeChangeView.as_view(), name='change_manager_type'),
]
