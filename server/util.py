import os
import hashlib

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
            else:
                index += 1

    # 去除垃圾文件
    def fileDel(list: list):
        index = 0
        while index < len(list):
            if list[index][:1] == '.':
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