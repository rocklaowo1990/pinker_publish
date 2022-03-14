import datetime
import errno
import json
import math
from multiprocessing.sharedctypes import Value
import os
import random
import sys
import numpy
import requests
import hashlib
import platform
import time
from boto3.session import Session
from moviepy.editor import VideoFileClip
import ffmpeg
import cv2


class Values:
    api_url = 'https://api.pkpinfo.xyz'
    file_url = 'https://www.pkpresources.xyz/files/'
    salt = 'tw23it66q4w44ab'
    test = 'pinker155805-dev'
    formal = 'pinker161210-prd'


class Api:
    # 登录接口
    def Login(account: str, password: str):
        url = '/api/account/login'
        _password = password + Values.salt
        md5 = hashlib.md5()
        md5.update(_password.encode(encoding='utf-8'))
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'account': account,
            'password': md5.hexdigest(),
            'accountType': 1 if str(account).isdigit() else 2,
        }
        print('正在登录：' + account)
        time.sleep(1)
        res = requests.post(Values.api_url + url, data=data, headers=headers)
        json = res.json()
        if res.status_code == 200:
            if json['code'] == 200:
                print('账号：' + account + '登录成功')
                return str(json['data']['token'])
            else:
                print('账号 ' + account + ' 登录失败 ' + json['msg'])
                return '-1'
        else:
            print('账号：' + account + ' 登录失败 ---- code: ' +
                  res.status_code + ' ---- 错误信息：' + res.text)
            return ''

    def myGroupList(token: str):
        url = '/api/subscribeGroup/myGroupList'
        headers = {
            'Content-Type': 'application/json',
            'token': token
        }
        print('正在获取用户 %s 订阅组信息' % account)
        time.sleep(1)
        res = requests.get(Values.api_url + url, headers=headers)
        json = res.json()
        if res.status_code == 200:
            if json['code'] == 200:
                print('用户 %s 订阅组信息获取成功' % account)
                return json['data']['list']
            elif json['code'] == 1:
                print('用户 %s 的 token 过期，正在重新登录' % account)
                return 1
            else:
                print('用户 %s 订阅组信息获取失败：%s' % (account, json['msg']))
                return []
        else:
            print('用户 %s 的订阅组信息获取失败 ---- code: ' +
                  res.status_code + ' ---- 错误信息：' + res.text % account)
            return []

    def publish(token: str, data):
        url = '/api/content/publish'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'token': token
        }
        print('正在发布推文')
        time.sleep(1)
        res = requests.post(Values.api_url + url, headers=headers, data=data)
        json = res.json()
        if res.status_code == 200:
            if json['code'] == 200:
                print('用户 %s 推文发布成功' % account)
                return 200
            elif json['code'] == 1:
                print('用户 %s 的 token 过期，正在重新登录' % account)
                return 1
            else:
                print('用户 %s 推文发布失败 %s' % (account, json['msg']))
                return -1
        else:
            print('用户 %s 的推文发布失败 ---- code: ' +
                  res.status_code + ' ---- 错误信息：' + res.text % account)


