# @Time       : 2022/4/14 20:07
# @Author     : HUII
# @File       : urls.py
# @Description:
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from article.views.get_article_categories import ArticleCategoryViewSet
from article.views.get_article_content import ArticleContentViewSet
from article.views.get_article_list import ArticleListViewSet
from article.views.search_article import SearchArticleView

router = DefaultRouter()
router.register('cate', ArticleCategoryViewSet)
router.register('list', ArticleListViewSet)
router.register('detail', ArticleContentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('search', SearchArticleView.as_view()),
]

