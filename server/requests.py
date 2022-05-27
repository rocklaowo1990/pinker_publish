from ast import parse
import os
import time
import requests
from lxml import etree


class MyRequests:
    def get(url):
        # 请求头
        headers = {
            'connection': 'keep-alive',
            'sec-ch-ua-platform': "macOS",
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        }
        res = requests.get(url, headers=headers)
        return res

    def parse(url:str, path:str, letter:str, medias:list, works_path:str):
        home_url = 'https://www.tgbak.com'

        have_file = os.path.exists(path)

        # 文件夹目录
        if url[-1] == '/':
            # 检查这个目录的文件有没有下载完成

            if not have_file:
                os.makedirs(path)

            print('正在访问: %s' % url)
            myrequeste = MyRequests.get(url)
            if myrequeste.status_code == 200:
                print('----\033[0;32;40m访问成功\033[0m')

                # 拿到返回数据
                obj = etree.HTML(myrequeste.text)

                # 解析
                obj_tiles = list(obj.xpath(
                    '//td[@class="fb-n"]/a/text()'))
                obj_urls = list(obj.xpath(
                    '//td[@class="fb-n"]/a/@href'))

                del(obj_tiles[0])
                del(obj_urls[0])

                index =0
                while index < len(obj_tiles):
                    next_path = os.path.join(path, obj_tiles[index])
                    next_url = obj_urls[index]
                    MyRequests.parse(home_url + next_url, next_path, letter, medias, works_path)
                    index += 1
        # 文件
        else:
            print('正在检查文件是否已经下载过...')

            alredy = False
            for media in medias:
                if media == url:
                    print('----\033[0;33;40m文件已经下载过,不再重复下载...\033[0m')
                    alredy = True
                    break       
            if not have_file and not alredy:
                print('----\033[0;32;40m文件没有下载过,即将开始下载...\033[0m')
                print('即将下载文件: %s' % url)
                print('----\033[0;33;40m正在下载文件...' + '(' +
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ')\033[0m')
                myrequeste = MyRequests.get(url)
                with open(path, 'wb') as fd:
                    for chunk in myrequeste.iter_content():
                        fd.write(chunk)
                print('----\033[0;32;40m文件下载完成...' + '(' +
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ')\033[0m')
                with open(os.path.join(works_path, 'config.txt'), 'a') as f:
                    f.write(url + '\n')
        