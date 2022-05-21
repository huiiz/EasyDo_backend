# @Time       : 2022/4/21 22:22
# @Author     : HUII
# @File       : get_article_categories.py
# @Description:

from article.models import ArticleCategory
from utils.json_response import SuccessResponse
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet


class ArticleCategorySerializers(CustomModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ['id', 'name']


class ArticleCategoryViewSet(CustomModelViewSet):
    queryset = ArticleCategory.objects.all()
    serializer_class = ArticleCategorySerializers

    def list(self, request, *args, **kwargs):
        recommend = [{
            'id': 0,
            'name': '推荐'
        }]
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True, request=request)
        res = recommend + serializer.data
        return SuccessResponse(data=res, msg="获取成功", total=len(res))
