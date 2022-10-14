import os
from lxml import etree
from server.requests import MyRequests

# 下载记录
medias = []

# 找出根目录里所有的文件夹
# 每一个文件夹代表一个用户
files = os.listdir()
# 遍历根目录,找到下载历史
for file in files:
    medias_txt = ''
    # 读取下载历史数据
    if file == 'video_history.txt':
        with open(file) as medias_txt_open:
            for media_txt_open in medias_txt_open.readlines():
                media_txt_open = media_txt_open.strip('\n')
                medias.append(media_txt_open)
        medias_txt_open.close()

# 首页地址
home_url = 'https://www.tgbak.com'

# 请求首页
print('正在请求首页:%s' % home_url)
requests_home = MyRequests.get(home_url)

# 访问首页成功
if requests_home.status_code == 200:
    print('----\033[0;32;40m访问成功\033[0m')
    # 拿到首页的返回数据
    home_obj = etree.HTML(requests_home.text)

    # 拿到二级页面的所有地址
    secondary_tiles = list(home_obj.xpath('//td[@class="fb-n"]/a/text()'))
    secondary_urls = list(home_obj.xpath('//td[@class="fb-n"]/a/@href'))

    print('请选择要下载的目录:')
    index = 0
    while index < len(secondary_tiles):
        print('%d: %s' % (index, secondary_tiles[index]))
        index += 1

    input_true = False
    index = 0
    while not input_true:
        index_input = input('请输入要下载的目录：）: ')
        if index_input == '' or index_input == '0':
            index = 0
            input_true = True
            print('----\033[0;36;40m即将开始下载目录 %s 的资源\033[0m' %
                  secondary_tiles[index])

        elif index_input.isdigit():
            if int(index_input) < len(secondary_tiles) - 1:
                index = int(index_input)
                input_true = True
                print('----\033[0;36;40m即将开始下载目录 %s 的资源\033[0m\033[0m' %
                      secondary_tiles[index])
            else:
                print('----\033[0;37;41m请输入 0 - %d 之间的数字...\033[0m' %
                      (len(secondary_tiles) - 1))

        else:
            print('----\033[0;37;41m请输入数字...\033[0m')

    # 根据选择的目录进行下载
    down_path = os.path.join('videos', secondary_tiles[index])
    down_url = home_url + secondary_urls[index]
    MyRequests.parse(down_url, down_path, '/', medias, '')
