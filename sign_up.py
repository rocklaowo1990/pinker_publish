import imghdr
import json
import os

from server.api import MyApi
from server.aws import MyAws
from server.timer import MyTimer
from server.util import MyUtil

# 找出根目录里所有的文件夹
# 每一个文件夹代表一个用户
# users: 用户
user_files = os.listdir()
# 剔除非文件夹
MyUtil.getFolder(user_files, '')
MyUtil.rename(user_files, '')

#-------------------------------------------------------------------------------
# 变量区:
# users: 用户集合,需要处理的所有用户数量
# token_server: 后台的token
# api_url: api 的接口地址
# server_url: 后台的接口地址
#-------------------------------------------------------------------------------

users = []
token_server = ''
api_url = ''
server_url = ''

# 遍历根目录
for user_file in user_files:
    # 每一个用户的数据
    data = {}

    # 用户文件的目录名
    print('正在检索文件夹: %s' % user_file)

    # 得到用户文件夹里的所有文件
    files = os.listdir(user_file)
    MyUtil.getFile(files)

    pics = ['', '', '']

    for file in files:
        file_path = os.path.join(user_file, file)
        # 检查图片文件
        if '000'.upper() in file.upper():
            image_check = imghdr.what(file_path)
            if image_check != None:
                data['avatar'] = file_path
                print('----\033[0;32;40m头像读取成功...\033[0m')
            else:
                print('----\033[0;37;41m%s 不是有效的图片文件...\033[0m' % file_path)
        # 检查图片文件
        elif '001'.upper() in file.upper():
            image_check = imghdr.what(file_path)
            if image_check != None:
                pics[0] = file_path
                print('----\033[0;32;40m头像读取成功...\033[0m')
            else:
                print('----\033[0;37;41m%s 不是有效的图片文件...\033[0m' % file_path)
        elif '002'.upper() in file.upper():
            image_check = imghdr.what(file_path)
            if image_check != None:
                pics[1] = file_path
                print('----\033[0;32;40m头像读取成功...\033[0m')
            else:
                print('----\033[0;37;41m%s 不是有效的图片文件...\033[0m' % file_path)
        elif '003'.upper() in file.upper():
            image_check = imghdr.what(file_path)
            if image_check != None:
                pics[2] = file_path
                print('----\033[0;32;40m头像读取成功...\033[0m')
            else:
                print('----\033[0;37;41m%s 不是有效的图片文件...\033[0m' % file_path)
        # 检查txt文件
        elif 'info.txt'.upper() in file.upper():
            # 读取json文件
            content_info_open = open(file_path,
                                     encoding='UTF-8',
                                     errors='ignore')
            data['info'] = json.loads(content_info_open.read().strip())
            content_info_open.close()

    pic_index = 0
    while pic_index < len(pics):
        if pics[pic_index] == '':
            pics.remove(pics[pic_index])
        else:
            pic_index += 1

    data['pics'] = pics
    data['token'] = ''

    if not 'avatar' in data.keys():
        print('----\033[0;33;40m缺少 000.jpg 文件,跳过处理...\033[0m')
    elif not 'info' in data.keys():
        print('----\033[0;33;40m缺少 info.txt 文件,跳过处理...\033[0m')

    else:
        print('----\033[0;32;40m发现一个合法文件 ,载入成功...\033[0m')
        users.append(data)

print('本次需要处理的注册用户: \033[0;32;40m %d \033[0m 个' % len(users))
if len(users) == 0:
    print('\033[0;37;41m本次没有需要执行的任务,已退出程序...\033[0m')
    exit()

environment = False
while not environment:
    environment_input = input('请输入环境(0: 测试环境  1: 正式环境): ')
    if environment_input == '' or environment_input == '0':
        print('----\033[0;36;40m注册到测试环境\033[0m')
        api_url = 'https://www.pkappsim.xyz'
        server_url = 'https://www.pkbackendsim.xyz'
        server_account = 'admin'
        environment = True
    elif environment_input == '1':
        print('----\033[0;36;40m注册到正式环境\033[0m')
        api_url = 'https://www.pkapp.buzz'
        server_url = 'https://www.pkweb.buzz'
        server_account = 'test001'
        environment = True
    else:
        print('----\033[0;37;41m环境输入错误,请重新输入\033[0m')

print('---------------------------------------------------------------------')
# 读取加密设置
# aws 桶信息
# salt 信息
accessKey = ''
secretKey = ''
bucket = ''
enKey = ''
iv = ''
region = ''

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

# 开始登陆后台
logoin_server_res = MyApi.loginServer(server_url, server_account, '123456')
if logoin_server_res == '' or logoin_server_res == '-1':
    print('\033[0;37;41m后台账号登陆失败,无法继续操作,程序即将推出...\033[0m')
    exit()
else:
    token_server = logoin_server_res

# 开始针对每一个用户进行处理
# 这里开始是正式的注册业务 和 设置分组信息
user_index = 0
for user in users:
    user_index += 1

    # 变量
    account = user['info']['account']
    password = user['info']['password']
    area_code = user['info']['areaCode']
    token = user['token']
    avatar_path = user['avatar']
    avatar = ''
    nikeName = user['info']['nikeName']
    birthday = user['info']['birthday']
    intro = user['info']['intro']
    groups = user['info']['groups']
    pics = user['pics']

    print(
        '---------------------------------------------------------------------'
    )
    print('即将处理第 %d 个用户: %s' % (user_index, account))
    MyTimer.waitTime(1)

    # 检查账号是否已经存在
    check_res = MyApi.checkAccount(api_url, account)
    if check_res != 200:
        continue

    # 注册账号
    sign_up_res = MyApi.signUp(server_url, token_server, account, password,
                               area_code, enKey)
    if sign_up_res == -1:
        print('跳过处理...')
        continue

    # 登陆APP
    login_res = MyApi.login(api_url, account, password, enKey)
    if login_res == '-1' or login_res == '':
        print('跳过处理...')
        continue
    else:
        token = login_res

    # 上传用户头像,并拿到地址
    avatar_md5 = MyUtil.getFileMd5(avatar_path)
    avatar_upload = MyAws.upload(api_url, avatar_path,
                                 MyUtil.getType(avatar_path), accessKey,
                                 secretKey, region, bucket)
    if avatar_upload != '-1':
        avatar = 'media/image/org/' + avatar_md5 + '.' + MyUtil.getType(
            avatar_path)

    # 修改用户信息
    user_info_res = MyApi.userInfo(api_url, token, avatar, nikeName, birthday,
                                   intro)

    group_max = len(pics)
    if len(groups) < len(pics):
        group_max = len(groups)

    # 添加分组
    group_index = 0
    while group_index < group_max:
        # 上传用户头像,并拿到地址
        pic_url = ''
        pic_md5 = MyUtil.getFileMd5(pics[group_index])

        pic_upload = MyAws.upload(api_url, pics[group_index],
                                  MyUtil.getType(pics[group_index]), accessKey,
                                  secretKey, region, bucket)
        if pic_upload != '-1':
            pic_url = 'media/image/org/' + pic_md5 + '.' + MyUtil.getType(
                avatar_path)
        print(pic_url)
        add_group_res = MyApi.addGroup(api_url, token,
                                       groups[group_index]['groupName'],
                                       pic_url, groups[group_index]['amount'])

        group_index += 1

print('---------------------------------------------------------------------')
print('处理完毕...')
