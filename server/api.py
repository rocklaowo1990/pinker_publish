import json
import requests
import hashlib
import json
from server.aes import MyAes
from server.timer import MyTimer


class MyApi:
    # 获取平台配置
    def get_config(api_url: str):
        data = {}
        url = '/api/common/config'
        headers = {
            'Content-Type': 'application/json',
        }
        print('正在获取平台设置...')
        res_suss = 0
        while res_suss < 3:
            try:
                res = requests.get(api_url + url, headers=headers)
                res_json = res.json()
                res_suss = 3
            except requests.exceptions.RequestException:
                res_suss += 1
                print('----连接失败,3秒后重连')
                MyTimer.waitTime(3)

        data['enKey'] = 'pinker.' + res_json['data']['encryptConfig']['enKey']
        data['iv'] = 'pinker.' + res_json['data']['encryptConfig']['iv']
        accessKey = MyAes.decrypt(data['enKey'],
                                  res_json['data']['awsConfig']['accessKey'],
                                  data['iv'])
        data['accessKey'] = accessKey
        region = MyAes.decrypt(data['enKey'],
                               res_json['data']['awsConfig']['region'],
                               data['iv'])
        data['region'] = region
        secretKey = MyAes.decrypt(data['enKey'],
                                  res_json['data']['awsConfig']['secretKey'],
                                  data['iv'])
        data['secretKey'] = secretKey
        bucket = MyAes.decrypt(data['enKey'],
                               res_json['data']['awsConfig']['bucket'],
                               data['iv'])
        data['bucket'] = bucket
        if res.status_code == 200:
            if res_json['code'] == 200:
                print('----\033[0;32;40m平台信息获取成功\033[0m')
                return data
            else:
                print('----\033[0;37;41m0m获取平台设置失败: %s\033[0m' %
                      res_json['msg'])
                return ''
        else:
            print('----\033[0;37;41m0m获取平台设置失败: ' + res.status_code +
                  '\033[0m')
            return ''

    def getContentListServer(server_url: str, token: str, pageSize: int,
                             pageNo: int):
        url = '/webapi/content/contentList'
        headers = {'Content-Type': 'application/json', 'token': token}

        params = {}
        params['pageSize'] = pageSize
        params['pageNo'] = pageNo

        print('正在获取推文列表...')

        res_suss = 0
        while res_suss < 3:
            try:
                res = requests.get(server_url + url,
                                   headers=headers,
                                   params=params)
                res_json = res.json()
                res_suss = 3
            except requests.exceptions.RequestException:
                res_suss += 1
                print('----连接失败,3秒后重连')
                MyTimer.waitTime(3)

        if res.status_code == 200 and res_json['code'] == 200:
            print('----\033[0;32;40m获取推文列表成功\033[0m')
            return res_json
        else:
            print('----\033[0;37;41m获取推文列表失败\033[0m')
            return -1

    # 登录接口
    def login(api_url: str, account: str, password: str, en_key: str):
        _password = password + en_key
        url = '/api/account/login'
        md5 = hashlib.md5()
        md5.update(_password.encode(encoding='utf-8'))
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'account': account,
            'password': md5.hexdigest(),
            'accountType': 1 if str(account).isdigit() else 2,
        }
        print('正在登录: ' + account)
        res_suss = 0
        while res_suss < 3:
            try:
                res = requests.post(api_url + url, data=data, headers=headers)
                res_json = res.json()
                res_suss = 3
            except requests.exceptions.RequestException:
                res_suss += 1
                print('----连接失败,3秒后重连')
                MyTimer.waitTime(3)

        if res.status_code == 200:
            if res_json['code'] == 200:
                print('----\033[0;32;40m登录成功\033[0m')
                return str(res_json['data']['token'])
            else:
                print('----\033[0;37;41m登录失败: ' + res_json['msg'] + 'c')
                return '-1'
        else:
            print('----\033[0;37;41m登录失败  code: ' + res.status_code +
                  '  错误信息: ' + res.text + '\033[0m')
            return ''

    # 后台登录接口
    def loginServer(server_url: str, account: str, password: str):
        url = '/webapi/account/login'
        headers = {'Content-Type': 'application/json', 'browser': 'Chrome'}
        data = json.dumps({'account': account, 'password': password})
        print('正在登录后台账号: ' + account)

        res_suss = 0
        while res_suss < 3:
            try:
                res = requests.post(server_url + url,
                                    data=data,
                                    headers=headers)
                res_json = res.json()
                res_suss = 3
            except requests.exceptions.RequestException:
                res_suss += 1
                print('----连接失败,3秒后重连')
                MyTimer.waitTime(3)

        if res.status_code == 200:
            if res_json['code'] == 200:
                print('----\033[0;32;40m后台账号: ' + account + '登录成功\033[0m')
                return str(res_json['data']['token'])
            else:
                print('----\033[0;37;41m后台账号 ' + account + ' 登录失败 ' +
                      res_json['msg'] + '\033[0m')
                return '-1'
        else:
            print('----\033[0;37;41m后台账号: ' + account + ' 登录失败 ---- code: ' +
                  res.status_code + ' ---- 错误信息: ' + res.text + '\033[0m')
            return ''

    # 获取分组信息
    def myGroupList(api_url: str, token: str, account: str):
        url = '/api/subscribeGroup/myGroupList'
        headers = {'Content-Type': 'application/json', 'token': token}
        print('正在获取用户 %s 订阅组信息: ' % account)

        res_suss = 0
        while res_suss < 3:
            try:
                res = requests.get(api_url + url, headers=headers)
                res_json = res.json()
                res_suss = 3
            except requests.exceptions.RequestException:
                res_suss += 1
                print('----连接失败,3秒后重连')
                MyTimer.waitTime(3)

        if res.status_code == 200:
            if res_json['code'] == 200:
                print('----\033[0;32;40m订阅组信息获取成功\033[0m')
                return res_json['data']['list']
            elif res_json['code'] == 1:
                print('----\033[0;33;40m用户 %s 的 token 过期,正在重新登录\033[0m' %
                      account)
                return 1
            else:
                print('----\033[0;37;41m订阅组信息获取失败: %s\033[0m' %
                      res_json['msg'])
                return []
        else:
            print('----\033[0;37;41m订阅组信息获取失败  code: %s  错误信息: %s\033[0m' %
                  (res.text, res.status_code))
            return []

    # 发推接口
    def publish(api_url: str, token: str, data: dict, account: str):
        url = '/api/content/publish'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'token': token
        }
        print('正在发布推文...')

        res_suss = 0
        while res_suss < 3:
            try:
                res = requests.post(api_url + url, headers=headers, data=data)
                res_json = res.json()
                res_suss = 3
            except requests.exceptions.RequestException:
                res_suss += 1
                print('----连接失败,3秒后重连')
                MyTimer.waitTime(3)

        if res.status_code == 200:
            if res_json['code'] == 200:
                print('----\033[0;32;40m推文发布成功\033[0m')
                return 200
            elif res_json['code'] == 1:
                print('----\033[0;33;40m用户 %s 的 token 过期,正在重新登录\033[0m' %
                      account)
                return 1
            else:
                print('----\033[0;37;41m推文发布失败 %s\033[0m' % res_json['msg'])
                return -1
        else:
            print('----\033[0;37;41m推文发布失败  code: %s  错误信息: %s\033[0m' %
                  (res.text, res.status_code))
            return -1

    # 作品列表
    def getContentList(api_url: str, token: str, pageNo: int, pageSize: int):
        url = '/api/content/userHomeContentList'
        headers = {'Content-Type': 'application/json', 'token': token}

        print('正在获取推文列表的第 %d 页...' % pageNo)

        data = {}
        data['pageNo'] = pageNo
        data['pageSize'] = pageSize
        data['type'] = 1

        res_suss = 0
        while res_suss < 3:
            try:
                res = requests.get(api_url + url, headers=headers, params=data)
                res_json = res.json()
                res_suss = 3
            except requests.exceptions.RequestException:
                res_suss += 1
                print('----连接失败,3秒后重连')
                MyTimer.waitTime(3)

        return_data = []

        if res.status_code == 200:
            if res_json['code'] == 200:
                print('----\033[0;32;40m获取推文列表成功\033[0m')
                return_data = res_json['data']['list']
                return return_data
            else:
                print('----\033[0;37;41m获取推文列表失败 %s\033[0m' % res_json['msg'])
                return return_data
        else:
            print('----\033[0;37;41m获取推文列表失败  code: %s  错误信息: %s\033[0m' %
                  (res.text, res.status_code))
            return return_data

    # 作品列表
    def getContentSize(api_url: str, token: str):
        url = '/api/content/userHomeContentList'
        headers = {'Content-Type': 'application/json', 'token': token}
        print('正在获取推文的数量...')

        data = {}
        data['pageNo'] = 1
        data['pageSize'] = 1
        data['type'] = 1

        res_suss = 0
        while res_suss < 3:
            try:
                res = requests.get(api_url + url, headers=headers, params=data)
                res_json = res.json()
                res_suss = 3
            except requests.exceptions.RequestException:
                res_suss += 1
                print('----连接失败,3秒后重连')
                MyTimer.waitTime(3)

        return_data = 0

        if res.status_code == 200:
            if res_json['code'] == 200:
                print('----\033[0;32;40m获取推文的数量成功\033[0m')
                print('----\033[0;32;40m推文的数量: %s \033[0m' %
                      res_json['data']['totalSize'])
                return_data = res_json['data']['totalSize']
                return return_data
            else:
                print('----\033[0;37;41m获取推文的数量失败 %s\033[0m' % res_json['msg'])
                return return_data
        else:
            print('----\033[0;37;41m获取推文的数量失败  code: %s  错误信息: %s\033[0m' %
                  (res.text, res.status_code))
            return return_data

    def contentDelForServer(server_url: str, token: str, wids: str):
        url = '/webapi/content/contentDel'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'token': token
        }
        print('正在删除推文...')

        data = {}
        data['wids'] = wids

        res_suss = 0
        while res_suss < 3:
            try:
                res = requests.delete(server_url + url,
                                      headers=headers,
                                      params=data)
                res_json = res.json()
                res_suss = 3
            except requests.exceptions.RequestException:
                res_suss += 1
                print('----连接失败,3秒后重连')
                MyTimer.waitTime(3)

        if res.status_code == 200:
            if res_json['code'] == 200:
                print('----\033[0;32;40m推文删除成功\033[0m')
                return 200
            else:
                print('----\033[0;37;41m推文删除失败 %s\033[0m' % res_json['msg'])
                return -1
        else:
            print('----\033[0;37;41m推文删除失败  code: %s  错误信息: %s\033[0m' %
                  (res.text, res.status_code))
            return -1

    # 作品列表
    def contentDel(api_url: str, token: str, wid: int):
        url = '/api/content/contentDel'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'token': token
        }
        print('正在删除推文...')

        data = {}
        data['wid'] = wid

        res_suss = 0
        while res_suss < 3:
            try:
                res = requests.post(api_url + url, headers=headers, data=data)
                res_json = res.json()
                res_suss = 3
            except requests.exceptions.RequestException:
                res_suss += 1
                print('----连接失败,3秒后重连')
                MyTimer.waitTime(3)

        if res.status_code == 200:
            if res_json['code'] == 200:
                print('----\033[0;32;40m推文删除成功\033[0m')
                return 200
            else:
                print('----\033[0;37;41m推文删除失败 %s\033[0m' % res_json['msg'])
                return -1
        else:
            print('----\033[0;37;41m推文删除失败  code: %s  错误信息: %s\033[0m' %
                  (res.text, res.status_code))
            return -1

    # 检查账号是否重复
    def checkAccount(api_url: str, account: str):
        url = '/api/account/verificateAccount'
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            'account': account,
        }
        print('正在验证账号 %s 是否已经存在...' % account)

        res_suss = 0
        while res_suss < 3:
            try:
                res = requests.get(api_url + url, headers=headers, params=data)
                res_json = res.json()
                res_suss = 3
            except requests.exceptions.RequestException:
                res_suss += 1
                print('----连接失败,3秒后重连')
                MyTimer.waitTime(3)

        if res.status_code == 200:
            if res_json['code'] == -1:
                print('----\033[0;32;40m账号 %s 可以注册 %s\033[0m' %
                      (account, res_json['msg']))
                return 200
            else:
                print('----\033[0;37;41m账号 %s 已经存在,或者出现了其他错误,错误代码: %d\033[0m' %
                      (account, res_json['code']))
                return -1
        else:
            print(
                '----\033[0;37;41m检测账号 %s 时与服务器连接失败 ---- code: %d ---- 错误信息: %s\033[0m'
                % (account, res.status_code, res.text))
            return 404

    # 注册接口
    def signUp(server_url: str, token: str, account: str, password: str,
               areaCode: str, en_key: str):
        _password = password + en_key
        md5 = hashlib.md5()
        md5.update(_password.encode(encoding='utf-8'))
        url = '/webapi/user/addUser'
        headers = {'Content-Type': 'application/json', 'token': token}
        data = {}
        if account.isdigit():
            data = json.dumps({
                'account': account,
                'accountType': 1,
                'password': md5.hexdigest(),
                'areaCode': areaCode
            })
        else:
            data = json.dumps({
                'account': account,
                'accountType': 2,
                'password': md5.hexdigest(),
            })
        print('正在创建账号...')

        res_suss = 0
        while res_suss < 3:
            try:
                res = requests.post(server_url + url,
                                    headers=headers,
                                    data=data)
                res_json = res.json()
                res_suss = 3
            except requests.exceptions.RequestException:
                res_suss += 1
                print('----连接失败,3秒后重连')
                MyTimer.waitTime(3)

        if res.status_code == 200:
            if res_json['code'] == 200:
                print('----\033[0;32;40m账号 %s 创建成功\033[0m' % account)
                return 200
            else:
                print('----\033[0;37;41m账号 %s 创建失败\033[0m' % account)
                return -1
        else:
            print(
                '----\033[0;37;41m创建账号 %s 时与服务器连接失败 ---- code: %d ---- 错误信息: %s\033[0m'
                % (account, res.status_code, res.text))
            return -1

    # 修改用户信息
    def userInfo(api_url: str, token: str, avatar: str, nickName: str,
                 birthday: str, intro: str):
        _birthday = birthday + ' 00:00:00'
        time_stamp = MyTimer.getTimer13(_birthday)
        url = '/api/user/updateUserInfo'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'token': token
        }
        data = {
            'avatar': avatar,
            'nickName': nickName,
            'birthday': int(time_stamp),
            'intro': intro
        }
        print('正在更新用户信息...')

        res_suss = 0
        while res_suss < 3:
            try:
                res = requests.post(api_url + url, headers=headers, data=data)
                res_json = res.json()
                res_suss = 3
            except requests.exceptions.RequestException:
                res_suss += 1
                print('----连接失败,3秒后重连')
                MyTimer.waitTime(3)

        if res.status_code == 200:
            if res_json['code'] == 200:
                print('----\033[0;32;40m用户信息更新成功\033[0m')
                return 200
            else:
                print('----\033[0;37;41m用户信息更新失败\033[0m')
                return -1
        else:
            print('----\033[0;37;41m用户信息更新失败 ---- code: ' + res.status_code +
                  ' ---- 错误信息: ' + res.text + '\033[0m')
            return -1

    # 添加订阅组
    def addGroup(api_url: str, token: str, groupName: str, groupPic: str,
                 amount: int):
        url = '/api/subscribeGroup/create'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'token': token
        }
        data = {
            'groupName': groupName,
            'groupPic': groupPic,
            'amount': amount,
            'timeLen': 30
        }
        print('正在创建分组 ' + groupName)

        res_suss = 0
        while res_suss < 3:
            try:
                res = requests.post(api_url + url, headers=headers, data=data)
                res_json = res.json()
                res_suss = 3
            except requests.exceptions.RequestException:
                res_suss += 1
                print('----连接失败,3秒后重连')
                MyTimer.waitTime(3)

        if res.status_code == 200:
            if res_json['code'] == 200:
                print('----\033[0;32;40m分组 %s 创建成功\033[0m' % groupName)
                return 200
            else:
                print('----\033[0;37;41m分组 %s 创建失败\033[0m' % groupName)
                return -1
        else:
            print('----\033[0;37;41m分组创建失败 ---- code: ' + res.status_code +
                  ' ---- 错误信息: ' + res.text + '\033[0m')
            return -1
