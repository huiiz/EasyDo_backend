# @Time       : 2022/5/20 22:45
# @Author     : HUII
# @File       : read_config.py.py
# @Description:
import configparser


def get_config(section, key):
    config = configparser.ConfigParser()
    # 获取配置文件的真实路径
    path = 'config.ini'
    config.read(path, encoding="utf-8")
    return config.get(section, key)


if __name__ == "__main__":
    access_key = get_config("ecloud", "access_key")
    print(access_key)
