# @Time       : 2022/5/21 10:56
# @Author     : HUII
# @File       : voice2text.py
# @Description: 将声音转化为文本
import math
import threading

import requests

from utils.ecloud import get_authed_request_url
from utils.sha1 import get_sha1


class VoiceToText:
    def __init__(self, voice_data):
        """
        :param voice_data: base64处理PCM编码音频字符串
        """
        self.subs = self.get_subs(voice_data)
        self.stream_id = self.get_stream_id(voice_data)
        self.n = 0
        self.len = len(self.subs)

    @staticmethod
    def get_subs(pcm):
        """
        将pcm分片
        :param pcm: pcm文件
        :return:
        """
        return [pcm[i * 102400: (i + 1) * 102400] for i in range(math.ceil(len(pcm) / 102400))]

    def get_stream_id(self, voice_data) -> str:
        """
        获得该段语音的编号
        :param voice_data: 声音数据
        :return: 语音编号字符串
        """
        return get_sha1(voice_data)

    @property
    def get_url(self) -> str:
        """
        获得结果地址
        :return: url
        """
        return get_authed_request_url(method='GET', url='https://api-wuxi-1.cmecloud.cn:8443',
                                      path='/api/lingxiyun/cloud/iat/query_result/v1')

    @property
    def post_url(self) -> str:
        """
        发送数据地址
        :return: url
        """
        return get_authed_request_url(url='https://api-wuxi-1.cmecloud.cn:8443',
                                      path='/api/lingxiyun/cloud/iat/send_request/v1')

    def post_request(self, sub: str, i: str, end: int) -> None:
        """
        分段声音请求
        :param sub: 声音内容,base64编码
        :param i: 序号，1开始
        :param end: 是否结束，1为结束
        :return: None
        """
        header = {
            'streamId': self.stream_id,
            'number': i,
            'Content-Type': 'application/json'
        }
        data = {
            "sessionParam": {
                "sid": "2",
                "aue": "raw",
                "rst": "plain",
                "eos": "3000",
                "bos": "3000",
                "dwa": "wpgs",
                "rate": "16000",
                "hotword": "",
            },
            "data": sub,
            "endFlag": end
        }
        print(header)

        res = requests.post(self.post_url, headers=header, json=data)
        print('post')
        print(res.json())
        print('-' * 10)
        self.n += 1

    def get_request(self) -> dict:
        """
        请求结果
        :return: 语音识别结果
        """
        header = {
            'streamId': self.stream_id,
            'Content-Type': 'application/json'
        }
        res = requests.get(self.get_url, headers=header)
        return res.json()

    def get_result(self) -> str:
        """
        获得最终结果
        :return: 识别出的内容
        """
        t_ls = []
        for i in range(len(self.subs)):
            # 多线程用于加速计算
            t = threading.Thread(target=self.post_request,
                                 args=(self.subs[i], str(i + 1), 1 if i == self.len - 1 else 0))
            t.start()
            t_ls.append(t)
        # 阻塞主进程至子进程完全结束
        for t in t_ls:
            t.join()
        res = self.get_request()
        res_text = ''.join([i['ansStr'] for i in res['body']['frame_results']])
        return res_text
