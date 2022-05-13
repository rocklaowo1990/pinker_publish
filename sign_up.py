
import json
import os
import platform

from server.api import Api
from server.aws import Aws
from server.timer import Timer
from server.util import Util

# 正式代码
# 从这里开始执行
# 入口
# path:py 文件所在的根目录
# letter 是盘符的符号,windows 是 \,Mac 和 Linux 是 /
letter = '\\' if platform.system() == 'Windows' else '/'
works_path = os.path.split(os.path.realpath(__file__))[0] + letter

# 找出根目录里所有的文件夹
# 每一个文件夹代表一个用户
# users: 用户
user_files = os.listdir(works_path)
# 剔除非文件夹
Util.dirDel(user_files, works_path)

'''
变量区: 
users: 用户集合,需要处理的所有用户数量
token_server: 后台的token
api_url: api 的接口地址
server_url: 后台的接口地址
'''
users = []
token_server = ''
api_url = ''
server_url = ''

# 遍历根目录
for user_file in user_files:
    # 每一个用户的数据
    data = {}

    # 用户文件的目录名
    user_path = works_path + user_file + letter
    print('正在检索文件夹: %s' % user_path)

    # 得到用户文件夹里的所有文件
    files = os.listdir(user_path)
    Util.fileDel(files)
    pics = ['', '', '']

    for file in files:
        # 检查图片文件
        if '000'.upper() in file.upper():
            data['avatar'] = user_path + file
        # 检查图片文件
        elif '001'.upper() in file.upper():
            pics[0] = user_path + file
        elif '002'.upper() in file.upper():
            pics[1] = user_path + file
        elif '003'.upper() in file.upper():
            pics[2] = user_path + file
        # 检查txt文件
        elif 'info.txt'.upper() in file.upper() or 'info.json'.upper() in file.upper():
            # 读取josn文件
            content_info_open = open(user_path + file, encoding='UTF-8', errors='ignore')
            data['info'] = json.loads(content_info_open.read().strip())
            content_info_open.close()

    Util.fileDel(pics)

    data['pics'] = pics
    data['token'] = ''
    if not 'avatar' in data.keys():
        print('缺少 000.jpg 文件,跳过处理')
    elif not 'info' in data.keys():
        print('缺少 info.txt 文件,跳过处理')
    else:
        print('发现一个合法文件,正在载入...')
        users.append(data)

print('本次需要处理的注册用户: %d 个' % len(users))
if len(users) == 0:
    print('本次没有需要执行的任务: 程序即将退出...')
    exit()

environment = False
while not environment:
    environment_input = input('请输入环境(0: 测试环境  1: 正式环境): ')
    if environment_input == '' or environment_input == '0':
        print('注册到测试环境服务器')
        api_url = 'https://www.pkappsim.xyz'
        server_url = 'https://www.pkbackendsim.xyz'
        server_account = 'admin'
        environment = True
    elif environment_input == '1':
        print('注册到正式线服务器')
        api_url = 'https://www.pkapp.buzz'
        server_url = 'https://www.pkweb.buzz'
        server_account = 'test001'
        environment = True
    else:
        print('环境输入错误,请重新输入')
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

config = Api.config(api_url)
if config != '':
    accessKey = config['accessKey']
    secretKey = config['secretKey']
    bucket = config['bucket']
    enKey = config['enKey']
    iv = config['iv']
    region = config['region']
else:
    print('获取全局配置失败,无法继续操作,即将退出程序...')
    exit()

# 开始登陆后台
logoin_server_res = Api.loginServer(server_url, server_account, '123456')
if logoin_server_res == '' or logoin_server_res == '-1':
    print('后台账号登陆失败,无法继续操作,程序即将推出...')
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

    print('---------------------------------------------------------------------')
    print('即将处理第 %d 个用户: %s' % (user_index, account))
    Timer.waitTime(1)

    # 检查账号是否已经存在
    check_res = Api.checkAccount(api_url, account)
    if check_res != 200:
        print('跳过处理...')
        continue

    # 注册账号
    sign_up_res = Api.signUp(server_url, token_server,
                             account, password, area_code, enKey)
    if sign_up_res == -1:
        print('跳过处理...')
        continue

    # 登陆APP
    login_res = Api.login(api_url, account, password, enKey)
    if login_res == '-1' or login_res == '':
        print('跳过处理...')
        continue
    else:
        token = login_res

    # 上传用户头像,并拿到地址
    avatar_md5 = Util.getFileMd5(avatar_path)
    avatar_upload = Aws.upload(api_url, avatar_path, Util.getType(
        avatar_path), accessKey, secretKey, region, bucket)
    if avatar_upload != '-1':
        avatar = 'public/' + avatar_md5 + '.' + Util.getType(avatar_path)

    # 修改用户信息
    user_info_res = Api.userInfo(
        api_url, token, avatar, nikeName, birthday, intro)

    group_max = len(pics)
    if len(groups) < len(pics):
        group_max = len(groups)

    # 添加分组
    group_index = 0
    while group_index < group_max:
        # 上传用户头像,并拿到地址
        pic_url = ''
        pic_md5 = Util.getFileMd5(pics[group_index])
        pic_upload = Aws.upload(api_url, pics[group_index], Util.getType(
            pics[group_index]), accessKey, secretKey, region, bucket)
        if pic_upload != '-1':
            pic_url = 'public/' + pic_md5 + '.' + Util.getType(avatar_path)
        print(pic_url)
        add_group_res = Api.addGroup(
            api_url, token, groups[group_index]['groupName'], pic_url, groups[group_index]['amount'])

        group_index += 1

print('---------------------------------------------------------------------')
print('处理完毕...')
