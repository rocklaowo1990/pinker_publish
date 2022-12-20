import math
import os
import random
import threading
import time

import cv2
from server.timer import MyTimer
from server.util import MyUtil


class MyVideo:
    # 压缩视频文件
    def compressVideo(video_path: str, size: int = 150):
        '''
        -i 输入的视频文件 \n
        -r 每一秒的帧数,一秒 25 帧大概就是人眼的速度 \n
        -pix_fmt 设置视频颜色空间 yuv420p网络传输用的颜色空间 ffmpeg -pix_fmts可以查看有哪些颜色空间选择 \n
        -vcodec 软件编码器,libx264通用稳定 \n
        -preset 编码机预设 编码机预设越高占用CPU越大 有十个参数可选 ultrafast superfast veryfast(录制视频选用) faster fast medium(默认) slow slower veryslow(压制视频时一般选用) pacebo \n
        -profile:v 压缩比的配置 越往左边压缩的越厉害,体积越小 baseline(实时通信领域一般选用,画面损失越大) Extended Main(流媒体选用) High(超清视频) High 10 High 4:2:2 High 4:4:4(Predictive) \n
        -level:v 对编码机的规范和限制针对不通的使用场景来操作,也就是不同分辨率设置不同的值(这个我没有设置,因为这个要根据不同的分辨率进行设置的,具体要去官方文档查看) \n
        -crf 码率控制模式 用于对画面有要求,对文件大小无关紧要的场景 0-51都可以选择 0为无损 一般设置18 - 28之间 大于28画面损失严重 \n
        -acodec 设置音频编码器 \n
        -loglevel quiet 禁止输出 \n
        '''
        fileName = video_path.split('.')
        out_path = fileName[0] + '_compress.mp4'

        fpsize = os.path.getsize(video_path) / 1024 / 1024
        if fpsize >= size:  # 大于150MB的视频需要压缩
            MyUtil.consol(
                '正在压缩视频 %s : (%s)' %
                (out_path, time.strftime("%Y-%m-%d %H:%M:%S",
                                         time.localtime())), 2)
            compress = 'ffmpeg -y -i {} -r 25 -pix_fmt yuv420p -vcodec libx264 -preset slow -vf scale=-2:720 -profile:v baseline  -crf 28 -acodec aac -b:v 720k -strict -5 {}'.format(
                video_path, out_path)
            isRun = os.system(compress)
            thr = threading.Thread(target=lambda: isRun)
            thr.start()
            thr.join()
            MyUtil.consol(
                '视频压缩完成: %s (%s)' %
                (out_path, time.strftime("%Y-%m-%d %H:%M:%S",
                                         time.localtime())), 1)
            return out_path
        else:
            MyUtil.consol('视频文件大小达标,无需压缩...', 1)
            return ''

    def cutVideo(video_path: str, video_duration: int):
        '''
        -i 输入的视频文件 \n
        -r 每一秒的帧数,一秒 25 帧大概就是人眼的速度 \n
        -pix_fmt 设置视频颜色空间 yuv420p网络传输用的颜色空间 ffmpeg -pix_fmts可以查看有哪些颜色空间选择 \n
        -vcodec 软件编码器,libx264通用稳定 \n
        -preset 编码机预设 编码机预设越高占用CPU越大 有十个参数可选 ultrafast superfast veryfast(录制视频选用) faster fast medium(默认) slow slower veryslow(压制视频时一般选用) pacebo \n
        -profile:v 压缩比的配置 越往左边压缩的越厉害,体积越小 baseline(实时通信领域一般选用,画面损失越大) Extended Main(流媒体选用) High(超清视频) High 10 High 4:2:2 High 4:4:4(Predictive) \n
        -level:v 对编码机的规范和限制针对不通的使用场景来操作,也就是不同分辨率设置不同的值(这个我没有设置,因为这个要根据不同的分辨率进行设置的,具体要去官方文档查看) \n
        -crf 码率控制模式 用于对画面有要求,对文件大小无关紧要的场景 0-51都可以选择 0为无损 一般设置18 - 28之间 大于28画面损失严重 \n
        -acodec 设置音频编码器 \n
        -loglevel quiet 禁止输出 \n
        '''
        fileName = video_path.split('.')
        out_path = fileName[0] + '_compress.mp4'

        if video_duration < 60:
            print('----\033[0;33;40m视频时长太小,不支持裁切...\033[0m')
            return ''
        else:
            print('正在裁切视频 %s : (%s)' %
                  (out_path,
                   time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            compress = 'ffmpeg -y -ss {} -t {} -i {} -r 25 -pix_fmt yuv420p -vcodec libx264 -preset slow -vf scale=-2:720 -profile:v baseline  -crf 28 -acodec aac -b:v 720k -strict -5 {}'.format(
                10, video_duration - 20, video_path, out_path)
            isRun = os.system(compress)
            thr = threading.Thread(target=lambda: isRun)
            thr.start()
            thr.join()
            print('\033[0;36;40m视频裁切完成: %s (%s)\033[0m' %
                  (out_path,
                   time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            return out_path

    # 拿到视频帧图片
    def getImage(video_path: str, video_duration: int, index: int, length=3):
        '''
        参数说明: \n
        -i 输入文件,这里指的就是视频文件。 \n
        -y 表示无需询问,直接覆盖输出文件（如果有原文件的话）。 \n
        -vf 一个命令行,表示过滤图形的描述。选择过滤器select会选择帧进行输出: pict_type和对应的类型:PICT_TYPE_I 表示是I帧,即关键帧。 \n
        -frames:v 1 设置要输出的帧数,这里1个视频就设置输出1帧画面。\n
        -vsync 2 阻止每个关键帧产生多余的拷贝；\n
        -f image2 "%%~na.jpg" 将视频帧写入到图片中,视频文件名称作为图片的文件名,jpg为图格式。\n
        -s 分辨率。\n
        -loglevel quiet 禁止输出\n
        '''
        fileName = video_path.split('.')
        pics = []
        _index = index
        while _index < length:
            start_time = _index
            play_time = video_duration - start_time
            if video_duration >= 30:
                start_time = random.randint(5, video_duration - 20)
                play_time = 20
            else:
                start_time = random.randint(5, video_duration)
                play_time = video_duration - start_time

            pic = fileName[0] + '_截屏00' + str(_index + 1) + '.jpg'

            compress = 'ffmpeg -loglevel quiet -ss %d -t %d -y -i %s -pix_fmt yuvj420p -vf select="eq(pict_type\,I)" -frames:v 1 -f image2 %s' % (
                start_time, play_time, video_path, pic)
            print('即将抽取视频帧...')
            os.system(compress)
            MyTimer.waitTime(1)
            pics.append(pic)
            print('----\033[0;36;40m视频帧抽取完成: %s_截屏00%s.jpg\033[0m' %
                  (fileName[0], str(_index + 1)))
            _index += 1
        return pics

    # 拿到视频帧图片
    def getImages(video_path: str, video_duration: int, length: int):
        '''
        ### 参数说明: \n
        - i  输入文件,这里指的就是视频文件。\n
        - y 表示无需询问,直接覆盖输出文件（如果有原文件的话）。\n
        - vf 一个命令行,表示过滤图形的描述。选择过滤器select会选择帧进行输出: pict_type和对应的类型:PICT_TYPE_I 表示是I帧,即关键帧。\n
        - frames:v 1 设置要输出的帧数,这里1个视频就设置输出1帧画面。\n
        - vsync 2 阻止每个关键帧产生多余的拷贝；\n
        - f image2 "%%~na.jpg" 将视频帧写入到图片中,视频文件名称作为图片的文件名,jpg为图格式。\n
        - s 分辨率。\n
        - loglevel quiet 禁止输出\n
        '''
        fileName = video_path.split('.')
        pics = []

        for _index in range(0, length):
            start_time = _index
            play_time = video_duration - start_time

            if video_duration >= 30:
                start_time = random.randint(5, video_duration - 20)
                play_time = 20
            else:
                start_time = random.randint(5, video_duration)
                play_time = video_duration - start_time

            pic = fileName[0] + '_截屏00' + str(_index + 1) + '.jpg'

            compress = 'ffmpeg -loglevel quiet -ss %d -t %d -y -i %s -pix_fmt yuvj420p -vf select="eq(pict_type\,I)" -frames:v 1 -f image2 %s' % (
                start_time, play_time, video_path, pic)

            print('即将抽取视频帧...')
            os.system(compress)

            MyTimer.waitTime(1)
            pics.append(pic)
            print('----\033[0;36;40m视频帧抽取完成: %s_截屏00%d.jpg\033[0m' %
                  (fileName[0], _index + 1))
            _index += 1
        return pics

    # 拿到视频帧图片
    def getFirstImage(video_path: str):
        '''
        拿到视频的首帧图片\n
        '''
        fileName = video_path.split('.')
        pic = fileName[0] + '_首帧预览图.jpg'

        compress = 'ffmpeg -loglevel quiet -ss %d -t %d -y -i %s -pix_fmt yuvj420p -vf select="eq(pict_type\,I)" -frames:v 1 -f image2 %s' % (
            1, 1, pic)
        print('即将抽取视频首帧预览图...')
        os.system(compress)

        MyTimer.waitTime(1)
        print('----\033[0;36;40m视频首帧抽取完成: %s\033[0m' % pic)

        return pic

    # 添加水印
    def waterMark(video_path: str, image_path: str, out_path: str):
        '''
        -i ：一般表示输入 \n
        -filter_complex: 相比-vf, filter_complex适合开发复杂的滤镜功能，如同时对视频进行裁剪并旋转。参数之间使用逗号（，）隔开即可\n
        main_w:视频宽度\n
        main_h : 视频高度\n
        overlay_w: 要添加的图片水印宽度\n
        overlay_h:要添加的图片水印宽度\n
        overlay:水印的定位
        main_w-overlay_w-10 : 水印在x轴的位置，也可以写成x=main_w-overlay_w-10\n
        main_h-overlay_h-10：水印在y轴的位置\n
        '''

        fileName = video_path.split('/')
        fileName = fileName[-1]
        fileName = fileName.split('.')

        MyUtil.consol('即为视频添加水印：%s' % video_path, 2)

        out_name = '%s_water_mark.mp4' % os.path.join(out_path, fileName[0])

        # compress = 'ffmpeg -y -i %s -i %s -filter_complex "overlay=main_w-overlay_w-10:main_h-overlay_h-10" %s' % (
        #     video_path, image_path, out_name)
        compress = 'ffmpeg -y -i %s -i %s -filter_complex "overlay=19:64" %s' % (
            video_path, image_path, out_name)

        isRun = os.system(compress)
        thr = threading.Thread(target=lambda: isRun)
        thr.start()
        thr.join()
        MyUtil.consol('水印添加完成,储存位置：%s' % out_name, 1)
        return out_name

    # 拼接视频
    def concat(
        video_paths: list[str],
        target_path: str,
        out_path: str,
        is_horizontal: bool = True,
    ):
        MyUtil.consol(
            '即将合并视频组：%s, %s' % (video_paths, is_horizontal),
            2,
        )

        ts_paths: list[str] = []

        concat_list = 'cat'

        target_name = target_path.split('/')
        target_name = target_name[-1]
        target_name = target_name.split('.')

        for video_path in video_paths:
            MyUtil.consol('正在拆解视频：%s' % (video_path), 2)
            fileName = video_path.split('/')
            fileName = fileName[-1]
            fileName = fileName.split('.')

            ts_path = '%s.mpg' % os.path.join(out_path, fileName[0])
            ts_paths.append(ts_path)

            capture = cv2.VideoCapture(video_path)

            capture_width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
            capture_height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

            width = 0
            height = 0
            x = 0
            y = 0

            if is_horizontal:

                if capture_width > capture_height:
                    size = capture_width / 1270
                    capture_width = 1270
                    capture_height = math.ceil(capture_height / size)
                    if capture_height % 2 != 0:
                        capture_height -= 1
                else:
                    size = capture_height / 720
                    capture_height = 720
                    capture_width = math.ceil(capture_width / size)

                    if capture_width % 2 != 0:
                        capture_width -= 1

                width = 1270
                height = 720
                x = (1270 - capture_width) / 2
                y = (720 - capture_height) / 2
            else:

                if capture_width > capture_height:

                    size = capture_width / 720
                    capture_width = 720
                    capture_height = math.ceil(capture_height / size)

                    if capture_height % 2 != 0:
                        capture_height -= 1
                else:

                    print(capture_width, capture_height)

                    size = capture_height / 1270
                    print(size)

                    capture_height = 1270

                    capture_width = math.ceil(capture_width / size)

                    if capture_width % 2 != 0:
                        capture_width -= 1
                width = 720
                height = 1270
                x = (720 - capture_width) / 2
                y = (1270 - capture_height) / 2

            compress = 'ffmpeg -y -i %s -q:v 4 -vf "scale=%d:%d,pad=%d:%d:%d:%d:black" %s' % (
                video_path,
                capture_width,
                capture_height,
                width,
                height,
                x,
                y,
                ts_path,
            )
            isRun = os.system(compress)
            thr = threading.Thread(target=lambda: isRun)
            thr.start()
            thr.join()

            concat_list += ' %s' % ts_path
            MyUtil.consol('视频拆解完成：%s' % (video_path), 2)
            MyTimer.waitTime(1)

        MyUtil.consol('正在合并视频段', 2)
        concat_path = '%s.mp4' % os.path.join(out_path, target_name[0])
        compress = '%s| ffmpeg -y -f mpeg -i - -q:v 6 -vcodec mpeg4 %s' % (
            concat_list,
            concat_path,
        )

        isRun = os.system(compress)
        thr = threading.Thread(target=lambda: isRun)
        thr.start()
        thr.join()

        for ts_path in ts_paths:
            os.remove(ts_path)
        MyUtil.consol('视频拼接完成...', 1)

        return concat_path
