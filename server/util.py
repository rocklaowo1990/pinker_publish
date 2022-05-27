import os
import hashlib
import cv2


class MyUtil:
    # 拿到文件后缀
    def getType(path: str):
        string_list = path.split('.')
        return string_list[len(string_list)-1]

    # 去除非文件夹的方法
    def getFolder(files:list[str], path: str):
        index = 0
        while index < len(files):
            print('正在检查路径是否为可用文件夹: [ %s ]' % files[index])
            if not os.path.isdir(os.path.join(path, files[index])):
                print('----\033[0;33;40m这不是一个文件夹, 从数据中移除...\033[0m')
                files.remove(files[index])
                
            elif files[index][0] == '.' or files[index][0] == '_':
                print('----\033[0;33;40m这个文件夹用不了, 从数据中移除...\033[0m')
                files.remove(files[index])
                
            elif files[index] == 'server':
                print('----\033[0;33;40mserver 是服务文件夹, 用不了, 从数据中移除...\033[0m')
                files.remove(files[index])
                
            else:
                index += 1
                print('----\033[0;32;40m可用文件夹...\033[0m')
      
    # 去除垃圾文件
    def getFile(files:list[str]):
        index = 0
        while index < len(files):
            if files[index][:1] == '.' or files[index][:1] == '_':
                files.remove(files[index])
            else:
                index += 1

    # 获取文件的M D5
    def getFileMd5(filename: str):
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

    # 检查文件路径的合法性
    # 这里真是更改字符串
    def checkName(value:str):
        print('正在检查路径名称的合法性: [ %s ]' % value)
        # 判断根目录是不是有特殊字符
        new = ''
        for i in value:
            if i.isalnum() or '\u4e00' <= i <= '\u9fa5' or i == '_' or i == '.':
                new += i
        if value == new:
            print('----\033[0;32;40m路径名称正常...\033[0m')
            return ''
        else:
            print('----\033[0;33;40m检查到路径名称不合法, 名称更改为: [ %s ]\033[0m' % new)
            return new


    # 更改文件路径
    def rename(files:list[str], path: str):
        index = 0
        for file in files:
            file_check = MyUtil.checkName(file)
            if file_check != '':
                os.rename(os.path.join(path, file), os.path.join(path, file_check))
                files[index] = file_check
            index += 1


    def checkVideo(file: str):
        print('正在检查视频文件的完整性: %s' % file)

        try:
            vid = cv2.VideoCapture(file)
            if not vid.isOpened():
                print('----\033[0;37;41m视频文件存在问题\033[0m')
                return -1
                # print('Just a Dummy Exception, write your own')
            print('----\033[0;32;40m视频文件正常\033[0m')
            return 200
        except cv2.error as e:
            print('----\033[0;37;41m视频文件存在问题: \033[0m', e)
            return -1
        except Exception as e:
            print('----\033[0;37;41m视频文件存在问题: \033[0m', e)
            return -1
        



