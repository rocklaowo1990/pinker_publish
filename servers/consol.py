class consol:
    '''
    控制台的输出信息
    '''

    def err(message: str):
        '''
        系统输出信息：错误信息
        '''
        print('\033[0;35;40m==\033[0;35;40m>\033[0;%d;40m %s\033[40m' %
              (31, message))

    def log(message: str):
        '''
        系统输出信息：普通输出日志
        '''
        print('\033[0;35;40m==\033[0;35;40m>\033[0;%d;40m %s\033[40m' %
              (33, message))

    def suc(message: str):
        '''
        系统输出信息：成功信息的输出
        '''
        print('\033[0;35;40m==\033[0;35;40m>\033[0;%d;40m %s\033[40m' %
              (32, message))
