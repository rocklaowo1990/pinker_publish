import json
import requests
import hashlib
import json
from server.aes import Aes
from server.timer import Timer

class Api:
    # 获取平台配置
    def config(api_url: str):
        data = {}
        url = '/api/common/config'
        headers = {
            'Content-Type': 'application/json',
        }
        print('正在获取平台设置')
        res = requests.get(api_url + url, headers=headers)
        res_json = res.json()

        data['enKey'] = 'pinker.' + res_json['data']['encryptConfig']['enKey']
        data['iv'] = 'pinker.' + res_json['data']['encryptConfig']['iv']
        accessKey = Aes.decrypt(data['enKey'],res_json['data']['awsConfig']['accessKey'],data['iv'])
        data['accessKey'] = accessKey
        region = Aes.decrypt(data['enKey'],res_json['data']['awsConfig']['region'],data['iv'])
        data['region'] = region
        secretKey = Aes.decrypt(data['enKey'],res_json['data']['awsConfig']['secretKey'],data['iv'])
        data['secretKey'] = secretKey
        bucket = Aes.decrypt(data['enKey'],res_json['data']['awsConfig']['bucket'],data['iv'])
        data['bucket'] = bucket
        if res.status_code == 200:
            if res_json['code'] == 200:
                print('平台信息获取成功')
                return data
            else:
                print('获取平台设置失败：%s' % res_json['msg'])
                return ''
        else:
            print('获取平台设置失败' +
                  res.status_code + ' ---- 错误信息：')
            return ''

    # 登录接口
    def login(api_url: str, account: str, password: str, en_key:str):
        _password = password + en_key
        url = '/api/account/login'
        md5 = hashlib.md5()
        md5.update(_password.encode(encoding='utf-8'))
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'account': account,
            'password': md5.hexdigest(),
            'accountType': 1 if str(account).isdigit() else 2,
        }
        print('正在登录：' + account)
        res = requests.post(api_url + url, data=data, headers=headers)
        res_json = res.json()
        if res.status_code == 200:
            if res_json['code'] == 200:
                print('账号：' + account + '登录成功')
                return str(res_json['data']['token'])
            else:
                print('账号 ' + account + ' 登录失败 ' + res_json['msg'])
                return '-1'
        else:
            print('账号：' + account + ' 登录失败 ---- code: ' +
                  res.status_code + ' ---- 错误信息：' + res.text)
            return ''


    # 后台登录接口
    def loginServer(server_url: str, account: str, password: str):
        url = '/webapi/account/login'
        headers = {
            'Content-Type': 'application/json',
            'browser': 'Chrome'
        }
        data = json.dumps({
            'account': account,
            'password': password
        }) 
        print('正在登录后台账号：' + account)
        
        res = requests.post(server_url + url, data=data, headers=headers)
        res_json = res.json()
        if res.status_code == 200:
            if res_json['code'] == 200:
                print('后台账号：' + account + '登录成功')
                
                return str(res_json['data']['token'])
            else:
                print('后台账号 ' + account + ' 登录失败 ' + res_json['msg'])
                return '-1'
        else:
            print('后台账号：' + account + ' 登录失败 ---- code: ' +
                  res.status_code + ' ---- 错误信息：' + res.text)
            return ''


    # 获取分组信息
    def myGroupList(api_url: str, token: str,account:str):
        url = '/api/subscribeGroup/myGroupList'
        headers = {
            'Content-Type': 'application/json',
            'token': token
        }
        print('正在获取用户 %s 订阅组信息' % account)
        res = requests.get(api_url + url, headers=headers)
        res_json = res.json()
        if res.status_code == 200:
            if res_json['code'] == 200:
                print('用户 %s 订阅组信息获取成功' % account)
                return res_json['data']['list']
            elif res_json['code'] == 1:
                print('用户 %s 的 token 过期，正在重新登录' % account)
                return 1
            else:
                print('用户 %s 订阅组信息获取失败：%s' % (account, res_json['msg']))
                return []
        else:
            print('用户 %s 的订阅组信息获取失败 ---- code: ' +
                  res.status_code + ' ---- 错误信息：' + res.text % account)
            return []

    # 发推接口
    def publish(api_url: str, token: str, data:dict, account:str):
        url = '/api/content/publish'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'token': token
        }
        print('正在发布推文')
        res = requests.post(api_url + url, headers=headers, data=data)
        res_json = res.json()
        if res.status_code == 200:
            if res_json['code'] == 200:
                print('用户 %s 推文发布成功' % account)
                return 200
            elif res_json['code'] == 1:
                print('用户 %s 的 token 过期，正在重新登录' % account)
                return 1
            else:
                print('用户 %s 推文发布失败 %s' % (account, res_json['msg']))
                return -1
        else:
            print('用户 %s 的推文发布失败 ---- code: ' +
                  res.status_code + ' ---- 错误信息：' + res.text % account)
            return -1

    # 检查账号是否重复
    def checkAccount(api_url:str, account:str):
        url = '/api/account/verificateAccount'
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            'account': account,
        }
        print('正在验证账号 %s 是否已经存在...' % account)
        res = requests.get(api_url + url, headers=headers, params=data)
        res_json = res.json()
        if res.status_code == 200:
            if res_json['code'] == -1:
                print('账号 %s 可以注册 %s' % (account, res_json['msg']))
                return 200
            else:
                print('账号 %s 已经存在，或者出现了其他错误，错误代码：%d' % (account,res_json['code']))
                return -1
        else:
            print('检测账号 %s 是否存在时与服务器连接失败 ---- code: ' + res.status_code + ' ---- 错误信息：' + res.text % account)
            return 404


    # 注册接口
    def signUp(server_url: str, token:str, account:str, password:str, areaCode:str, en_key:str):
        _password = password + en_key
        md5 = hashlib.md5()
        md5.update(_password.encode(encoding='utf-8'))
        url = '/webapi/user/addUser'
        headers = {
            'Content-Type': 'application/json',
            'token': token
        }
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
        
        res = requests.post(server_url + url, headers=headers, data=data)
        res_json = res.json()
        if res.status_code == 200:
            if res_json['code'] == 200:
                print('账号 %s 创建成功' % account)
                return 200
            else:
                print('账号 %s 创建失败' % account)
                return -1
        else:
            print('创建账号 %s 时与服务器连接失败 ---- code: ' + res.status_code + ' ---- 错误信息：' + res.text % account)
            return -1

    
    # 修改用户信息
    def userInfo(api_url: str, token:str, avatar:str, nickName:str, birthday:str, intro:str):
        _birthday = birthday + ' 00:00:00'
        time_stamp = Timer.getTimer13(_birthday)
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
        
        res = requests.post(api_url + url, headers=headers, data=data)
        res_json = res.json()
        if res.status_code == 200:
            if res_json['code'] == 200:
                print('用户信息更新成功')
                return 200
            else:
                print('用户信息更新失败 XXXXXX')
                return -1
        else:
            print('用户信息更新失败 ---- code: ' + res.status_code + ' ---- 错误信息：' + res.text)
            return -1

    
    # 添加订阅组
    def addGroup(api_url: str, token:str, groupName:str, groupPic:str, amount:int):
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
        
        res = requests.post(api_url + url, headers=headers, data=data)
        res_json = res.json()
        if res.status_code == 200:
            if res_json['code'] == 200:
                print('分组 %s 创建成功' % groupName)
                return 200
            else:
                print('分组 %s 创建失败' % groupName)
                return -1
        else:
            print('分组创建失败 ---- code: ' + res.status_code + ' ---- 错误信息：' + res.text)
            return -1