import datetime
import json
import math
import os
import platform

from moviepy.editor import VideoFileClip

from server.api import Api
from server.aws import Aws
from server.timer import Timer
from server.util import Util
from server.video import Video


# 正式代码
# 从这里开始执行
# 入口
# path:py 文件所在的根目录
# letter 是盘符的符号，windows 是 \，Mac 和 Linux 是 /
letter = '\\' if platform.system() == 'Windows' else '/'
works_path = os.path.split(os.path.realpath(__file__))[0] + letter

for i in works_path:
    if not (i.isalnum() or '\u4e00' <= i <= '\u9fa5' or i == letter):
        print('文件夹：' + works_path + ' 移动硬盘名字 或 主文件夹名字包含特殊字符，需要手动修改')
        exit()

# 找出根目录里所有的文件夹
# 每一个文件夹代表一个用户
user_files = os.listdir(works_path)

# 剔除非文件夹
Util.dirDel(user_files, works_path)

# 用户列表
users = []

# 需要处理的所有推文数量
contents_all = 0

# 找出推文最多的数量
index_max = 0

# 遍历根目录
for user_file in user_files:
    # 每一个用户的数据
    data = {}

    # 用户文件的目录名
    user_path = works_path + user_file + letter
    user_path = Util.rename(user_path)
    print('正在检索用户文件夹: %s' % user_path)

    # 得到用户文件夹里的所有文件
    contents_files = os.listdir(user_path)
    Util.fileDel(contents_files)

    # 读取josn文件
    # josn 统一用 user.txt
    user_info = ''
    for txt in contents_files:
        if 'user.txt'.upper() in txt.upper() or 'user.json'.upper() in txt.upper():
            with open(user_path + txt, encoding='UTF-8', errors='ignore') as user_info_open:
                user_info = json.loads(user_info_open.read().strip())
            user_info_open.close()

    if user_info == '':
        print('没有找到 user.txt 文件，跳过该用户...')
        continue

    # 储存用户信息
    data['info'] = user_info
    data['contents'] = []
    data['token'] = ''
    data['groups'] = []

    # 去除非文件夹
    Util.dirDel(contents_files, user_path)

    # 遍历所有的推文文件夹
    for content_file in contents_files:
        content_path = user_path + content_file + letter
        content_path = Util.rename(content_path)
        print('正在检索推文文件夹：%s' % content_path)
        medias = os.listdir(content_path)
        Util.fileDel(medias)

        content_data = {}
        content_data_pics = []
        content_data_video = ''
        content_data_duration = 0
        content_data_info = {}

        content_data['pass'] = False

        for media in medias:
            if media == 'pass':
                content_data['pass'] = True

        if content_data['pass']:
            print('检测到 pass 文件，跳过...')
            continue

        # 读取图片和视频的路径
        for media in medias:
            if '.png'.upper() in media.upper() or '.jpg'.upper() in media.upper() or '.jpeg'.upper() in media.upper():
                image_path = content_path + media
                image_path = Util.rename(image_path)
                content_data_pics.append(image_path)
            elif '.mp4'.upper() in media.upper():
                content_data_video = content_path + media
                content_data_video = Util.rename(content_data_video)
                content_data_duration = math.ceil(
                    (VideoFileClip(content_data_video).duration))
            elif 'content.txt'.upper() in media.upper() or 'content.json'.upper() in media.upper():
                # 读取josn文件
                content_info_open = open(
                    content_path + media, encoding='UTF-8', errors='ignore')
                content_data_info = json.loads(
                    content_info_open.read().strip())
                content_info_open.close()

        if content_data_pics == [] and content_data_video == '' or content_data_info == {}:
            print('文件不合法,缺少媒体文件或者 content.txt 请检查文件夹...')
            continue
        content_data['pics'] = content_data_pics
        content_data['video'] = content_data_video
        content_data['duration'] = content_data_duration
        content_data['info'] = content_data_info
        content_data['path'] = content_path
        data['contents'].append(content_data)

        contents_all += 1

        # 算出最大的推文数量
        if(len(data['contents']) > index_max):
            index_max = len(data['contents'])

    if data['contents'] != [] and data['info'] != '':
        users.append(data)


print('本次要处理的用户：' + str(len(users)) + ' 推文总数量：' + str(contents_all))
print('最多的推文数量为：' + str(index_max))
if contents_all == 0 or len(users) == 0:
    print('本次没有需要执行的任务，退出程序')
    exit()


environment = False
api_url = ''
while not environment:
    environment_input = input('请输入环境(0: 测试环境  1: 正式环境)：')
    if environment_input == '' or environment_input == '0':
        print('资源将上传到测试环境服务器')
        api_url = 'https://www.pkappdev.xyz'
        environment = True
    elif environment_input == '1':
        print('资源将上传到正式线服务器')
        api_url = 'https://www.pkapp.buzz'
        environment = True
    else:
        print('环境输入错误，请重新输入')


