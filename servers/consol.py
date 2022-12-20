import os
import hashlib
from PIL import Image


class consol:
    '''
    控制台的输出信息
    '''

    def erro(message: str):
        '''
        系统输出信息：错误信息
        '''
        print('\033[0;35;40m==\033[0;35;40m>\033[0;%d;40m %s \033[0m' %
              (31, message))

    def info(message: str):
        '''
        系统输出信息：错误信息
        '''
        print('\033[0;35;40m==\033[0;35;40m>\033[0;%d;40m %s \033[0m' %
              (33, message))

    def success(message: str):
        '''
        系统输出信息：错误信息
        '''
        print('\033[0;35;40m==\033[0;35;40m>\033[0;%d;40m %s \033[0m' %
              (32, message))
