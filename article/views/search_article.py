# @Time       : 2022/5/21 0:26
# @Author     : HUII
# @File       : search_article.py
# @Description: 搜索文章相关接口
import base64

from rest_framework.views import APIView

from article.remove_punctuation import remove_punctuation
from article.search import search_from_article
from article.search_caches import set_cache, get_cache
from article.text2voice import TextToVoice
from article.voice2text import VoiceToText
from utils.json_response import SuccessResponse
from utils.sha1 import get_sha1


class SearchArticleView(APIView):
    def post(self, *args, **kwargs):
        rtype = self.request.POST.get('type')
        page = int(self.request.query_params.get('page', 1))
        limit = int(self.request.query_params.get('limit', 5))
        if rtype == 'voice':
            pcm = self.request.FILES.get('voice').read()
            encoded_pcm = str(base64.b64encode(pcm), 'utf-8')
            v2t = VoiceToText(encoded_pcm)
            text = v2t.get_result()
            keyword = remove_punctuation(text)
            key = get_sha1(keyword)
            set_cache(key, keyword)
        else:
            key = self.request.POST.get('key')
            keyword = get_cache(key)

        data = search_from_article(keyword).values('id', 'title', 'category')
        total = data.count()
        data = data[(page-1) * limit: page * limit]
        titles = [i['title'] for i in data]
        names = []
        for title in titles:
            t2v = TextToVoice(title)
            t2v.non_block()
            names.extend(t2v.names)
        return SuccessResponse(data={'list': data, 'voice': names, 'text': keyword, 'key': key}, msg="获取成功", total=total, page=page, limit=limit)