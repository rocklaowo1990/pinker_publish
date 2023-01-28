import os
import hashlib
from servers.consol import consol


class file:
    '''
    文件和文件夹处理
    '''

    # 拿到文件后缀
    def suffix(path: str):
        '''
        拿到文件的后缀
        '''
        string_list = path.split('.')
        return string_list[len(string_list) - 1]

    # 去除非文件夹的方法
    def get_folder(files: list[str], path: str):
        '''
        ### 得到文件夹的方法
        - 去除非文件夹
        '''
        index = 0
        while index < len(files):
            consol.log('正在检查路径是否为可用文件夹: [ %s ]' % files[index])
            if not os.path.isdir(os.path.join(path, files[index])):
                consol.err('这不是一个文件夹, 从数据中移除...')
                files.remove(files[index])

            elif files[index][0] == '.' or files[index][0] == '_':
                consol.err('这个文件夹用不了, 从数据中移除...')
                files.remove(files[index])

            elif files[index] == 'server':
                consol.err('server 是服务文件夹, 用不了, 从数据中移除...')
                files.remove(files[index])
            else:
                index += 1
                consol.suc('用文件夹....')

    # 去除垃圾文件
    def del_illegal(files: list[str]):
        '''
        去除非法文件
        '''
        index = 0
        while index < len(files):
            if files[index][:1] == '.' or files[index][:1] == '_':
                files.remove(files[index])
            else:
                index += 1

    # 获取文件的M D5
    def md5(file_name: str):
        '''
        获取文件的MD5
        '''
        if not os.path.isfile(file_name):
            return
        myhash = hashlib.md5()
        f = open(file_name, 'rb')
        while True:
            b = f.read(8096)
            if not b:
                break
            myhash.update(b)
        f.close()
        return myhash.hexdigest()

    # 更改文件路径
    def check(files: list[str], path: str):
        index = 0
        for file in files:
            # 判断根目录是不是有特殊字符
            new = ''
            for i in file:
                if i.isalnum(
                ) or '\u4e00' <= i <= '\u9fa5' or i == '_' or i == '.':
                    new += i
                elif i == ' ':
                    new += '_'
            if file == new:
                consol.suc('路径名称正常...')
            else:
                consol.err('检查到路径名称不合法, 名称更改为: [ %s ]\033[0m' % new)
                os.rename(os.path.join(path, file), os.path.join(path, new))
                files[index] = new
            index += 1
