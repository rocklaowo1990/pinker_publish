from server.api import MyApi

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

content_list = []

for i in range(1, page_number + 2):
    print('正在获取第 %d 页的数据' % i)
    get_content = MyApi.getContentListServer(server_url, server_token, 20, i)
    if get_content == -1:
        exit()
    content_list.extend(get_content['data']['list'])

print(len(content_list))

# for i in range(0, len(content_list)):
#     for j in range(i+1, len(content_list)):
#         if content_list[i]['works']['content'] == content_list[j]['works']['content']:
#             print(content_list[j]['works']['content'])

for i in range(0, len(content_list)):
    for j in range(i + 1, len(content_list)):
        if content_list[j]['works']['video'] == {} or content_list[i]['works'][
                'video'] == {}:
            continue
        if content_list[i]['works']['video']['url'] == content_list[j][
                'works']['video']['url']:
            print('原推文：')
            print(content_list[i]['works']['content'])
            print('重复的推文：')
            print(content_list[j]['works']['content'])