import random
import requests
import time
from lxml import etree
import os


def getHtml(url):
    # 请求头
    headers = {
        'connection': 'keep-alive',
        'sec-ch-ua-platform': "macOS",
        'user-agent': 'Mozilla/5.0 (MacintoshIntel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
        'referer': 'https://www.v2ph.com/',
        'cache-control': 'max-age=0',
        'sec-fetch-site': 'same-site',
        'cookie': 'frontend=eafada11b0995b806ee543b82d40e93e; fpestid=-rjxgxm6wTx_YloLLGWFGnxhFOp99oO9OIN3Xqj1xkl-DgsyjjlbvARaQnSJY_uDNiULvw; cf_clearance=F5jymsGCqi9u33tBUw47SO..6vsZibYSgvzY.7pzRlw-1646465641-0-150; _gid=GA1.2.1160746623.1646618113; __stripe_mid=fd0d8936-4081-4855-b7c9-4cc838b442d4e3ad5d; __cf_bm=0jxQvMHCI0lWQDqqnBeM8HNSqhiNJzZMi0Xf1A4DxF4-1646712580-0-AXeOBAVEO7U5YOJ0Ice7jTnw1sVGeWOgXig2L3f72+uV4zuUOUuDg5mz2tOsq+zs52gPDIHMGISvZARqwYu1kDqfJS5YS1QFw2ogcihM+ErfAfTZ43/CTlxnnUzRsoCZaQ==; __stripe_sid=7ff29417-4ae4-4422-8ce8-28e08baa6e329da7a6; frontend-rmu=HfsHJ5oZQ0Of60JfGaoHyARUZ616mg==; frontend-rmt=6WiCsGQR8o8ISxy58TPdAiLuXMM7+0zqwmLD4PZwXxcm+IjmQcYMQfiHOdyzVemF; _gat_UA-140713725-1=1; _ga=GA1.2.187270400.1646106115; _ga_170M3FX3HZ=GS1.1.1646712575.24.1.1646712656.48'
    }
    res = requests.get(url, headers=headers)
    return res


