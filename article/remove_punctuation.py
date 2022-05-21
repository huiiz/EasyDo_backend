# @Time       : 2022/5/21 15:10
# @Author     : HUII
# @File       : remove_punctuation.py
# @Description:
import re


def remove_punctuation(content):
    punctuation = r"~!@#$%^&*()_+`{}|\[\]\:\";\-\\\='<>?,./，。、《》？；：‘“{【】}|、！@#￥%……&*（）——+=-"
    content = re.sub(r'[{}]+'.format(punctuation), '', content)
    return content.strip().lower()


if __name__ == '__main__':
    c = '据路透社20日报道，加拿大贸易部长武凤已与农业部长比伯日前发布声明，表示中国解除了对该国油菜籽的进口禁令，已有两家加拿大公司获得出口授权，据悉加拿大是世界上最大的油菜籽生产国和出口国，在得知上述消息后，其油菜籽理事会会长爱伟声称，这是向前迈进的积极一步，未来将继续努力争取一个良好的贸易环境，不过他话锋一转，马上开始阴阳怪气起来，表示希望所有行业出口商都能被中国平等对待，更让人难以接受的是当我们主动向加拿大释放善意之后，他们拿到好处立马就换了副嘴脸，当时时间19日，加拿大政府以国家安全为由，正式宣布禁止华为和中兴参与该国5g网络建设。'
    print(remove_punctuation(c))