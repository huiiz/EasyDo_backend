# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/6/6 006 10:30
@Remark: 自定义权限
"""

from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission


class AnonymousUserPermission(BasePermission):
    """
    匿名用户权限
    """

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return True


class CommonPermission(BasePermission):
    """管理员通用权限"""

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        # 对ViewSet下的def方法进行权限判断
        # 当权限为空时,则可以访问
        is_head = getattr(view, 'head', None)
        if is_head:
            head_kwargs = getattr(view.head, 'kwargs', None)
            if head_kwargs:
                _permission_classes = getattr(head_kwargs, 'permission_classes', None)
                if _permission_classes is None:
                    return True
        if request.user.manage_type > 0:
            return True
        else:
            return False


class BossPermission(BasePermission):
    """Boss权限"""

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        is_head = getattr(view, 'head', None)
        if is_head:
            head_kwargs = getattr(view.head, 'kwargs', None)
            if head_kwargs:
                _permission_classes = getattr(head_kwargs, 'permission_classes', None)
                if _permission_classes is None:
                    return True
        if request.user.manager_type == 1:
            return True
        else:
            return False


class UserManagePermission(BasePermission):
    """用户管理权限"""

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        is_head = getattr(view, 'head', None)
        if is_head:
            head_kwargs = getattr(view.head, 'kwargs', None)
            if head_kwargs:
                _permission_classes = getattr(head_kwargs, 'permission_classes', None)
                if _permission_classes is None:
                    return True
        if request.user.manager_type in [1, 2]:
            return True
        else:
            return False


class ArticleManagePermission(BasePermission):
    """文章管理权限"""

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        is_head = getattr(view, 'head', None)
        if is_head:
            head_kwargs = getattr(view.head, 'kwargs', None)
            if head_kwargs:
                _permission_classes = getattr(head_kwargs, 'permission_classes', None)
                if _permission_classes is None:
                    return True
        if request.user.manager_type in [1, 3]:
            return True
        else:
            return False
