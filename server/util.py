import os
import hashlib
import stat


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
        print('正在处理文件名: %s' % path)
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
            print('文件更改为：%s' % new_path)

        return new_path + '/' if path_list[-1] == '' else new_path
