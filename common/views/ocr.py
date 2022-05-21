# @Time       : 2022/5/20 23:03
# @Author     : HUII
# @File       : ocr.py
# @Description:
from rest_framework.views import APIView

from article.text2voice import TextToVoice
from utils.ecloud import get_authed_request_url
from utils.json_response import DetailResponse


class GetOcrUrlView(APIView):
    # 获得ocr请求路径
    def get(self, *args, **kwargs):
        url = get_authed_request_url(url='https://api-wuxi-1.cmecloud.cn:8443', path='/api/ocr/v1/general')
        return DetailResponse(data={'url': url})


class GetOcrVoiceView(APIView):
    # 获得ocr声音内容
    def post(self, *args, **kwargs):
        text = self.request.POST.get('text')
        t2v = TextToVoice(text)
        res = t2v.get_result()
        return DetailResponse(data={'voice': res})
