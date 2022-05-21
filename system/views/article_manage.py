# @Time       : 2022/4/23 10:48
# @Author     : HUII
# @File       : article_manage.py
# @Description: 文章管理
import json

from rest_framework import serializers
from rest_framework.views import APIView

from article.models import Article, ArticleCategory
from utils.get_article_tags import get_tags
from utils.json_response import ErrorResponse, DetailResponse
from utils.pagination import CustomPagination
from utils.permission import ArticleManagePermission
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet


class GetArticleSerializer(CustomModelSerializer):
    tags = serializers.SerializerMethodField()
    # category = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'
        # depth =1

    def get_tags(self, obj):
        return json.loads(obj.tags)

    # def get_category(self, obj):
    #     category = obj.category
    #     return {
    #         'id': category.id,
    #         'name': category.name
    #     }


class CreateArticleSerializer(CustomModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

    def create(self, validated_data):
        instance = super().create(validated_data)
        if not instance.tags:
            instance.tags = json.dumps(get_tags(instance.content), ensure_ascii=False)
        else:
            instance.tags = json.dumps(instance.tags, ensure_ascii=False)
        instance.save()
        return instance


class UpdateArticleSerializer(CustomModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

    def update(self, instance, validated_data):
        if validated_data.get('tags', None):
            validated_data['tags'] = json.dumps(validated_data['tags'], ensure_ascii=False)
        instance = super().update(instance, validated_data)
        return instance


class ArticleManageViewSet(CustomModelViewSet):
    queryset = Article.objects.all()
    serializer_class = GetArticleSerializer
    create_serializer_class = CreateArticleSerializer
    update_serializer_class = UpdateArticleSerializer
    permission_classes = [ArticleManagePermission]
    pagination_class = CustomPagination


class GetTagsView(APIView):
    permission_classes = [ArticleManagePermission]

    def post(self, *args, **kwargs):
        content = self.request.data.get('content', '')
        if not content:
            return ErrorResponse('请传递content')
        tags = get_tags(content)
        return DetailResponse(data={
            'tags': tags
        })


class CategorySerializer(CustomModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ['id', 'name', 'ordering']


class CategoryViewSet(CustomModelViewSet):
    queryset = ArticleCategory.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ArticleManagePermission]
