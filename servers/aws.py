import time
import boto3
from boto3.session import Session
from botocore.config import Config
from boto3.s3.transfer import TransferConfig
from servers.file import file


class aws:

    # 上传文件到S3,通过打开文件后上传
    def uploadLow(file_path: str, type: str, access_key: str, secret_key: str,
                  region: str, bucket: str):
        session = Session(aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key,
                          region_name=region)

        s3 = session.resource("s3")
        upload_data = open(file_path, 'rb')
        file_md5 = file.getFileMd5(file_path)

        upload_key = ''
        if (type == 'mp4'):
            upload_key = 'media/mp4/org/' + str(file_md5) + '.' + type
        elif (type == 'png' or type == 'jpg' or type == 'jpeg'):
            upload_key = 'media/image/org/' + str(file_md5) + '.' + type

        print('正在检查文件是否存在于服务器: ' + file_path)

        files = session.client('s3').list_objects_v2(Bucket=bucket,
                                                     Delimiter='/',
                                                     Prefix=upload_key)

        if files['KeyCount'] != 0:
            print('----\033[0;33;40m文件已存在于服务器: ' + upload_key + '\033[0m')
            return '1'
        else:
            print('----\033[0;32;40m文件不存在于服务器: ' + upload_key + '\033[0m')

        print('正在上传文件...' + '(' +
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ')')
        try:
            s3.Bucket(bucket).put_object(Key=upload_key,
                                         Body=upload_data,
                                         ACL='public-read')
            print('文件上传成功...(' +
                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ')' +
                  '\033[0m')
            upload_data.close()
            return upload_key
        except Exception as e:
            print('\033[0;37;41m上传文件出错: ' + str(e) + '\033[0m')
            return '-1'

    # 路径上传
    def upload(file_path: str, type: str, access_key: str, secret_key: str,
               region: str, bucket: str):
        # 处理文件
        file_md5 = file.getFileMd5(file_path)

        upload_key = ''
        if (type == 'mp4'):
            upload_key = 'media/mp4/org/' + str(file_md5) + '.' + type
        elif (type == 'png' or type == 'jpg' or type == 'jpeg'):
            upload_key = 'media/image/org/' + str(file_md5) + '.' + type

        config = Config(s3={"use_accelerate_endpoint": True})

        # 当文件大小超过multipart_threshold属性的值时,会发生多部分传输 。
        # 如果文件大小大于TransferConfig对象中指定的阈值,以下示例将upload_file传输配置为分段传输。
        # 1GB=1024的三次方=1073741824字节
        MB = 1024**2
        transfer_config = TransferConfig(multipart_threshold=100 * MB,
                                         max_concurrency=64,
                                         max_io_queue=1280)

        # aws 信息
        s3 = boto3.resource("s3",
                            aws_access_key_id=access_key,
                            aws_secret_access_key=secret_key,
                            region_name=region)

        # 检查文件是否存在
        print('正在检查文件是否存在于服务器: ' + file_path)
        session = Session(aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key,
                          region_name=region)
        files = session.client('s3').list_objects_v2(Bucket=bucket,
                                                     Delimiter='/',
                                                     Prefix=upload_key)
        if files['KeyCount'] != 0:
            print('----\033[0;33;40m文件已存在于服务器: ' + upload_key + '\033[0m')
            return '1'
        else:
            print('----\033[0;32;40m文件不存在于服务器: ' + upload_key + '\033[0m')

        print('----\033[0;33;40m正在上传文件...' + '(' +
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
              ')\033[0m')

        try:
            # upload logo to s3,key_name指定S3上的路径,大于阀值分段传输
            s3.Bucket(bucket).upload_file(Filename=file_path,
                                          Key=upload_key,
                                          ExtraArgs={'ACL': 'public-read'},
                                          Config=transfer_config)
            print('----\033[0;33;40m文件上传成功...(' +
                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ')' +
                  '\033[0m')
            return upload_key
        except Exception as e:
            print('\033[0;37;41m上传文件出错: ' + str(e) + '\033[0m')
            return '-1'

    # 下载
    def download(file_path: str, file_name: str, access_key: str,
                 secret_key: str, region: str, bucket: str):
        # aws 信息
        s3 = boto3.client("s3",
                          aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key,
                          region_name=region)

        try:
            s3.download_file(bucket, file_name, file_path)
            print('----\033[0;33;40m文件下载成功...\033[0m')
            return 1
        except Exception as e:
            print('\033[0;37;41m文件下载出错: ' + str(e) + '\033[0m')
            return -1