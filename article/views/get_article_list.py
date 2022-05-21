# @Time       : 2022/4/21 23:40
# @Author     : HUII
# @File       : get_article_list.py
# @Description:
from article.models import Article
from article.text2voice import TextToVoice
from utils.json_response import SuccessResponse
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet


class ArticleListSerializers(CustomModelSerializer):
    # cateid = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'category']


class ArticleListViewSet(CustomModelViewSet):
    queryset = Article.objects.filter(status=True).order_by('?')
    serializer_class = ArticleListSerializers

    def list(self, request, *args, **kwargs):
        cid = int(request.query_params.get('cateid', 0))
        queryset = self.get_queryset().filter(category_id=cid)[:5] if cid > 0 else self.get_queryset().all()[:5]
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True, request=request)
        data = serializer.data
        titles = [i['title'] for i in data]
        names = []
        for title in titles:
            t2v = TextToVoice(title)
            t2v.non_block()
            names.extend(t2v.names)
        return SuccessResponse(data={'list': data, 'voice': names}, msg="获取成功", total=5)
