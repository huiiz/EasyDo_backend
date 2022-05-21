# @Time       : 2022/4/27 18:41
# @Author     : HUII
# @File       : spark_test.py
# @Description:
import json
import os

import django
from pyspark import SparkContext
from pyspark.ml.feature import Word2Vec
from pyspark.sql import SparkSession

sc = SparkContext()
spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EasyDo.settings')
django.setup()

from article.models import Article

data = list(Article.objects.all().values_list('id', 'tags'))
data = [(i[0], json.loads(i[1])) for i in data[:10]]
pd_data = spark.createDataFrame(data, ['id', 'tags'])
w2v_model = Word2Vec(vectorSize=100, inputCol='tags', outputCol='vector', minCount=3)
model = w2v_model.fit(pd_data)
model.save("/article/models/test.word2vec")
