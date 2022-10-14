import json
import os

from server.api import MyApi
from server.timer import MyTimer
from server.util import MyUtil

works_path = os.path.join('', 'works')

if not os.path.exists(works_path):
    print('----\033[0;37;41m没有找到 works 文件夹, 退出...\033[0m')
    exit()
else:
    print('----\033[0;32;40m找到 works 文件夹正在检索...\033[0m')

    # 找出根目录里所有的文件夹
    # 每一个文件夹代表一个用户
    task_files = os.listdir(works_path)
    MyUtil.getFile(task_files)

    tasks = []

    if task_files == []:
        print('----\033[0;37;41m没有检测到任何相关的数据 退出...\033[0m')
        exit()

    # 遍历根目录
    for task_file in task_files:
        print(
            '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        )
        task_path = os.path.join(works_path, task_file)
        print('正在检索任务文件: %s' % task_path)

        task_data = {}

        if '.txt'.upper() in task_file.upper():
            with open(task_path) as info_open:
                info_json = json.loads(info_open.read().strip())
                if not 'account' in info_json or not 'password' in info_json:
                    print('----\033[0;33;40m用户信息文件不太正常, 跳过处理...\033[0m')
                    print('----\033[0;33;40m文件目录:[ %s ]\033[0m' % task_path)
                    continue
                else:
                    task_data['data'] = info_json
                    task_data['path'] = task_path
                    tasks.append(task_data)
                    print('----\033[0;32;40m用户信息导入成功...\033[0m')

            info_open.close()

print('检索完成...')
print('本次要处理的任务数量: \033[0;32m' + str(len(tasks)) + ' \033[0m')
if tasks == []:
    print('\033[0;37;41m本次没有需要执行的任务,已退出程序...\033[0m')
    exit()
input('输入回车键继续...')

# 读取加密设置
# aws 桶信息
# salt 信息
accessKey = ''
secretKey = ''
bucket = ''
enKey = ''
iv = ''
region = ''
api_url = 'https://www.pkapp.buzz'

get_config = MyApi.get_config(api_url)
if get_config != '':
    accessKey = get_config['accessKey']
    secretKey = get_config['secretKey']
    bucket = get_config['bucket']
    enKey = get_config['enKey']
    iv = get_config['iv']
    region = get_config['region']
else:
    print('\033[0;37;41m获取系统配置失败\033[0m')
    exit()

index = 0
for task in tasks:
    print(
        '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    )
    print('即将处理第 %d 个用户: %s' % (index + 1, task['data']['account']))
    print('----\033[0;32;40m文件夹目录: %s \033[0m' % task['path'])

    MyTimer.waitTime(3)

    # 这里是登录模块
    # token = ’‘ 表示没有登录过,执行登录方法
    # token = ’-1‘ 表示曾经登录失败过,跳过

    token = MyApi.login(api_url, task['data']['account'],
                        task['data']['password'], enKey)
    if token == '' or token == '-1':
        continue

    # 订阅组获取
    pay_group_ids = MyApi.myGroupList(api_url, token, task['data']['account'])
    if pay_group_ids == []:
        continue
    print(pay_group_ids)

    # 获取推文的总数量
    contents_size = MyApi.getContentSize(api_url, token)

    # 推文的总页码和最后一页的数量
    page_number = contents_size // 20
    page_size = contents_size % 20

    # 推文列表
    task_contents = []

    page_number_index = 0
    while page_number_index <= page_number:
        _page_size = page_size if page_number_index == page_number else 20
        task_contents.extend(
            MyApi.getContentList(api_url, token, page_number_index + 1,
                                 _page_size))
        page_number_index += 1

    task_content_index = 0
    for task_content in task_contents:
        print('即将处理第 %d 条作品...' % (task_content_index + 1))

        content_pass = False
        for pay_group_id in pay_group_ids:
            if pay_group_id == task_content['works']['payPermission'][
                    'groupId']:
                content_pass = True

        if content_pass:
            continue

        MyTimer.waitTime(1)

        publish_data = {}

        publish_data['content'] = task_content['works']['content']
        publish_data[
            'video'] = '{"url":"%s","format":"%s","duration":"%s","snapshot_url":"%s","previews_urls":"%s,%s,%s"}' % (
                task_content['works']['video']['url'],
                task_content['works']['video']['format'],
                task_content['works']['video']['duration'],
                task_content['works']['video']['snapshot_url'],
                task_content['works']['video']['previews_urls'][0],
                task_content['works']['video']['previews_urls'][1],
                task_content['works']['video']['previews_urls'][2],
            )
        publish_data['payPermissionType'] = task_content['works'][
            'payPermission']['type']
        publish_data['payGroupId'] = pay_group_ids[0]['groupId']
        publish_data['payPrice'] = task_content['works']['payPermission'][
            'price']
        publish_data['limitFreeDays'] = task_content['works']['payPermission'][
            'limitFreeDays']
        publish_data['replyPermissionType'] = task_content['works'][
            'replyPermission']['type']

        re_publish = MyApi.publish(api_url, token, publish_data,
                                   task['data']['account'])
        task_delete = MyApi.contentDel(api_url, token, task_content['wid'])
        task_content_index += 1

    index += 1

print('任务处理完毕...')