def getImages():
    # 首页地址
    home_url = 'https://www.v2ph.com'

    # 请求首页
    home_res = getHtml(home_url)

    # 访问首页成功
    if home_res.status_code == 200:

        # 拿到首页的返回数据
        home_obj = etree.HTML(home_res.text)

        # 筛选首页的 Nav 找到需要寻找图片的分类的地址
        nav_url_list = list(home_obj.xpath(
            '//ul[@class="navbar-nav"]/li/a/@href'))
        nav_name_list = list(home_obj.xpath(
            '//ul[@class="navbar-nav"]/li/a/text()'))

        # 处理数据,拿到导航栏里有用的大分类
        del nav_url_list[0]
        del nav_url_list[0]
        nav_url_list.pop()

        del nav_name_list[0]
        del nav_name_list[0]
        nav_name_list.pop()

        """从这里开始对每个分类进行检测,就是先循环处理每个导航,例如日本,美国等
        1、先找出每个分类一共有多少页
        2、然后每一页开始对每一个模特进行检索,并获取每一页模特的页面地址
        3、对每一个模特页面进行访问
        """
        # 大分类
        # 0 = 中国大陆
        # 1 = 日本
        # 2 = 韩国
        # 3 = 台湾
        # 4 = 泰国
        # 5 = 欧美
        nav_inex = 0
        while nav_inex < len(nav_url_list):
            print('正在访问；' + home_url + nav_url_list[nav_inex])
            # 访问分类页面
            nav_res = getHtml(home_url + nav_url_list[nav_inex])

            # 访问成功
            if nav_res.status_code == 200:
                print('访问成功: ' + home_url + nav_url_list[nav_inex])

                # 查看分类文件夹是否存在
                nav_folder = nav_name_list[nav_inex] + '/'

                # 如果不存在就创建一个文件夹
                if not os.path.exists(nav_folder):
                    os.makedirs(nav_folder)
                    print('文件夹: ' + nav_folder + '创建成功')

                else:
                    print('文件夹: ' + nav_folder + '已经存在')

                print('正在分析: ' + nav_folder + '总页数')

                # 分析分类页面的返回信息
                nav_obj = etree.HTML(nav_res.text)

                # 筛选每个分类页面的 页面 找到分类里一共有多少页模特
                str_list = nav_obj.xpath('//a[@class="page-link"]/@href')
                str_last = str_list[len(str_list)-1]
                mode_pages_str_list = str(str_last).split('=')

                # 拼接这个分类下每个页面的访问地址
                mode_pages_url = mode_pages_str_list[0] + '='

                # 根据最后一页的href信息,找出这个分类所有模特的页面总数
                mode_pages = mode_pages_str_list[len(mode_pages_str_list)-1]
                mode_pages = int(mode_pages)
                print(nav_url_list[nav_inex] +
                      '一共有: ' + str(mode_pages) + '页数据')

                """从这里开始对是访问该分类下的每一页,例如日本这个标签里有100页
                1、可以找出这个页面里有多少个模特
                2、可以找出每个模特的地址
                3、可以进到每个模特地址进行图片操作
                """
                # 大分类页面下的页码
                # 例如: 
                # 中国大陆的 第一页
                # 从 1 开始
                # 日本 第二页
                mode_page = 4
                while mode_page <= mode_pages:

                    # 访问分类等单个页码
                    mode_res = getHtml(
                        home_url + mode_pages_url + str(mode_page))

                    print('正在访问' + nav_folder + '第' + str(mode_page) + '页')
                    print('网址: ' + home_url + mode_pages_url + str(mode_page))

                    if mode_res.status_code == 200:
                        print(nav_folder + '第' + str(mode_page) + '页' + ' 访问成功')
                        print('正在分析: '+nav_folder + '第' +
                              str(mode_page) + '页')

                        # 分析分类页面的返回信息
                        mode_obj = etree.HTML(mode_res.text)

                        # 每个分类页面里的模特的地址集合
                        mode_url_list = mode_obj.xpath(
                            '//div[@class="card-cover"]/a/@href')
                        # 模特的名字集合
                        mode_name_url_list = mode_obj.xpath(
                            '//div[@class="card-body media-meta p-2"]/div/a/text()')

                        print(nav_folder + '第' +
                              str(mode_page) + '页一共有' + str(len(mode_name_url_list)) + '个模特')

                        # 页面上的第几个模特
                        # 0 代表第一个
                        # 1 代表第二个
                        # ... 以此类推
                        mode_index = 8
                        while mode_index < len(mode_url_list):

                            # 访问每一个模特的页面
                            images_page_res = getHtml(
                                home_url + mode_url_list[mode_index])

                            print('正在访问' + nav_folder + '第' +
                                  str(mode_page) + '页的第' + str(mode_index+1) + '个模特:' + home_url + mode_url_list[mode_index])

                            if(images_page_res.status_code == 200):
                                print('访问成功,正在分析: ' + nav_folder + '第' +
                                      str(mode_page) + '页的第' + str(mode_index+1) + '个模特的图片数量（页数）')
                                # 分析模特页面里的数据
                                images_page_obj = etree.HTML(
                                    images_page_res.text)

                                # 找到图片的集合
                                image_page_url_list = images_page_obj.xpath(
                                    '//a[@class="page-link"]/@href')

                                print(nav_folder + '第' +
                                      str(mode_page) + '页的第' + str(mode_index) + '个模特的图片页数' + str(image_page_url_list))

                                image_page_temp = str(
                                    image_page_url_list[len(image_page_url_list)-1]).split('=')

                                image_page_url = image_page_temp[0] + '='
                                image_page = int(
                                    image_page_temp[len(image_page_temp)-1])
                                print(nav_folder + '第' +
                                      str(mode_page) + '页的第' + str(mode_index+1) + '个模特一共有' + str(image_page) + '页图片')

                                # 模特一共有几页照片
                                # 例如: 
                                # 这个模特有10页照片
                                # 从 1 开始
                                # 每一页是十张
                                print('开始保存图片: ')
                                image_page_index = 1
                                while image_page_index < image_page:

                                    # 访问每一个模特的每一个页面
                                    image_res = getHtml(
                                        home_url + image_page_url + str(image_page_index))
                                    print('正在访问: ' + nav_folder + '第' +
                                          str(mode_page) + '页的第' + str(mode_index+1) + '个模的第' + str(image_page_index) + '页图片')
                                    if(image_res.status_code == 200):

                                        # 分析模特页面里的数据
                                        image_obj = etree.HTML(
                                            image_res.text)
                                        print('访问成功,正在分析: ' + nav_folder + '第' +
                                              str(mode_page) + '页的第' + str(mode_index+1) + '个模的第' + str(image_page_index))
                                        # 找到图片的集合
                                        # 这里是每一页的10张图片的地址集合
                                        image_url_list = image_obj.xpath(
                                            '//div[@class="album-photo my-2"]/img/@data-src')
                                        print(nav_folder + '第' +
                                              str(mode_page) + '页的第' + str(mode_index+1) + '个模的第' + str(image_page_index) + '页有' + str(len(image_url_list)) + '几张图片')
                                        # 创建模特名字的文件夹
                                        # 查看文件夹是否存在
                                        mode_folder = nav_name_list[nav_inex] + \
                                            '/' + \
                                            mode_name_url_list[mode_index] + '/'

                                        # 如果不存在就创建一个文件夹
                                        if not os.path.exists(mode_folder):
                                            os.makedirs(mode_folder)
                                            print('文件夹: ' + mode_folder + '创建成功')
                                        else:
                                            print('文件夹: ' + mode_folder + '已经存在')

                                        # 保存每个模特的图片
                                        # 这个是记录图片的下标
                                        # 例如
                                        # 模特001.jpg  模特002.jpg
                                        image_index = 1
                                        # 每一页十张图
                                        # 一张一张的访问
                                        # 一张一张的保存
                                        for image_url in image_url_list:
                                            image_res = getHtml(image_url)

                                            if image_res.status_code == 200:
                                                with open(mode_folder + mode_name_url_list[mode_index] + '-' + str(image_page_index-1) + str(image_index) + '.jpg', 'wb') as fd:
                                                    for chunk in image_res.iter_content():
                                                        fd.write(chunk)

                                            print(mode_name_url_list[mode_index] + '-' + str(
                                                image_page_index-1) + str(image_index) + '.jpg' + '---' + '保存成功')
                                            image_index += 1
                                            time.sleep(random.randint(1, 3))
                                    else:
                                        print('访问第5层页面失败: 单个模特的图片页面')

                                    image_page_index += 1
                                    time.sleep(random.randint(1, 3))

                            else:
                                print('访问第4层页面失败')

                            mode_index += 1
                            time.sleep(random.randint(1, 3))

                    else:
                        print('访问第3层页面失败')

                    time.sleep(random.randint(1, 3))
                    mode_page += 1

            else:
                print('访问第2层页面失败')

            time.sleep(random.randint(1, 3))

    else:
        print('访问第1层页面失败, 错误码: %e' % home_res.status_code)
        return

if __name__ == '__main__':
    getImages()
