import math
import os
import platform
import threading
import time
import cv2

from servers.consol import consol
from servers.timer import timer


class ffmpeg:
    '''
    视频处理：ffmpeg
    '''

    # 压缩视频文件
    def compres(video_path: str):
        '''
        - -i 输入的视频文件 
        - -r 每一秒的帧数,一秒 25 帧大概就是人眼的速度 
        - -pix_fmt 设置视频颜色空间 yuv420p网络传输用的颜色空间 ffmpeg -pix_fmts可以查看有哪些颜色空间选择 
        - -vcodec 软件编码器,libx264通用稳定 
        - -preset 编码机预设 编码机预设越高占用CPU越大 有十个参数可选 ultrafast superfast veryfast(录制视频选用) faster fast medium(默认) slow slower veryslow(压制视频时一般选用) pacebo 
        - -profile:v 压缩比的配置 越往左边压缩的越厉害,体积越小 baseline(实时通信领域一般选用,画面损失越大) Extended Main(流媒体选用) High(超清视频) High 10 High 4:2:2 High 4:4:4(Predictive) 
        - -level:v 对编码机的规范和限制针对不通的使用场景来操作,也就是不同分辨率设置不同的值(这个我没有设置,因为这个要根据不同的分辨率进行设置的,具体要去官方文档查看) 
        - -crf 码率控制模式 用于对画面有要求,对文件大小无关紧要的场景 0-51都可以选择 0为无损 一般设置18 - 28之间 大于28画面损失严重 
        - -acodec 设置音频编码器 
        - -loglevel quiet 禁止输出 
        '''

        # 给文件重新命名
        _out_path = video_path.split('.')[0] + '_compres.mp4'

        # file_size = os.path.getsize(video_path) / 1024 / 1024

        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        consol.log('正在压缩视频 %s : (%s)' % (video_path, time_now))
        compres = 'ffmpeg -y -i {} -r 25 -pix_fmt yuv420p -vcodec libx264 -preset slow -vf scale=-2:720 -profile:v baseline  -crf 28 -acodec aac -b:v 720k -strict -5 {}'.format(
            video_path, _out_path)
        is_run = os.system(compres)
        thr = threading.Thread(target=lambda: is_run)
        thr.start()
        thr.join()
        consol.suc('视频压缩完成: %s (%s)' % (_out_path, time_now))
        return _out_path

    # 添加水印
    def water(video_path: str, water_path: str):
        '''
        -i ：一般表示输入 
        -filter_complex: 相比-vf, filter_complex适合开发复杂的滤镜功能，如同时对视频进行裁剪并旋转。参数之间使用逗号（，）隔开即可
        main_w:视频宽度
        main_h : 视频高度
        overlay_w: 要添加的图片水印宽度
        overlay_h:要添加的图片水印宽度
        overlay:水印的定位
        main_w-overlay_w-10 : 水印在x轴的位置，也可以写成x=main_w-overlay_w-10
        main_h-overlay_h-10：水印在y轴的位置
        scale=176:144：水印的大小
        '''
        consol.log('正在为视频添加水印：%s' % video_path)

        capture = cv2.VideoCapture(video_path)
        capture_width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        capture_height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

        water_width = 83
        water_height = 94

        x = 0
        y = 0

        if capture_width >= capture_height:
            water_width = 83 * capture_width / 1270
            x = 20 * capture_width / 1270

        else:
            water_width = 83 * capture_width / 720
            x = 20 * capture_width / 720

        water_height = 94 * water_width / 83
        y = x

        video_names = video_path.split('.')
        _out_path = '%s_water.mp4' % video_names[0]

        # compres = 'ffmpeg -y -i %s -i %s -filter_complex "overlay=main_w-overlay_w-10:main_h-overlay_h-10" %s' % (
        #     video_path, image_path, out_name)
        compres = 'ffmpeg -y -i %s -i %s -filter_complex "[1:v] scale=%d:%d [logo];[0:v][logo]overlay=x=%d:y=%d"  %s' % (
            video_path, water_path, water_width, water_height, x, y,
            _out_path)

        isRun = os.system(compres)
        thr = threading.Thread(target=lambda: isRun)
        thr.start()
        thr.join()

        consol.suc('水印添加完成,储存位置：%s' % _out_path)
        return _out_path

    # 拼接视频
    def concat(
        video_path_list: list[str],
        main_video: int = 2,
    ):
        '''
        - 将多个视频拼接
        - video_path_list: 视频地址的集合
        - main_video: 主视频的位置, 第1个就传1
        '''
        is_horizontal = True

        _capture = cv2.VideoCapture(video_path_list[main_video - 1])
        _capture_width = _capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        _capture_height = _capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

        is_horizontal = True if _capture_width > _capture_height else False

        consol.log('即将合并视频组：%s, 是否横版：%s' % (video_path_list, is_horizontal))

        mpg_paths: list[str] = []

        is_windows = platform.system().lower() == 'windows'
        concat_list = 'type' if is_windows else 'cat'

        _out_path = ''

        index = 0

        for video_path in video_path_list:
            index += 1
            consol.log('正在拆解第 %d 个视频：%s' % (index, video_path))

            video_names = video_path.split('.')

            _mpg_path = '%s_mpg.mpg' % video_names[0]
            mpg_paths.append(_mpg_path)

            if main_video == index:
                _out_path = _mpg_path

            capture = cv2.VideoCapture(video_path)
            capture_width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
            capture_height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

            width = 0
            height = 0
            x = 0
            y = 0

            if is_horizontal:
                if capture_width / capture_height > 1270 / 720:
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
                if capture_width / capture_height > 720 / 1270:
                    size = capture_width / 720
                    capture_width = 720
                    capture_height = math.ceil(capture_height / size)
                    if capture_height % 2 != 0:
                        capture_height -= 1
                else:
                    size = capture_height / 1270
                    capture_height = 1270
                    capture_width = math.ceil(capture_width / size)
                    if capture_width % 2 != 0:
                        capture_width -= 1
                width = 720
                height = 1270
                x = (720 - capture_width) / 2
                y = (1270 - capture_height) / 2

            print(capture_width, capture_height, x, y)
            compres = 'ffmpeg -y -i %s -q:v 4 -vf "scale=%d:%d,pad=%d:%d:%d:%d:black" %s' % (
                video_path,
                capture_width,
                capture_height,
                width,
                height,
                x,
                y,
                _mpg_path,
            )
            isRun = os.system(compres)
            thr = threading.Thread(target=lambda: isRun)
            thr.start()
            thr.join()

            concat_list += ' %s' % _mpg_path
            consol.suc('视频拆解完成：%s' % (video_path))
            timer.wait(1)

        consol.log('正在合并视频段')
        _out_path = '%s_concat.mp4' % _out_path.split('.')[0]

        compres = '%s| ffmpeg -y -f mpeg -i - -q:v 6 -vcodec mpeg4 %s' % (
            concat_list,
            _out_path,
        )

        isRun = os.system(compres)
        thr = threading.Thread(target=lambda: isRun)
        thr.start()
        thr.join()

        for ts_path in mpg_paths:
            os.remove(ts_path)

        consol.suc('视频拼接完成...')
        return _out_path
