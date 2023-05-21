import os
import time

import cv2
from server.api import MyApi
from server.requests import MyRequests
from server.util import MyUtil
from boto3.session import Session
from boto3.s3.transfer import TransferConfig

# 下载记录
medias = []

# 找出根目录里所有的文件夹
files = os.listdir()
# 遍历根目录,找到下载历史
for file in files:
    medias_txt = ''
    # 读取下载历史数据
    if file == 'history.txt':
        with open(file) as medias_txt_open:
            for media_txt_open in medias_txt_open.readlines():
                media_txt_open = media_txt_open.strip('\n')
                medias.append(media_txt_open)
        medias_txt_open.close()

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
        '请输桶目录（0 Public 1 Media/image/org 2 Media/image/wn ) : ')

    if commpress_input == '0' or commpress_input == '':
        print('----\033[0;36;40m选择了 Public\033[0m')
        compress_pass = True
        os_path = 'public'

    elif commpress_input == '1':
        print('----\033[0;36;40m选择了 Media/image/org\033[0m')
        compress_pass = True
        commpress_type = 1
        os_path = 'media/image/org'

    elif commpress_input == '2':
        print('----\033[0;36;40m选择了 Media/image/wn\033[0m')
        compress_pass = True
        commpress_type = 2
        os_path = 'media/image/wm'

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

page_index = 1

search_key = os_path + '/'
print('正在检索 %s 里第 %d 页的图片' % (os_path, page_index))

datas = []

files = session.client('s3').list_objects_v2(
    Bucket=bucket,
    Delimiter='/',
    Prefix=search_key,
)

print('----\033[0;32;40m数据获取成功，正在载入...\033[0m')
datas.extend(files['Contents'])
print('----\033[0;32;40m载入成功\033[0m')

isResponse = False

if 'NextContinuationToken' in files:
    isResponse = True
    continuation_token = files['NextContinuationToken']
    page_index += 1
else:
    isResponse = False

while isResponse:
    print('正在检索 %s 里第 %d 页的图片' % (os_path, page_index))

    files = session.client('s3').list_objects_v2(
        Bucket=bucket,
        Delimiter='/',
        Prefix=search_key,
        ContinuationToken=continuation_token)

    print('----\033[0;32;40m数据获取成功，正在载入...\033[0m')
    datas.extend(files['Contents'])
    print('----\033[0;32;40m载入成功\033[0m')

    if 'NextContinuationToken' in files:
        continuation_token = files['NextContinuationToken']
        page_index += 1
    else:
        isResponse = False

for data in datas:
    # 如果不是图片，或者路径里没有资源，或者路径里没有的都跳过不处理
    if data['Key'] == search_key or not os_path in data['Key'] or '.mp4'.upper(
    ) in data['Key'].upper() or '.mov'.upper() in data['Key'].upper(
    ) or '.jpg'.upper() in data['Key'].upper():
        continue

    if data['Key'] in medias:
        print('----\033[0;32;40m已经处理过改文件,跳过处理...\033[0m')
        continue

    # 根据选择的目录进行下载
    path = os.path.join('', 'medias')

    have_file = os.path.exists(path)
    if not have_file:
        os.makedirs(path)

    file_name = str(data['Key']).split('/')[-1]
    path = os.path.join(path, file_name)

    url = 'https://' + bucket + '.s3.ap-southeast-1.amazonaws.com/' + data[
        'Key']

    print('正在下载文件   ' + path + '   (' +
          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ')')
    myrequeste = MyRequests.get(url)
    with open(path, 'wb') as fd:
        for chunk in myrequeste.iter_content():
            fd.write(chunk)
        fd.close()
    print('----\033[0;32;40m文件下载完成   ' + path + '   (' +
          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ')\033[0m')

    resizeImage = MyUtil.resizeImage(path)
    if resizeImage == -1:
        continue
    else:
        new_path = path + '.jpg'

    img = cv2.imread(new_path)
    cv2.imwrite(new_path, img, [cv2.IMWRITE_JPEG_QUALITY, 80])

    print('正在上传文件   ' + new_path + '   (' +
          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ')')
    MB = 1024**2
    transfer_config = TransferConfig(multipart_threshold=100 * MB,
                                     max_concurrency=64,
                                     max_io_queue=1280)

    try:
        # upload logo to s3,key_name指定S3上的路径,大于阀值分段传输
        s3.Bucket(bucket).upload_file(Filename=new_path,
                                      Key=data['Key'],
                                      ExtraArgs={'ACL': 'public-read'},
                                      Config=transfer_config)
        print('----\033[0;33;40m文件上传成功   ' + new_path + '   (' +
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ')' +
              '\033[0m')
    except Exception as e:
        print('----\033[0;37;41m上传文件出错: ' + str(e) + '\033[0m')
        print('----\033[0;37;41m文件路径: %s\033[0m' % new_path)
        continue

    with open(os.path.join('', 'history.txt'), 'a') as f:
        f.write(data['Key'] + '\n')
