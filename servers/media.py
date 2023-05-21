import cv2
from PIL import Image

from servers.consol import consol


class media:

    def isVideo(path: str):
        '''
        检查视频文件是否完整
        True: 说明完整
        False: 不完整
        '''
        consol.log('正在检查视频文件的完整性: %s' % path)
        try:
            vid = cv2.VideoCapture(path)
            if not vid.isOpened():
                consol.err('视频文件存在问题')
                return False
            consol.suc('视频文件正常')
            return True
        except cv2.error as e:
            consol.err('视频文件存在问题: %s', e)
            return False
        except Exception as e:
            consol.err('视频文件存在问题: %s', e)
            return False

    # 检查图片是否损坏
    def isImage(path: str):
        consol.log('正在检查图片文件的完整性: %s' % path)

        try:
            Image.open(path).load()
            consol.suc('图片文件正常')
            return True

        except OSError:
            consol.err('图片文件存在问题')
            return False

    def resizeImage(path: str):
        """修改图片尺寸       
        :param infile: 图片源文件       
        :param outfile: 重设尺寸文件保存地址       
        :param x_s: 设置的宽度       
        :return:    
        """
        isImage = media.isImage(path)
        if not isImage:
            return False

        im = Image.open(path)
        x, y = im.size

        if x > y:
            if x >= 1280:
                x_s = 1280
            else:
                x_s = x
        else:
            if x >= 720:
                x_s = 720
            else:
                x_s = x

        y_s = int(y * x_s / x)

        out = im.convert('RGB')
        out.save(path + '.jpg')

        if x >= 720:
            im = Image.open(path + '.jpg')
            out = im.resize((x_s, y_s), Image.ANTIALIAS)
            out.save(path + '.jpg')

        return True