time_true = False
publish_time = 3
while not time_true:
    publish_time_input = input('请输入发推的时间例如(22:15),在这里输入发推时间吧：')
    if publish_time_input == '0' or publish_time_input == '':
        print('设定的发推时间为：立刻')
        time_true = True
    else:
        time_list = publish_time_input.split(':')
        true_length = 0

        for time_value in time_list:
            if time_value.isdigit():
                true_length += 1

        if true_length == len(time_list):
            time_now = datetime.datetime.now()
            if true_length < 2:
                if int(time_list[0]) >= 24:
                    time_list[0] = '00'
                time_str = time_now.strftime(
                    '%Y-%m-%d') + ' ' + time_list[0] + ':00:00'
            elif true_length < 3:
                if int(time_list[0]) >= 24:
                    time_list[0] = '00'
                if int(time_list[1]) >= 60:
                    time_list[1] = '00'
                time_str = time_now.strftime(
                    '%Y-%m-%d') + ' ' + time_list[0] + ':' + time_list[1]+':00'
            else:
                if int(time_list[0]) >= 24:
                    time_list[0] = '00'
                if int(time_list[1]) >= 60:
                    time_list[1] = '00'
                if int(time_list[2]) >= 60:
                    time_list[2] = '00'
                time_str = time_now.strftime(
                    '%Y-%m-%d') + ' ' + time_list[0] + ':' + time_list[1] + ':' + time_list[2]

            time_pub = datetime.datetime.strptime(
                time_str, '%Y-%m-%d %H:%M:%S')
            publish_time = (time_pub - time_now).seconds
            print('设定的发推时间为：%s' % time_pub)
            time_true = True

        else:
            print('发推时间输入有误')


compress_pass = False
commpress_type = 0
while not compress_pass:
    commpress_input = input('请输入视频处理方式（0 不处理 1 压缩 2 裁切片头片尾 ) ：')

    if commpress_input == '0' or commpress_input == '':
        print('视频不做处理，将直接上传')
        compress_pass = True

    elif commpress_input == '1':
        print('将对视频进行压缩处理')
        compress_pass = True
        commpress_type = 1

    elif commpress_input == '2':
        print('将对视频进行裁切并压缩处理')
        compress_pass = True
        commpress_type = 2
    else:
        print('是否压缩选择输入有误')

Timer.waitTime(publish_time)


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
    print('登陆失败：登录时获取配置失败')
    exit()

# 开始执行发推部分
# 一个用户发一条，轮流发送
# 顺序执行
print('开始执行发推程序')

succ = 0