class Util:

    # 等待
    def WaitTime(duration: int):
        _duration = 0
        while _duration < duration:
            if duration < 60:
                print('%d 秒后开始发推...' % (duration - _duration))
            elif duration < 3600:
                print('%d 分 %d 秒后开始发推' %
                      ((duration - _duration)//60, (duration - _duration) % 60))
            else:
                print('%d 时 %d 分 %d 秒后开始发推' %
                      ((duration - _duration)//3600, ((duration - _duration) % 3600)//60, ((duration - _duration) % 3600) % 60))
            time.sleep(1)
            _duration += 1

    # 根据分组找到ID
    def GetGroupId(group_name: str, group_list: list):
        for group in group_list:
            if group['groupName'] == group_name:
                return group['groupId']
        return 0

    # 拿到文件后缀
    def GetType(path: str):
        string_list = path.split('.')
        return string_list[len(string_list)-1]

    # 去除非文件夹的方法
    def DirDel(list: list, path: str):
        index = 0
        while index < len(list):
            if not os.path.isdir(path+list[index]):
                list.remove(list[index])
            else:
                index += 1

    # 获取文件的M D5
    def GetFileMd5(filename: str):
        if not os.path.isfile(filename):
            return
        myhash = hashlib.md5()
        f = open(filename, 'rb')
        while True:
            b = f.read(8096)
            if not b:
                break
            myhash.update(b)
        f.close()
        return myhash.hexdigest()

    # 上传文件到S3
    def Upload(file_path: str, type: str, bucket: str):

        aws_access_key_id = 'AKIAWTPT7XPD45PB7CGD'
        aws_secret_access_key = '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'
        region_name = 'ap-southeast-1'
        session = Session(aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key, region_name=region_name)

        s3 = session.resource("s3")

        upload_data = open(file_path, 'rb')
        file_md5 = Util.GetFileMd5(file_path)
        upload_key = str(file_md5) + '.' + type

        print('正在检查文件是否存在: '+file_path)
        files = session.client('s3').list_objects_v2(
            Bucket=bucket,
            Delimiter='/',
            Prefix=upload_key
        )

        if files['KeyCount'] != 0:
            print('文件已存在: ' + upload_key)
            return '1'

        print('正在上传文件：' + file_path)
        try:
            s3.Bucket(bucket).put_object(
                Key=upload_key, Body=upload_data, ACL='public-read-write')
        except Exception as e:
            print('上传文件出错：' + str(e))
            return '-1'

        print('文件上传成功')
        return upload_key


# 对象
class Works:
    list = []


# 视频处理
class VideoServer:
    def read_frame_by_time(in_file, time):
        """
        指定时间节点读取任意帧
        """
        out, err = (
            ffmpeg.input(in_file, ss=time)
            .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
            .run(capture_stdout=True)
        )
        return out

    def get_video_info(in_file):
        """
        获取视频基本信息
        """
        try:
            probe = ffmpeg.probe(in_file)
            video_stream = next(
                (stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            if video_stream is None:
                print('No video stream found', file=sys.stderr)
                sys.exit(1)
            return video_stream
        except ffmpeg.Error as err:
            print(str(err.stderr, encoding='utf8'))
            sys.exit(1)

    def GetVideoPic(video_path: str, path: str):
        video_info = VideoServer.get_video_info(video_path)
        total_duration = video_info['duration']

        index = 1
        pics = []
        while index <= 4:
            random_time = random.randint(
                1, int(float(total_duration)) - 1) + random.random()
            out = VideoServer.read_frame_by_time(video_path, random_time)

            image_array = numpy.asarray(bytearray(out), dtype="uint8")

            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            cv2.imwrite(path+'截屏图片000'+str(index)+'.png', image)
            pics.append(path+'截屏图片000'+str(index)+'.png')
            index += 1
        return pics


# 正式代码
# 从这里开始执行
# 入口
# path:py 文件所在的根目录
# letter 是盘符的符号，windows 是 \，Mac 和 Linux 是 /
letter = '\\' if platform.system() == 'Windows' else '/'
works_path = os.path.split(os.path.realpath(__file__))[0] + letter

# 找出根目录里所有的文件夹
# 每一个文件夹代表一个用户
# users: 用户
user_files = os.listdir(works_path)
# 剔除非文件夹
Util.DirDel(user_files, works_path)

# 需要处理的所有推文数量
all = 0

# 找出推文最多的数量
index_max = 0
for user_file in user_files:
    # 每一个用户的数据
    data = {}

    # 用户文件的目录名
    user_path = works_path + user_file + letter

    # 得到用户文件夹里的所有文件
    print('正在检索文件夹: %s' % user_path)
    contents_files = os.listdir(user_path)
    if len(contents_files) < 2:
        print('检测到空文件夹：跳过不处理')
        continue

    # 读取josn文件
    # josn 统一用 user.txt
    user_info_open = open(user_path + 'user.txt', encoding='UTF-8')
    user_info = json.loads(user_info_open.read())

    # 储存用户信息
    data['info'] = user_info
    data['contents'] = []
    data['token'] = ''
    data['groups'] = []

    user_info_open.close()

    # 去除非文件夹
    Util.DirDel(contents_files, user_path)

    # 算出最大的推文数量
    if(len(contents_files) > index_max):
        index_max = len(contents_files)

    all += len(contents_files)

    # 遍历所有的推文文件夹
    for content_file in contents_files:
        content_path = user_path + content_file + letter
        medias = os.listdir(content_path)
        content_data = {}

        content_data_pics = []
        content_data_video = ''
        content_data_duration = 0
        content_data_info = {}

        # 读取图片和视频的路径
        for media in medias:
            if '.png'.upper() in media.upper() or '.jpg'.upper() in media.upper() or '.jpeg'.upper() in media.upper():
                content_data_pics.append(content_path + media)
            elif '.mp4'.upper() in media.upper():
                content_data_video = (content_path + media)
                content_data_duration = math.ceil((VideoFileClip(
                    content_path + media).duration))
                print(content_path + media)
                video_pics = VideoServer.GetVideoPic(
                    content_path + media, content_path)
                print(video_pics)
                content_data_pics.extend(video_pics)
                print(content_data_pics)
            elif '.txt'.upper() in media.upper() or '.json'.upper() in media.upper():
                # 读取josn文件
                # josn 统一用 user.txt
                content_info_open = open(
                    content_path + media, encoding='UTF-8')
                content_data_info = json.loads(content_info_open.read())
                content_info_open.close()
        content_data['pics'] = content_data_pics
        content_data['video'] = content_data_video
        content_data['duration'] = content_data_duration
        content_data['info'] = content_data_info
        data['contents'].append(content_data)
    Works.list.append(data)

print('本次要处理的用户：' + str(len(Works.list)) + ' 推文总数量：' + str(all))
print('最多的推文数量为：' + str(index_max))

environment = False
bucket = ''
while not environment:
    environment_input = input('请输入环境(0: 测试环境  1: 正式环境)：')
    if environment_input == '' or environment_input == '0':
        print('资源将上传到测试环境服务器')
        bucket = Values.test
        environment = True
    elif environment_input == '1':
        print('资源将上传到正式线服务器')
        bucket = Values.formal
        environment = True
    else:
        print('环境输入错误，请重新输入')

time_true = False
publish_time = 5

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


time_true = False
wait_time = 1
while not time_true:
    wait_time_input = input('请输入发推间隔的秒数：')

    if wait_time_input == '0' and wait_time_input == '':
        print('发推间隔时间为：' + str(wait_time) + ' 秒')
        time_true = True

    elif wait_time_input.isdigit():
        wait_time = int(wait_time_input)
        print('发推间隔时间为：' + str(wait_time) + ' 秒')
        time_true = True
    else:
        print('时间间隔输入有误')

Util.WaitTime(publish_time)


# 开始执行发推部分
# 一个用户发一条，轮流发送
# 顺序执行
print('开始执行发推程序')

succ = 0

index = 0
while index < index_max:
    for work in Works.list:

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
            print('正在处理用户：' + account + ' 的第 ' + str(index + 1) + ' 条推文')

            # 这里是登录模块
            # token = ’‘ 表示没有登录过，执行登录方法
            # token = ’-1‘ 表示曾经登录失败过，跳过
            if token == '':

                login = Api.Login(account, password)
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
            groups = Api.myGroupList(token)

            if groups == 1:
                login = Api.Login(account, password)
                work['token'] = login
                token = login
                if login == '' or login == '-1':
                    continue
                groups = Api.myGroupList(token)
            work['groups'] = groups

            if content_info['payPermissionType'] == 0:
                publish_data['payPermissionType'] = 0

            elif content_info['payPermissionType'] == 1:
                if len(pics_path) < 3:
                    print('图片数量不够发布推文，跳过处理')
                    continue
                publish_data['payPermissionType'] = 1
                if groups == []:
                    print('没有找到相关的订阅组设置：退出')
                    continue
                else:
                    publish_data['payGroupId'] = Util.GetGroupId(
                        content_info['payGroupIdName'], groups)

            elif content_info['payPermissionType'] == 2 or content_info['payPermissionType'] == 3:
                if len(pics_path) < 3:
                    print('图片数量不够发布推文，跳过处理')
                    continue
                publish_data['payPermissionType'] = content_info['payPermissionType']
                if groups == []:
                    print('没有找到相关的订阅组设置：退出')
                    continue
                else:
                    publish_data['payGroupId'] = Util.GetGroupId(
                        content_info['payGroupIdName'], groups)
                publish_data['payPrice'] = content_info['payPrice']

            elif content_info['payPermissionType'] == 4:
                if len(pics_path) < 3:
                    print('图片数量不够发布推文，跳过处理')
                    continue
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
                # 上传视频并拿到地址
                # 这一步也会检查文件是否已经存在
                # 如果存在的话，则会跳过
                video_upload = Util.Upload(
                    video_path, Util.GetType(video_path), bucket)
                if video_upload == '1' or video_upload == '-1':
                    print('跳过处理')
                    continue

                for pic_path in pics_path:
                    pic_md5 = Util.GetFileMd5(pic_path)
                    pic_upload = Util.Upload(
                        pic_path, Util.GetType(pic_path), bucket)
                    if pic_upload != '-1':
                        data_pics.append(
                            pic_md5 + '.' + Util.GetType(pic_path))
                if len(data_pics) < 4:
                    print('检测到了视频，图片数量不够发布推文，跳过处理')
                    continue
                publish_data['video'] = '{"url":"%s","format":"%s","duration":"%s","snapshot_url":"%s","previews_urls":"%s,%s,%s"}' % (Util.GetFileMd5(video_path) + '.' + Util.GetType(video_path), Util.GetType(
                    video_path), video_duration, data_pics[0], data_pics[1], data_pics[2], data_pics[3])

            # 如果是空的，说明没有视频，那就当成图片推文去发
            else:

                # failed：重复或者失败的图片统计
                failed = 0
                for pic_path in pics_path:
                    pic_md5 = Util.GetFileMd5(pic_path)
                    pic_upload = Util.Upload(
                        pic_path, Util.GetType(pic_path), bucket)
                    if pic_upload == '1' or pic_upload == '-1':
                        failed += 1
                    data_pics.append(pic_md5 + '.' + Util.GetType(pic_path))

                if failed > len(pics_path) / 2:
                    print('跳过处理')
                    continue
                publish_data['pics'] = ','.join(data_pics)

            # 开始执行发推
            # 调用发推的接口
            publish = Api.publish(token, publish_data)
            if publish == 1:
                login = Api.Login(account, password)
                work['token'] = login
                token = login
                publish = Api.publish(token, publish_data)
                if login == '' or login == '-1':
                    continue
            elif publish == 200:
                succ += 1

            print(account + ' 的第 ' + str(index + 1) + ' 条推文处理完成')
            Util.WaitTime(wait_time)

    index += 1

print('---------------------------------------------------------------------')
print('处理完毕: 一共处理了 ' + str(all) + ' 条推文，成功发推 ' +
      str(succ) + ' 条 失败 ' + str(all - succ) + ' 条')
