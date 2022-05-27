
import json
import os

from server.api import MyApi
from server.timer import MyTimer
from server.util import MyUtil






# 找出根目录里所有的文件夹
# 每一个文件夹代表一个用户
tasks_files = os.listdir()
# 剔除非文件夹
MyUtil.getFolder(tasks_files, '')
MyUtil.rename(tasks_files, '')

if tasks_files == []:
    print('\033[0;37;41没有检测到任何相关的数据 退出...\033[0m')

tasks = []

# 遍历根目录
for tasks_file in tasks_files:
    # 用户文件的目录名

    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('正在检索任务文件夹: %s' % tasks_file)

    task_data = {}

    in_info = {}
    out_info = {}

    out_info_infos = []
    out_info_paths = []

    # 获取转入用户的数据
    user_txt_path = os.path.join(tasks_file,'user.txt')

    if not os.path.exists(user_txt_path):
        print('----\033[0;33;40m没有找到 user.txt 文件,跳过该用户...\033[0m')
        continue
    else:
        print('----\033[0;32;40m找到 user.txt 文件正在读取...\033[0m')
        with open(user_txt_path) as user_info_open:
            in_info = json.loads(user_info_open.read().strip())
        user_info_open.close()

    if not 'account' in in_info  or not 'password' in in_info:
        print('----\033[0;33;40m用户的数据存在问题...\033[0m')
        print('----\033[0;33;40m有问题的文件路径: [ %s ]\033[0m' % user_txt_path)
        continue
    else:
        print('----\033[0;32;40m用户数据读取成功...\033[0m')


    
    # 获取转出用户的数据
    outs_path = os.path.join(tasks_file, '转出')

    if not os.path.exists(outs_path):
        print('----\033[0;33;40m没有找到 转出 文件夹,跳过该用户...\033[0m')
        continue
    else:
        print('----\033[0;32;40m找到 转出 文件夹, 正在扫描...\033[0m')

        task_files = os.listdir(outs_path)
        MyUtil.getFile(task_files)
        MyUtil.rename(task_files, outs_path)

        for task_file in task_files:
            task_path = os.path.join(outs_path, task_file)
            if '.txt'.upper() in task_file.upper():
                with open(task_path) as out_info_open:
                    out_info = json.loads(out_info_open.read().strip())
                    out_info_infos.append(out_info)
                    out_info_paths.append(task_path)
                    print('----\033[0;32;40m转入用户信息导入成功...\033[0m')

                out_info_open.close()
                    

        out_info['infos'] = out_info_infos
        out_info['paths'] = out_info_paths

        if in_info == {} or out_info == {}:
            print('\033[0;33;40m转入用户数据或者转出用户数据为空 跳过处理...\033[0m')
            continue

        task_data['in_info'] = in_info
        task_data['out_info'] = out_info
        task_data['path'] = task_path

        tasks.append(task_data)

print('检索完成...')
print('本次要处理的任务数量: \033[0;32m' + str(len(tasks)) + ' \033[0m')

if tasks == []:
    print('\033[0;37;41m本次没有需要执行的任务,已退出程序...\033[0m')
    exit()

input('输入回车键继续...')
MyTimer.waitTime(5)

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

config = MyApi.config(api_url)
if config != '':
    accessKey = config['accessKey']
    secretKey = config['secretKey']
    bucket = config['bucket']
    enKey = config['enKey']
    iv = config['iv']
    region = config['region']
else:
    print('\033[0;37;41m获取系统配置失败\033[0m')
    exit()

index = 0
for task in tasks:
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('即将处理第 %d 个用户: %s' % (index + 1, task['in_info']['account']))
    print('----\033[0;32;40m文件夹目录: %s \033[0m' % task['path'])

    MyTimer.waitTime(3)

    # 这里是登录模块
    # token = ’‘ 表示没有登录过,执行登录方法
    # token = ’-1‘ 表示曾经登录失败过,跳过

    in_token = MyApi.login(
        api_url, task['in_info']['account'], task['in_info']['password'], enKey)
    if in_token == '' or in_token == '-1':
        continue

    # 订阅组获取
    pay_group_ids = MyApi.myGroupList(
        api_url, in_token, task['in_info']['account'])
    if pay_group_ids == []:
        continue

    for out_user in task['out_info']['infos']:
        out_token = MyApi.login(
            api_url, out_user['account'], out_user['password'], enKey)
        if out_token == '' or out_token == '-1':
            continue

        contents_size = MyApi.getContentSize(api_url, out_token)

        page_number = contents_size // 20
        page_size = contents_size % 20

        out_contents = []
        page_number_index = 0

        while page_number_index <= page_number:
            out_contents_page_size = page_size if page_number_index == page_number else 20
            out_contents.extend(MyApi.getContentList(
                api_url, out_token, page_number_index + 1, out_contents_page_size))
            page_number_index += 1

        out_content_index = 0
        for out_content in out_contents:
            print('即将添加第 %d 条作品...' % (out_content_index + 1))
            MyTimer.waitTime(1)

            publish_data = {}

            publish_data['content'] = out_content['works']['content']
            publish_data['video'] = '{"url":"%s","format":"%s","duration":"%s","snapshot_url":"%s","previews_urls":"%s,%s,%s"}' % (
                out_content['works']['video']['url'],
                out_content['works']['video']['format'],
                out_content['works']['video']['duration'],
                out_content['works']['video']['snapshot_url'],
                out_content['works']['video']['previews_urls'][0],
                out_content['works']['video']['previews_urls'][1],
                out_content['works']['video']['previews_urls'][2],
            )
            publish_data['payPermissionType'] = out_content['works']['payPermission']['type']
            publish_data['payGroupId'] = pay_group_ids[0]['groupId']
            publish_data['payPrice'] = out_content['works']['payPermission']['price']
            publish_data['limitFreeDays'] = out_content['works']['payPermission']['limitFreeDays']
            publish_data['replyPermissionType'] = out_content['works']['replyPermission']['type']

            in_publish = MyApi.publish(
                api_url, in_token, publish_data, task['in_info']['account'])

            out_delete = MyApi.contentDel(
                api_url, out_token, out_content['wid'])

            out_content_index += 1

    index += 1
print('任务处理完毕...')