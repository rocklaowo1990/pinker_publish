import os
import hashlib
import re
import stat

import cv2
import numpy as np


class Util:
    # 拿到文件后缀
    def getType(path: str):
        string_list = path.split('.')
        return string_list[len(string_list)-1]

    # 去除非文件夹的方法
    def dirDel(list: list, path: str):
        index = 0
        while index < len(list):
            if not os.path.isdir(path+list[index]):
                list.remove(list[index])
            elif list[index][0] == '.' or list[index][0] == '_':
                list.remove(list[index])
            elif list[index] == 'server':
                list.remove(list[index])
            else:
                index += 1

    # 去除垃圾文件
    def fileDel(list: list):
        index = 0
        while index < len(list):
            if list[index][:1] == '.' or list[index][:1] == '_':
                list.remove(list[index])
            elif list[index] == '':
                list.remove(list[index])
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

    def rename(path: str):
        # print('正在检查路径是否合法: %s' % path)
        # 用 / 把地址分割成小块进行处理
        path_list = path.split('/')
        old_path = ''
        new_path = ''
        index = 1
        isChanged = False
        while index < len(path_list):
            old_path += '/' + \
                path_list[index] if path_list[index] != '' else ''

            path_item = ''
            for i in path_list[index]:
                if i.isalnum() or '\u4e00' <= i <= '\u9fa5' or i == '_' or i == '.':
                    path_item += i

            new_path += '/' + path_item if path_list[index] != '' else ''

            if new_path != old_path:
                os.rename(old_path, new_path)
                isChanged = True

            old_path = new_path
            index += 1

        if isChanged:
            print('\033[0;33;40m检查到路径不合法,更改为: %s\033[0m' % new_path)
        # else:
        #     print('\033[0;32m路径合法\033[0m')


        return new_path + '/' if path_list[-1] == '' else new_path

    def checkVideo(file: str):
        print('--------正在检查视频文件的完整性: %s' % file)

        try:
            vid = cv2.VideoCapture(file)
            if not vid.isOpened():
                print('\033[0;37;41m视频文件存在问题\033[0m')
                return -1
                # print('Just a Dummy Exception, write your own')
            print('--------\033[0;32;40m视频文件没有问题\033[0m')
            return 200
        except cv2.error as e:
            print('--------\033[0;37;41m视频文件存在问题: \033[0m', e)
            return -1
        except Exception as e:
            print('--------\033[0;37;41m视频文件存在问题: \033[0m', e)
            return -1
        



