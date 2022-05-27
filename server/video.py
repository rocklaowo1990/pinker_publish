import os
import random
import threading
import time

from server.timer import MyTimer


class MyVideo:
    # 压缩视频文件
    def compressVideo(video_path: str):
        '''
        -i 输入的视频文件
        -r 每一秒的帧数,一秒 25 帧大概就是人眼的速度
        -pix_fmt 设置视频颜色空间 yuv420p网络传输用的颜色空间 ffmpeg -pix_fmts可以查看有哪些颜色空间选择
        -vcodec 软件编码器,libx264通用稳定
        -preset 编码机预设 编码机预设越高占用CPU越大 有十个参数可选 ultrafast superfast veryfast(录制视频选用) faster fast medium(默认) slow slower veryslow(压制视频时一般选用) pacebo
        -profile:v 压缩比的配置 越往左边压缩的越厉害,体积越小 baseline(实时通信领域一般选用,画面损失越大) Extended Main(流媒体选用) High(超清视频) High 10 High 4:2:2 High 4:4:4(Predictive)
        -level:v 对编码机的规范和限制针对不通的使用场景来操作,也就是不同分辨率设置不同的值(这个我没有设置,因为这个要根据不同的分辨率进行设置的,具体要去官方文档查看)
        -crf 码率控制模式 用于对画面有要求,对文件大小无关紧要的场景 0-51都可以选择 0为无损 一般设置18 - 28之间 大于28画面损失严重
        -acodec 设置音频编码器
        -loglevel quiet 禁止输出
        '''
        fileName = video_path.split('.')
        out_path = fileName[0] + '_compress.mp4'
       
        fpsize = os.path.getsize(video_path) / 1024 / 1024
        if fpsize >= 150.0:  # 大于150MB的视频需要压缩
            print('正在压缩视频 %s : (%s)' % (out_path, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            compress = 'ffmpeg -y -i {} -r 25 -pix_fmt yuv420p -vcodec libx264 -preset slow -vf scale=-2:720 -profile:v baseline  -crf 28 -acodec aac -b:v 720k -strict -5 {}'.format(
                video_path, out_path)
            isRun = os.system(compress)
            thr = threading.Thread(target = isRun)
            thr.start()
            thr.join()
            print('\033[0;36;40m视频压缩完成: %s (%s)\033[0m' % (out_path, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            return out_path
        else:
            print('----\033[0;33;40m视频文件大小达标,无需压缩...\033[0m')
            return ''

    def cutVideo(video_path: str, video_duration: int):
        '''
        -i 输入的视频文件
        -r 每一秒的帧数,一秒 25 帧大概就是人眼的速度
        -pix_fmt 设置视频颜色空间 yuv420p网络传输用的颜色空间 ffmpeg -pix_fmts可以查看有哪些颜色空间选择
        -vcodec 软件编码器,libx264通用稳定
        -preset 编码机预设 编码机预设越高占用CPU越大 有十个参数可选 ultrafast superfast veryfast(录制视频选用) faster fast medium(默认) slow slower veryslow(压制视频时一般选用) pacebo
        -profile:v 压缩比的配置 越往左边压缩的越厉害,体积越小 baseline(实时通信领域一般选用,画面损失越大) Extended Main(流媒体选用) High(超清视频) High 10 High 4:2:2 High 4:4:4(Predictive)
        -level:v 对编码机的规范和限制针对不通的使用场景来操作,也就是不同分辨率设置不同的值(这个我没有设置,因为这个要根据不同的分辨率进行设置的,具体要去官方文档查看)
        -crf 码率控制模式 用于对画面有要求,对文件大小无关紧要的场景 0-51都可以选择 0为无损 一般设置18 - 28之间 大于28画面损失严重
        -acodec 设置音频编码器
        -loglevel quiet 禁止输出
        '''
        fileName = video_path.split('.')
        out_path = fileName[0] + '_compress.mp4'

        if video_duration < 60:
            print('----\033[0;33;40m视频时长太小,不支持裁切...\033[0m')
            return ''
        else:
            print('正在裁切视频 %s : (%s)' % (out_path, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            compress = 'ffmpeg -y -ss {} -t {} -i {} -r 25 -pix_fmt yuv420p -vcodec libx264 -preset slow -vf scale=-2:720 -profile:v baseline  -crf 28 -acodec aac -b:v 720k -strict -5 {}'.format(
                10, video_duration - 20, video_path, out_path)
            isRun = os.system(compress)
            thr = threading.Thread(target = isRun)
            thr.start()
            thr.join()
            print('\033[0;36;40m视频裁切完成: %s (%s)\033[0m' % (out_path, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            return out_path
       
    

    # 拿到视频帧图片
    def getImage(video_path: str, video_duration: int, index:int):
        '''
        参数说明: 
        -i 输入文件,这里指的就是视频文件。
        -y 表示无需询问,直接覆盖输出文件（如果有原文件的话）。
        -vf 一个命令行,表示过滤图形的描述。选择过滤器select会选择帧进行输出: pict_type和对应的类型:PICT_TYPE_I 表示是I帧,即关键帧。
        -frames:v 1 设置要输出的帧数,这里1个视频就设置输出1帧画面。
        -vsync 2 阻止每个关键帧产生多余的拷贝；
        -f image2 "%%~na.jpg" 将视频帧写入到图片中,视频文件名称作为图片的文件名,jpg为图格式。
        -s 分辨率。
        -loglevel quiet 禁止输出
        '''
        fileName = video_path.split('.')
        pics = []
        _index = index
        while _index < 3:
            start_time = _index
            play_time = video_duration - start_time
            if video_duration >= 30:
                start_time = random.randint(5, video_duration - 20)
                play_time = 20
            else:
                start_time = random.randint(5, video_duration)
                play_time = video_duration - start_time
            compress = 'ffmpeg -loglevel quiet -ss %d -t %d -y -i %s -pix_fmt yuvj420p -vf select="eq(pict_type\,I)" -frames:v 1 -f image2 %s' % (
              start_time, play_time, video_path, fileName[0] + '_截屏00' + str(_index + 1) + '.png')
            print('即将抽取视频帧...')
            MyTimer.waitTime(1)
            os.system(compress)
            pics.append(fileName[0] + '_截屏00' + str(_index + 1) + '.png')
            print('----\033[0;36;40m视频帧抽取完成: %s_截屏00%s.png\033[0m' % (fileName[0], str(_index + 1)))
            _index += 1
        return pics