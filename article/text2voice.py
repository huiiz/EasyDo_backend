# @Time       : 2022/5/20 20:45
# @Author     : HUII
# @File       : text2voice.py
# @Description: 将文本转化为声音
import base64
import os.path
import threading
import wave

from utils.ecloud import request_ecloud_api
from utils.read_config import get_config
from utils.sha1 import get_sha1

# 相关配置
native_voice_name = get_config("ecloud_setting", "voice_name")  # 选择了yiping
rate = int(get_config("ecloud_setting", "rate"))    # 默认16000


class TextToVoice:
    def __init__(self, text: str):
        """
        :param text: 待转化的文本
        """
        self.subs = self.get_subs(text)
        self.len = len(self.subs)
        self.names = self.get_voice_names()

    @staticmethod
    def get_subs(article_content: str) -> list:
        """
        将文章分段，前面每段250字，后面最后一段若小于50字，则与前一个合并
        :param article_content: 文章内容
        :return: 分段后的结果
        """
        total_len = len(article_content)
        combine = total_len % 250 < 50
        pre_n = total_len / 250
        n = 0
        res = []
        while n * 250 < total_len:
            if (n + 2) > pre_n and combine:
                text = article_content[n * 250:]
                n += 1
            else:
                text = article_content[n * 250: (n + 1) * 250]
            n += 1
            res.append(text)
        return res

    def get_voice_names(self) -> list:
        """
        获得音频文件名
        :return: 文件名列表
        """
        res = [f'{get_sha1(sub)}.wav' for sub in self.subs]
        return res


    @staticmethod
    def text_to_sound_request(text: str, name: str) -> str:
        """
        请求将文字转化为声音数据
        :param text: 文字
        :param name:
        :return: 声音数据（base64）
        """
        payload = {
            "text": text,
            "sessionParam": {
                "sid": name,
                "frame_size": 640,
                "audio_coding": "raw",
                "native_voice_name": native_voice_name,
                "speed": 0,
                "volume": 0,
                "read_all_marks": 0,
                "read_number": 0,
                "read_english": 0
            }
        }

        res = request_ecloud_api(method='POST',
                                 url='https://api-wuxi-1.cmecloud.cn:8443',
                                 path='/api/lingxiyun/cloud/tts/v1',
                                 payload=payload)
        return res.get('body').get('data')


    def check_and_save_voice(self, sub: str, name: str) -> None:
        """
        检查对应音频文件是否存在
        :param sub: 文章内容
        :param name: 文件名
        :return:
        """
        if not os.path.exists(f'voice/{name}'):
            self.get_voice_and_save(sub, name)

    def get_voice_and_save(self, sub: str, name: str) -> None:
        """
        获得声音数据并保存成文件
        :param sub: 分段文字
        :param name: 文件名
        :return: None
        """
        print(f'保存{name}中')
        req_data = self.text_to_sound_request(sub, name)
        pcm = base64.b64decode(req_data)
        self.pcm_to_wav(pcm, name)

    @staticmethod
    def pcm_to_wav(data, name: str) -> None:
        """
        将pcm转化为wav并保存
        :param data: pcm数据
        :param name: 要保存wav文件名
        :return: None
        """
        try:
            wave_out = wave.open(f'voice/{name}', 'wb')
            wave_out.setnchannels(1)
            wave_out.setsampwidth(2)
            wave_out.setframerate(16000)
            wave_out.writeframes(data)
        except:
            print('获取音频出错啦')

    def non_block(self) -> bool:
        """
        实现非阻塞保存文件
        :return:
        """
        for i in range(len(self.subs)):
            # 多线程用于加速计算
            t = threading.Thread(target=self.check_and_save_voice,
                                 args=(self.subs[i], self.names[i]))
            t.start()
        return True

    def get_result(self) -> list:
        """
        获取结果（名字，确保语音合成已完成）
        :return: 文件名列表
        """
        t_ls = []
        for i in range(len(self.subs)):
            # 多线程用于加速计算
            t = threading.Thread(target=self.check_and_save_voice,
                                 args=(self.subs[i], self.names[i]))
            t.start()
            t_ls.append(t)
        # 阻塞主进程至子进程完全结束
        for t in t_ls:
            t.join()
        return self.names
