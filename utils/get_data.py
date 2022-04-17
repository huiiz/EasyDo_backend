# @Time       : 2022/4/16 12:44
# @Author     : HUII
# @File       : get_data.py
# @Description:
import requests


def get_data(url):
    header = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    data = {
        'url': url,
        'method': 'GET',
    }

    res = requests.post('https://www.coder.work/embed/httptest/api', data, headers=header)
    return res.json()['body']


if __name__ == '__main__':
    print(get_data('https://m.thepaper.cn/baijiahao_17575422'))