import os
from server.api import MyApi

# 下载记录
medias = []

# 找出根目录里所有的文件夹
files = os.listdir()
# 遍历根目录,找到下载历史
for file in files:
    medias_txt = ''
    # 读取下载历史数据
    if file == 'contents.txt':
        with open(file) as medias_txt_open:
            for media_txt_open in medias_txt_open.readlines():
                media_txt_open = media_txt_open.strip('\n')
                medias.append(media_txt_open)
        medias_txt_open.close()

server_url = 'https://www.pkbackend.buzz'
server_account = 'test001'

server_token = MyApi.loginServer(server_url, server_account, '123456')
if server_token == '' or server_token == '-1':
    print('\033[0;37;41m后台账号登陆失败,无法继续操作,程序即将推出...\033[0m')
    exit()

get_content = MyApi.getContentListServer(server_url, server_token, 20, 1)
if get_content == -1:
    exit()

# 推文的总页码和最后一页的数量
contents_size = get_content['data']['totalSize']
page_number = contents_size // 20
last_page_size = contents_size % 20

print('推文总数量：%d' % contents_size)

for i in range(1, page_number + 2):
    print('正在获取第 %d 页的数据' % i)
    get_content = MyApi.getContentListServer(server_url, server_token, 20, i)
    if get_content == -1:
        exit()

    for content in get_content['data']['list']:
        content_data = {}

        if content['works']['video'] == {}:
            continue

        content_data['wid'] = content['wid']
        content_data['content'] = content['works']['content']

        with open(os.path.join('', 'contents.txt'), 'a') as f:
            f.write(str(content_data) + '\n')
