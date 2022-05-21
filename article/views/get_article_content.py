# @Time       : 2022/4/21 19:55
# @Author     : HUII
# @File       : get_article_content.py
# @Description: GET请求：获得文章内容并新增阅读记录；PUT请求：更新阅读结束时间
from rest_framework import serializers

from article.models import Article, ReadingRecord
from article.text2voice import TextToVoice
from utils.json_response import DetailResponse, ErrorResponse
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet


class ArticleSerializers(CustomModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Article
        exclude = ('status', 'update_datetime', 'tags')


class ArticleContentViewSet(CustomModelViewSet):
    queryset = Article.objects.filter(status=True)
    serializer_class = ArticleSerializers

    def retrieve(self, request, *args, **kwargs):
        # 获得文章内容
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # 如果前端没有执行结束阅读，则手动执行
        before_reading_record = ReadingRecord.objects.filter()
        if before_reading_record:
            first = before_reading_record.first()
            if first.create_datetime == first.update_datetime:
                first.save()

        ReadingRecord.objects.create(article_id=instance.id, user_id=self.request.user.id)
        instance.count += 1
        instance.save()
        data = serializer.data
        t2v = TextToVoice(data['content'])
        t2v.non_block()
        data['voice'] = t2v.names
        data['length'] = len(data['content'])
        return DetailResponse(data=data, msg="获取成功")

    def update(self, request, *args, **kwargs):
        try:
            record = ReadingRecord.objects.filter(article_id=int(kwargs.get('pk')), user_id=self.request.user.id)
            record[0].save()
            return DetailResponse()
        except:
            return ErrorResponse()


