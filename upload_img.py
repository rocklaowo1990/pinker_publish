import os
import time

from server.api import MyApi
from boto3.session import Session
from boto3.s3.transfer import TransferConfig

# 媒体
datas = []

works_path = os.path.join('', 'works')

have_file = os.path.exists(works_path)
if not have_file:
    print('\033[0;37;41m没找到 works 文件夹，退出...\033[0m')
    exit()

# 找出根目录里所有的文件夹
files = os.listdir(path=works_path)

# 遍历根目录,找到下载历史
for file in files:
    if '.jpg' in file:
        file_path = os.path.join(works_path, file)
        datas.append(file_path)

if len(datas) <= 0:
    print('\033[0;37;41m没有发现任何可执行的任务，退出...\033[0m')
    exit()

print(datas)

environment = False
api_url = ''
while not environment:
    environment_input = input('请输入环境(0: 测试环境  1: 正式环境): ')
    if environment_input == '' or environment_input == '0':
        print('----\033[0;36;40m资源将上传到测试环境服务器\033[0m')
        api_url = 'https://api.pkappsim.xyz'
        environment = True
    elif environment_input == '1':
        print('----\033[0;36;40m资源将上传到正式环境服务器\033[0m')
        api_url = 'https://www.pkapp.buzz'
        environment = True
    else:
        print('----\033[0;37;41m环境输入错误,请重新输入\033[0m')

compress_pass = False
os_path = ''
while not compress_pass:
    commpress_input = input(
        '请输桶目录（0 Publick 1 Media/image/org 2 Media/image/wn ) : ')

    if commpress_input == '0' or commpress_input == '':
        print('----\033[0;36;40m选择了 Public\033[0m')
        compress_pass = True
        os_path = 'public/'

    elif commpress_input == '1':
        print('----\033[0;36;40m选择了 Media/image/org\033[0m')
        compress_pass = True
        commpress_type = 1
        os_path = 'media/image/org/'

    elif commpress_input == '2':
        print('----\033[0;36;40m选择了 Media/image/wn\033[0m')
        compress_pass = True
        commpress_type = 2
        os_path = 'media/image/wm/'

    else:
        print('----\033[0;37;41m是否压缩选择输入有误\033[0m')

#-------------------------------------------------------------------------------
# 读取加密设置
# aws 桶信息
# salt 信息
#-------------------------------------------------------------------------------

accessKey = ''
secretKey = ''
bucket = ''
enKey = ''
iv = ''
region = ''

get_config = MyApi.get_config(api_url)
if get_config != '':
    accessKey = get_config['accessKey']
    secretKey = get_config['secretKey']
    bucket = get_config['bucket']
    enKey = get_config['enKey']
    iv = get_config['iv']
    region = get_config['region']
else:
    print('\033[0;37;41m获取系统配置失败\033[0m')
    exit()

session = Session(aws_access_key_id=accessKey,
                  aws_secret_access_key=secretKey,
                  region_name=region)
s3 = session.resource("s3")

for data in datas:
    data_url = os_path + str(data).split('/')[-1]

    print('正在上传文件   ' + data + '   (' +
          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ')')
    MB = 1024**2
    transfer_config = TransferConfig(multipart_threshold=100 * MB,
                                     max_concurrency=64,
                                     max_io_queue=1280)
    try:
        # upload logo to s3,key_name指定S3上的路径,大于阀值分段传输
        s3.Bucket(bucket).upload_file(Filename=data,
                                      Key=data_url,
                                      ExtraArgs={'ACL': 'public-read'},
                                      Config=transfer_config)
        print('----\033[0;33;40m文件上传成功   ' + data + '   (' +
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ')' +
              '\033[0m')
    except Exception as e:
        print('----\033[0;37;41m上传文件出错: ' + str(e) + '\033[0m')
        print('----\033[0;37;41m文件路径: %s\033[0m' % data)
        continue
