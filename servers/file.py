import json
import os
import hashlib


class file:
    '''
    文件和文件夹处理
    '''
    # 判断文件夹是否存在
    def isHave(path:str, isMake:bool = False):
        have_file = os.path.exists(path)
        if not have_file and isMake:
            os.makedirs(path)
        return have_file

    # 拿到文件后缀
    def suffix(path: str):
        '''
        拿到文件的后缀
        '''
        string_list = path.split('.')
        return string_list[len(string_list) - 1]

    # 去除非文件夹的方法
    def getFolder(files: list[str], path: str):
        '''
        ### 得到文件夹的方法
        - 去除非文件夹
        '''
        index = 0
        while index < len(files):
            if not os.path.isdir(os.path.join(path, files[index])):
                files.remove(files[index])

            elif files[index][0] == '.' or files[index][0] == '_':
                files.remove(files[index])

            elif files[index] == 'server':
                files.remove(files[index])
            else:
                index += 1

    # 去除垃圾文件
    def clear(files: list[str]):
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
            if file != new:
                os.rename(os.path.join(path, file), os.path.join(path, new))
                files[index] = new
            index += 1

    def write(path:str, content:str, type:str='a+'):
        '''
        ## 文件的写入方法
        ### type:
        + 'a' 在文件的末尾追加写入
        + 'r' 读取模式（默认值）
        + 'w' 写入模式
        + 'x' 独占写入模式
        + 'a' 附加模式
        + 'b' 二进制模式（与其他模式结合使用）
        + 't' 文本模式（默认值，与其他模式结合使用）
        + '+' 读写模式（与其他模式结合使用）
        '''
        with open(path, type,newline='\n',encoding='utf-8') as f:
            f.write('%s\n' % (content))
        f.close()

    def read(path:str):
        with open(path) as f:
            content_info = json.loads(f.read().strip())
        f.close()
        return content_info
