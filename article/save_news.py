# @Time       : 2022/4/16 14:40
# @Author     : HUII
# @File       : save_news.py
# @Description: 将数据存入数据库
import django
import os

from article.get_news import GetBaiduNews

if __name__ != '__main__':
    from article.models import Article


def save_news(news: dict):
    if len(news['content']) < 35:
        print(f'\033[35m -{news["title"]} 内容过短，不保存\033[0m')
        return None
    if not Article.objects.filter(title=news['title']):
        Article.objects.create(**news)
        print(f'\033[32m -{news["title"]} 保存成功\033[0m')
    else:
        print(f'\033[34m -{news["title"]} 已存在\033[0m')


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EasyDo.settings')
    django.setup()

    from article.models import Article

    for news in enumerate(GetBaiduNews().run()):
        try:
            save_news(news[1])
        except:
            if __name__ == '__main__':
                os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EasyDo.settings')
                django.setup()
            else:
                pass