index = 0
while index < index_max:
    for work in users:

        if index < len(work['contents']):
            content_info = work['contents'][index]['info']
            account = work['info']['account']
            password = work['info']['password']
            token = work['token']
            video_path = work['contents'][index]['video']
            pics_path = work['contents'][index]['pics']
            video_duration = work['contents'][index]['duration']
            groups = work['groups']
            print('---------------------------------------------------------------------')
            print('即将处理用户：' + account + ' 的第 ' + str(index + 1) + ' 条推文')
            if video_path != '':
                print('文件夹目录：' + video_path)
            else:
                print('文件夹目录：' + pics_path[0])

            if work['contents'][index]['pass'] == True:
                print('检测到跳过标记：跳过处理')
                continue

            # 这里是登录模块
            # token = ’‘ 表示没有登录过，执行登录方法
            # token = ’-1‘ 表示曾经登录失败过，跳过
            if token == '':
                login = Api.login(api_url, account, password, enKey)
                work['token'] = login
                token = login
                if login == '' or login == '-1':
                    continue

            elif token == '-1':
                print(account + ' 的账号登录失败过，跳过处理')
                continue

            # 准备发推的数据
            # content_info = contents_info[index]
            publish_data = {}
            data_pics = []

            # 先请求一下订阅组的接口
            # 如果发推的信息设置的不对就可以跳出，避免撒谎给你传资源后发不了
            groups = Api.myGroupList(api_url, token, account)

            if groups == 1:
                login = Api.login(api_url, account, password, enKey)
                work['token'] = login
                token = login
                if login == '' or login == '-1':
                    continue
                groups = Api.myGroupList(api_url, token, account)
            work['groups'] = groups

            if content_info['payPermissionType'] == 0:
                publish_data['payPermissionType'] = 0

            elif content_info['payPermissionType'] == 1:
                publish_data['payPermissionType'] = 1
                if groups == []:
                    print('没有找到相关的订阅组设置：退出')
                    continue
                else:
                    for group in groups:
                        if group['groupName'] == content_info['payGroupIdName']:
                            publish_data['payGroupId'] = group['groupId']
                            break
                if not 'payGroupId' in publish_data.keys():
                    print('没有找到相关的订阅组设置：跳过处理...')
                    continue

            elif content_info['payPermissionType'] == 2 or content_info['payPermissionType'] == 3:
                publish_data['payPermissionType'] = content_info['payPermissionType']
                if groups == []:
                    print('没有找到相关的订阅组设置：退出')
                    continue
                else:
                    for group in groups:
                        if group['groupName'] == content_info['payGroupIdName']:
                            publish_data['payGroupId'] = group['groupId']
                            break
                if not 'payGroupId' in publish_data.keys():
                    print('没有找到相关的订阅组设置：跳过处理...')
                    continue
                publish_data['payPrice'] = content_info['payPrice']

            elif content_info['payPermissionType'] == 4:
                publish_data['payPermissionType'] = 4
                publish_data['payPrice'] = content_info['payPrice']

            # 公共数据
            # publish_data['content']: 推文的文本信息
            # publish_data['replyPermissionType']：推文的回复权限
            # content_info['limitFreeDays']：推文的限免设置
            publish_data['content'] = content_info['content']
            publish_data['replyPermissionType'] = 1
            if content_info['limitFreeDays'] != 0:
                publish_data['limitFreeDays'] = content_info['limitFreeDays']

            # 如果视频路径不是空的，那就当成视频推文去发
            if video_path != '':
                # 是否可以删掉视频文件
                # 默认Flase，不可以删除
                is_can_delete = False

                # 抽取视图片
                if 3 - len(pics_path) > 0:
                    video_pics = Video.getImage(
                        video_path, video_duration, len(pics_path))
                    pics_path.extend(video_pics)

                # 判断是否需要压缩
                if commpress_type == 1:
                    compress_video = Video.compressVideo(video_path)
                    if compress_video != '':
                        video_path = compress_video
                        is_can_delete = True
                    else:
                        continue
                elif commpress_type == 2:
                    compress_video = Video.cutVideo(video_path, video_duration)
                    if compress_video != '':
                        video_path = compress_video
                        is_can_delete = True
                    else:
                        continue

                # 上传视频并拿到地址
                # 这一步也会检查文件是否已经存在
                # 如果存在的话，则会跳过
                video_upload = Aws.upload(api_url, video_path, Util.getType(
                    video_path), accessKey, secretKey, region, bucket)
                if video_upload == '-1':
                    video_upload = Aws.upload_s3(api_url, video_path, Util.getType(
                        video_path), accessKey, secretKey, region, bucket)
                if video_upload == '-1':
                    print('上传视频文件失败，无法继续执行发推...跳过处理')
                    if is_can_delete:
                        print('删除压缩文件...')
                        os.remove(video_path)
                    continue

                video_md5 = Util.getFileMd5(video_path)
                video_url = 'public/' + video_md5 + \
                    '.' + Util.getType(video_path)

                for pic_path in pics_path[:3]:
                    pic_md5 = Util.getFileMd5(pic_path)
                    pic_upload = Aws.upload(api_url, pic_path, Util.getType(
                        pic_path), accessKey, secretKey, region, bucket)
                    if pic_upload == '-1':
                        pic_upload = Aws.upload_s3(api_url, pic_path, Util.getType(
                            pic_path), accessKey, secretKey, region, bucket)
                    if pic_upload == '-1':
                        print('图片上传失败，无法继续执行发推...跳过处理')
                        continue
                    data_pics.append('public/' + pic_md5 +
                                     '.' + Util.getType(pic_path))

                publish_data['video'] = '{"url":"%s","format":"%s","duration":"%s","snapshot_url":"%s","previews_urls":"%s,%s,%s"}' % (video_url, Util.getType(
                    video_path), video_duration, data_pics[0], data_pics[0], data_pics[1], data_pics[2])

            # 如果是空的，说明没有视频，那就当成图片推文去发
            else:
                if content_info['payPermissionType'] != 0 and pics_path < 4:
                    print('收费的图片推文，图片必须要大于三张，跳过处理')
                    continue
                suss = 0
                for pic_path in pics_path:
                    pic_md5 = Util.getFileMd5(pic_path)
                    pic_upload = Aws.upload(api_url, pic_path, Util.getType(
                        pic_path), accessKey, secretKey, region, bucket)
                    if pic_upload == '-1':
                        pic_upload = Aws.upload_s3(api_url, pic_path, Util.getType(
                            pic_path), accessKey, secretKey, region, bucket)
                    if pic_upload != '-1':
                        suss += 1
                        data_pics.append('public/' + pic_md5 +
                                         '.' + Util.getType(pic_path))

                if content_info['payPermissionType'] != 0 and succ < 4:
                    print('收费的图片推文，上传成功的图片必须要大于三张，无法继续发推')
                    continue
                publish_data['pics'] = ','.join(data_pics)

            # 开始执行发推
            # 调用发推的接口
            publish = Api.publish(api_url, token, publish_data, account)

            if publish == 1:
                login = Api.login(api_url, account, password, enKey)
                work['token'] = login
                token = login
                publish = Api.publish(api_url, token, publish_data, account)
                if login == '' or login == '-1':
                    continue
            elif publish == 200:
                succ += 1
                # 创建标记，标记为已经处理过
                passFlie = open(work['contents'][index]['path'] + 'pass', 'w')
                passFlie.close()

            if video_path != '' and is_can_delete:
                print('删除压缩文件...')
                os.remove(video_path)

            print(account + ' 的第 ' + str(index + 1) + ' 条推文处理完成')

    index += 1

print('---------------------------------------------------------------------')
print('处理完毕: 一共处理了 ' + str(contents_all) + ' 条推文，成功发推 ' +
      str(succ) + ' 条 失败 ' + str(contents_all - succ) + ' 条')
