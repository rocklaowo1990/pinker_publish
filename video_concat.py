import os
import cv2

from servers.consol import consol
from servers.ffmpeg import ffmpeg
from servers.file import file

# 找出根目录里所有的文件夹
media_files = os.listdir()

# 处理记录
historys = []

# 片头片尾路径
horizontal_start = ''
vertical_start = ''
horizontal_end = ''
vertical_end = ''

# 水印路径
water_path = ''

# 目标
targets: list[str] = []

# 输出目录
# out_path = os.path.join('', 'out')
# have_out = os.path.exists(out_path)
# if not have_out:
#     os.makedirs(out_path)

consol.log('正在查找相关文件...')

# 遍历根目录,找到下载历史
for media_file in media_files:

    # 读取下载历史数据
    if media_file == 'history.txt':
        with open(media_file) as medias_txt_open:
            for media_txt_open in medias_txt_open.readlines():
                media_txt_open = media_txt_open.strip('\n')
                historys.append(media_txt_open)
        medias_txt_open.close()

    # 读取片头的路径
    elif media_file == 'assets':
        assets_path = os.path.join('', 'assets')
        assets = os.listdir(assets_path)
        for asset in assets:
            if asset == 'logo.png':
                water_path = os.path.join(assets_path, asset)
            elif asset == 'horizontal_start.mp4':
                horizontal_start = os.path.join(assets_path, asset)
            elif asset == 'vertical_start.mp4':
                vertical_start = os.path.join(assets_path, asset)
            elif asset == 'horizontal_end.mp4':
                horizontal_end = os.path.join(assets_path, asset)
            elif asset == 'vertical_end.mp4':
                vertical_end = os.path.join(assets_path, asset)

    # 读取目标视频
    elif media_file == 'target':
        target_path = os.path.join('', 'target')
        target_media_files = os.listdir(target_path)
        # 判断文件夹的名字是否合法
        # 不合法的将进行修改
        file.check(target_media_files, target_path)
        for target_media_file in target_media_files:
            if '.mp4'.upper() in target_media_file.upper() or '.mkv'.upper(
            ) in target_media_file.upper() or '.mov'.upper(
            ) in target_media_file.upper():
                targets.append(os.path.join(target_path, target_media_file))

# 从历史记录里剔除已经处理过的视频
_index = 0
while _index < len(targets):
    if targets[_index] in historys or 'water_mpg_concat_compres' in targets[
            _index] or 'water' in targets[_index]:
        consol.err('发现已经处理过的文件：%s' % (targets[_index]))
        targets.remove(targets[_index])
    else:
        _index += 1

if horizontal_start == '' and vertical_start == '':
    consol.err('没有找到片头文件，程序退出...')
    exit()

if horizontal_end == '' and vertical_end == '':
    consol.err('没有找到片尾文件，程序退出...')
    exit()

if water_path == '':
    consol.err('没有找到水印文件，程序退出...')
    exit()

if targets == []:
    consol.err('没有找到可以处理的视频，程序退出...')
    exit()

consol.log('本次任务一共需要处理 %d 个视频' % (len(targets)))

index = 1
for target in targets:
    consol.log('正在处理第 %d 个视频' % (index))

    water_out_path = ffmpeg.water(target, water_path)
    concats = []

    capture = cv2.VideoCapture(water_out_path)
    capture_width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    capture_height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    if capture_width > capture_height:
        concats.append(
            horizontal_start if horizontal_start != '' else vertical_start)
        concats.append(water_out_path)
        concats.append(
            horizontal_end if horizontal_end != '' else vertical_end)
    else:
        concats.append(
            vertical_start if vertical_start != '' else horizontal_start)
        concats.append(water_out_path)
        concats.append(vertical_end if vertical_end != '' else horizontal_end)

    concat_temp = ffmpeg.concat(concats, 2)

    ffmpeg.compres(concat_temp)

    consol.log('写入历史记录...%s' % (target))
    with open(os.path.join('', 'history.txt'), 'a') as f:
        f.write(str(target) + '\n')
    consol.suc('第 %d 个视频处理完成' % (index))
    index += 1

    consol.log('删除文件：%s' % (concat_temp))
    os.remove(concat_temp)

    consol.log('删除文件：%s' % (water_out_path))
    os.remove(water_out_path)

consol.suc('任务全部处理完成, 程序退出...')
