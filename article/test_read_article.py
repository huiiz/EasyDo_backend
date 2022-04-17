# @Time       : 2022/4/16 15:07
# @Author     : HUII
# @File       : test_read_article.py
# @Description:
import django
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EasyDo.settings')
django.setup()

from article.models import Article

article = Article.objects.get(id=1)
print(article.content)
print(article.tags)