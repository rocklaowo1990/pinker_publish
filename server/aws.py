from server.util import Util
from boto3.session import Session


class Aws:
    # 上传文件到S3
    def upload(api_url:str, file_path: str, type: str, access_key:str, secret_key:str, region:str, bucket:str):
        '''
        上传文件到 aws 的 s3 桶
        '''
        session = Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)
        s3 = session.resource("s3")
        upload_data = open(file_path, 'rb')
        file_md5 = Util.getFileMd5(file_path)
        upload_key = str(file_md5) + '.' + type

        print('正在检查文件是否存在: ' + file_path)
        files = session.client('s3').list_objects_v2(
            Bucket=bucket,
            Delimiter='/',
            Prefix='public/' + upload_key
        )

        if files['KeyCount'] != 0:
            print('文件已存在: ' + 'public/' + upload_key)
            return '1'

        print('正在上传文件：' + file_path)
        try:
            s3.Bucket(bucket).put_object(
                Key='public/' + upload_key, Body=upload_data, ACL='public-read-write')
        except Exception as e:
            print('上传文件出错：' + str(e))
            return '-1'

        print('文件上传成功: public/' + upload_key)
        return 'public/' + upload_key