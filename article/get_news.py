# @Time       : 2022/4/15 23:22
# @Author     : HUII
# @File       : get_news.py
# @Description: 爬取资讯
import json
import random
import re
import time

# import requests
from bs4 import BeautifulSoup

from utils.get_article_tags import get_tags
from utils.get_data import get_data

rubbish_words = ('图片来源', '漫画制作', '供图', '原标题', '策划设计', '阅读全文', '制图', '图/', '相关文章推荐', '撰稿', '编辑', '校对', '摄）',
                '撰文', '排版 ', '版权所有', '更多精彩内容', '　摄', '全文共', '转载此文是出于传递更多信息之目的')


class GetBaiduNews:
    def __init__(self):
        self.cates = [
            '国内', '国际', '军事', '财经', '娱乐', '体育', '互联网', '科技', '游戏', '女人', '汽车', '房产'
        ]
        self.cate_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.urls = [
            'http://news.baidu.com/guonei',
            'http://news.baidu.com/guoji',
            'http://news.baidu.com/mil',
            'http://news.baidu.com/finance',
            'http://news.baidu.com/ent',
            'http://news.baidu.com/sports',
            'http://news.baidu.com/widget?id=AllOtherData&channel=internet',
            'http://news.baidu.com/tech',
            'http://news.baidu.com/game',
            'http://news.baidu.com/lady',
            'http://news.baidu.com/auto',
            'http://news.baidu.com/house',
        ]
        self.header = {
            'Cookie': 'BAIDUID=658A62B320775577118CC9B065AE0D43:FG=1; ab_jid=f479205045689ca50206944b056f8e02c1ea; ab_jid_BFESS=f479205045689ca50206944b056f8e02c1ea; PSTM=1650075500; BIDUPSID=EC3A5949F0E988375A602543CA87B60B; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BAIDUID_BFESS=658A62B320775577118CC9B065AE0D43:FG=1; delPer=0; PSINO=3; BDUSS=Etmemc2QUFSRTRmWE9SQjNXR0R-WkZQYVE2d2FKRFM4R2k1cW9jTGpUdGx4WUZpRVFBQUFBJCQAAAAAAAAAAAEAAAB2kVk5c21pbGXWo7vUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGU4WmJlOFpid; BDUSS_BFESS=Etmemc2QUFSRTRmWE9SQjNXR0R-WkZQYVE2d2FKRFM4R2k1cW9jTGpUdGx4WUZpRVFBQUFBJCQAAAAAAAAAAAEAAAB2kVk5c21pbGXWo7vUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGU4WmJlOFpid; H_PS_PSSID=35836_36174_31660_35912_36165_34584_36121_36073_36125_35802_36258_26350_35724_22159_36061; BA_HECTOR=a4al85a504ak0h8g4f1h5kfrm0q; ab_bid=6f8e02c1ebdf640b3b3053878fecf17f35ef; ab_sr=1.0.1_YjViODg1N2UxOWY1ZDlhZDU0Mjk4YTZhODE5YzE2NjE1ZDRlZmJhMmM4MWMzMTFlNjUwMDkyMjdhN2M0OWRjYzMxMjZlODI2YjU4ZTdlMTA0YTkzMGIzYWQ1ZjI2YmE3OTZiMjM5ZDFlNDY1YjE5MTk5NDQyOGVlNzMzNDIzZThkZDNlYmI4ZjBlOGM3OGFhMmRiNzIwM2RiNmZjMzNiYg==',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) runapi/1.0.7 Chrome/80.0.3987.163 Electron/8.5.5 Safari/537.36',
        }

    def get_raw_html(self, url: str) -> str:
        """
        获得网址对应内容
        :param url: 网址
        :return: html内容
        """
        # res = requests.get(url, headers=self.header)
        # res.encoding = res.apparent_encoding
        res = get_data(url)
        return res

    @staticmethod
    def get_news_title_and_urls(html: str) -> list:
        """
        解析获得新闻标题和url
        :param html: 原始html内容
        :return:
        """
        res = []
        soup = BeautifulSoup(html, 'html.parser')
        if '"ulist' in html:
            class_name = 'ulist'
        elif 'tlc-fl' in html:
            class_name = 'tlc-fl'
        else:
            class_name = 'title'
        ulists = soup.select(f'.{class_name}')
        for ulist in ulists:
            lis = ulist.find_all('a')
            for li in lis:
                title = li.text
                url = li['href']
                res.append((title, url))
        return res

    @staticmethod
    def get_class_name(contain_str: str, html: str) -> str:
        """
        获得包含该字段的类名
        :param contain_str: 包含的字段
        :param html: 原始html内容
        :return: 包含该字段的类名
        """
        class_re = f'"{contain_str}.*?"'
        res = re.findall(class_re, html)
        if res:
            return res[0].replace('"', '')
        else:
            return ''

    @staticmethod
    def get_news_tags(content: str) -> list:
        """
        获得新闻标签
        :param content: 新闻内容
        :return: 新闻标签
        """
        tags = get_tags(content)
        return tags

    def get_news_content(self, html: str) -> tuple:
        """
        获得新闻详细内容
        :param html: 包含新闻的原始html
        :return: title、发布时间、文章来源、content
        """
        content_res = []
        soup = BeautifulSoup(html, 'html.parser')

        if 'contentFont' in html:
            # content_class = 'contentFont'
            title_class = 'titleFont'
            source_and_time = soup.select('.info')[0].span.text.strip()
            stls = source_and_time.split(' ')
            # contents = soup.select(f'.{content_class}')
            if len(stls) == 3:
                post_time = ' '.join(stls[1:])
                source = stls[0]
            else:
                t0 = stls[0]
                if len(t0) > 10:
                    post_time = t0[-10:] + ' ' + stls[1]
                    source = t0[:-10].strip()
                else:
                    post_time = ' '.join(stls)
                    source = ''
        else:
            # content_class = 'bjh-p'
            author_name_class = self.get_class_name('index-module_authorName', html)
            time_class = self.get_class_name('index-module_time', html)
            title_class = self.get_class_name('index-module_articleTitle', html)
            source = soup.select(f'.{author_name_class}')[0].text
            post_time = soup.select(f'.{time_class}')[0].text.replace('发布时间: ', '')

        contents = soup.select('p')[1:]
        title = soup.select(f'.{title_class}')[0].text
        for content in contents:
            if len(content.text) > 2:
                if content_res and content.text == content_res[-1]:
                    continue
                continue_flag = False
                for rub_word in rubbish_words:
                    if rub_word in content.text:
                        continue_flag = True
                        break
                if continue_flag:
                    continue
                content_res.append(content.text)
        return title, post_time, source, '\n'.join(content_res).strip()

    def parse_news(self, cate_id: int, url: str) -> dict:
        """
        解析获得
        :param cate_id: 新闻分类
        :param title: 标题
        :param url: 文章路径
        :return:
        """
        raw = self.get_raw_html(url)
        title, post_time, source, content = self.get_news_content(raw)
        tags = self.get_news_tags(content)
        return {
            'title': title,
            'post_time': post_time,
            'source': source,
            'category_id': cate_id,
            'tags': json.dumps(tags, ensure_ascii=False),
            'content': content
        }

    def run(self, from_i: int = 0, to_i: int = 12):
        for i in range(from_i, to_i):
            cate = self.cates[i]
            cate_id = self.cate_id[i]
            cate_url = self.urls[i]
            raw_content = self.get_raw_html(cate_url)
            news_titles_and_urls = self.get_news_title_and_urls(raw_content)
            for title, url in news_titles_and_urls:
                print(f'正在处理 {title}  【{cate}】')
                try:
                    time.sleep(1 + random.random() * 4)
                    yield self.parse_news(cate_id, url)
                except Exception as e:
                    print(f'\033[31m {title} 处理出错！url:{url}\033[0m')
                    print(e)
                    print('-------------------------------------------------')
