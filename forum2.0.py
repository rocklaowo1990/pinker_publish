import json
import os
import numpy as np

from servers.consol import consol
from servers.exls import exls
from servers.file import file
from servers.response import response
from selenium import webdriver
from selenium.webdriver.common.by import By
# 第一步: 读取文件
# 1、读取历史文件
# 2、读取表格文件, 并且把数据储存到临时数据
# 3、处理数据
# 保存历史

# 打包
# pyinstaller -F forum.py --clean


def get(url: str):
    driver = webdriver.Chrome()
    driver.implicitly_wait(300)  # seconds
    try:
        driver.get(url)
        return driver.page_source
    except:
        return None


def getForumName(url: str):
    '''
    ### 解析论坛
    得到论坛的主域名
    '''
    domain = url
    domain = domain.replace('www.', '')
    domain = domain.replace('//forum.', '')
    domain = domain.replace('//forums.', '')
    domain = domain.replace('//news.', '')
    domain = domain.replace('//new.', '')
    domain = domain.replace('//foro.', '')
    domain = domain.replace('//foros.', '')
    domain = domain.replace('//', '')
    domain = domain.split(':')[-1]
    domain = domain.split('.')[0]
    return domain


def getString(keywords):
    '''
    ### 解析表格里的数据
    转成字符串
    '''
    keywordsTemp = str(keywords)
    if keywordsTemp == '' or keywordsTemp is np.nan or keywordsTemp.upper(
    ) == 'nan'.upper():
        return ''
    else:
        return keywordsTemp


# 这个是判断有没有正确输入目标目录
isInput = False

# 一直要求输入目标文件夹的名称, 直到正确输入
while not isInput:
    pathTaget = input('请输入目录名称 : ')
    if pathTaget != '':
        if file.isHave(pathTaget):
            consol.suc('目录查找成功: %s' % (pathTaget))
            consol.suc(os.listdir(pathTaget))
            isInput = True

        elif pathTaget == 'exit':
            exit()
        elif pathTaget == 'exit':
            consol.log(os.listdir(pathTaget))
        else:
            consol.err('没有找到相关的目录, 请重新输入')
    else:
        consol.err('不能输入空的')

print()

# 表格数据对象
# ---------------------------------------------------------
# data: 表格数据的格式化
# data = {
#     '表格的名字': {
#         'sheet名字': [{
#             'page_1': str,                #第一页地址
#             'page_2': str,                #第二页地址
#             'page_3': str,                #第三页地址
#             'titile': str,                #论坛标题
#             'nickName': str               #昵称
#         }],
#         'sheet名字': [{
#             'page_1': str,                #第一页地址
#             'page_2': str,                #第二页地址
#             'page_3': str,                #第三页地址
#             'titile': str,                #论坛标题
#             'nickName': str               #昵称
#         }]
#     },
#     '表格的名字': {
#         'sheet名字': [{
#             'page_1': str,                #第一页地址
#             'page_2': str,                #第二页地址
#             'page_3': str,                #第三页地址
#             'titile': str,                #论坛标题
#             'nickName': str               #昵称
#         }],
#         'sheet名字': [{
#             'page_1': str,                #第一页地址
#             'page_2': str,                #第二页地址
#             'page_3': str,                #第三页地址
#             'titile': str,                #论坛标题
#             'nickName': str               #昵称
#         }]
#     }
# }
# ---------------------------------------------------------
data = {}

# 每个人的历史记录对象
# ---------------------------------------------------------
# history: 历史记录的格式化
# history = {
#      '表格名称': {
#           'failure': list[str],       #审核失败的论坛
#           'repeated': list[str],      #和别人重复的论坛
#           'successful': list[str],    #审核通过的论坛
#           'process‘: int              #处理总数量
#       },
#      '表格名称': {
#           'failure': list[str],       #审核失败的论坛
#           'repeated': list[str],      #和别人重复的论坛
#           'successful': list[str],    #审核通过的论坛
#           'process': int              #处理总数量
#       },
# }
# ---------------------------------------------------------
history = {}

# 还会用一个文件记录所有发送成功的并且不重复的论坛
# 这个文件会在 py 文件的目录下, 也就是根目录
consol.log('正在读取统计表...', pathTaget)
successful = []
failure = []
repeated = []

pathSuccessful = os.path.join('', '成功统计表.xlsx')
pathFailure = os.path.join('', '失败统计表.xlsx')
pathRepeated = os.path.join('', '重复统计表.xlsx')

if file.isHave(pathSuccessful):
    # 开始读取表格信息
    # 读取的是单个表格文件的所有 sheet
    successfulRead = exls.read(pathSuccessful)
    # 开始分析表格数据
    # 主要是看这个表格有多少页
    # 每一页都需要解析出来
    for sheetName, sheetData in successfulRead.items():
        sheetDataTemp = sheetData.to_dict(orient='records')
        # 读取每一行的信息
        for rowData in sheetDataTemp:
            # 把每一行的信息转成数组
            rowDataTemp = list(rowData.values())
            successful.append(rowDataTemp[0])

consol.suc('成功统计表读取成功: %s\n' % successful, pathTaget)

if file.isHave(pathFailure):
    # 开始读取表格信息
    # 读取的是单个表格文件的所有 sheet
    failureRead = exls.read(pathFailure)
    # 开始分析表格数据
    # 主要是看这个表格有多少页
    # 每一页都需要解析出来
    for sheetName, sheetData in failureRead.items():
        sheetDataTemp = sheetData.to_dict(orient='records')
        # 读取每一行的信息
        for rowData in sheetDataTemp:
            # 把每一行的信息转成数组
            rowDataTemp = list(rowData.values())
            failure.append(rowDataTemp[0])

consol.suc('失败统计表读取成功: %s\n' % failure, pathTaget)

if file.isHave(pathRepeated):
    # 开始读取表格信息
    # 读取的是单个表格文件的所有 sheet
    repeatedRead = exls.read(pathRepeated)
    # 开始分析表格数据
    # 主要是看这个表格有多少页
    # 每一页都需要解析出来
    for sheetName, sheetData in repeatedRead.items():
        sheetDataTemp = sheetData.to_dict(orient='records')
        # 读取每一行的信息
        for rowData in sheetDataTemp:
            # 把每一行的信息转成数组
            rowDataTemp = list(rowData.values())
            repeated.append(rowDataTemp[0])

consol.suc('重复统计表读取成功: %s\n' % repeated, pathTaget)

filesTaget = os.listdir(pathTaget)

# 开始读取每一个文件 每个文件代表的是一个表格(一个人)
# 表格的文件数据放到 data
# 历史记录的数据放到 history
for fileName in filesTaget:
    pathFile = os.path.join(pathTaget, fileName)

    isXls = '.xls'.upper() in fileName.upper()
    isXlsx = '.xlsx'.upper() in fileName.upper()
    isCsv = '.csv'.upper() in fileName.upper()
    isHistory = 'history.json'.upper() in fileName.upper()

    if isHistory:
        consol.log('开始读取历史记录...', pathTaget)
        history = file.read(pathFile)
        consol.suc('读取成功: %s\n' % history, pathTaget)

    if isXls or isXlsx or isCsv:
        consol.log('正在检查文件: %s ' % (pathFile), pathTaget)

        # 开始读取表格信息
        # 读取的是单个表格文件的所有 sheet
        dataRead = exls.read(pathFile)

        # 每个表格都是一个人, 这个人有一个数据
        # 表格的数据是由多个 sheet 组成
        dataExcel = {}

        # 开始分析表格数据
        # 主要是看这个表格有多少页
        # 每一页都需要解析出来
        for sheetName, sheetData in dataRead.items():
            # 格式化表格文件
            sheetDataTemp = sheetData.to_dict(orient='records')
            consol.log('正在读取表格: %s ==> %s 的数据...\n' % (fileName, sheetName),
                       pathTaget)

            # 每一个 sheet 也有一个数据
            # 每个 sheet 是有多行数据组成
            dataSheet = []

            # 读取每一行的信息
            for rowData in sheetDataTemp:
                consol.log('%s' % (rowData), pathTaget)

                # 每一行也有数据的, 我们需要解析出来
                dataRow = {}

                # 把每一行的信息转成数组
                rowDataTemp = list(rowData.values())

                dataRow['page_1'] = getString(rowDataTemp[0]).strip()
                dataRow['page_2'] = getString(rowDataTemp[1]).strip()
                dataRow['page_3'] = getString(rowDataTemp[2]).strip()
                dataRow['title'] = getString(rowDataTemp[3]).strip()
                dataRow['nickName'] = getString(rowDataTemp[4]).strip()

                # 把每一个 行 的数据添加到 Sheet 里
                # 这里我们要加一个条件:
                # 1、没有标题的不添加, 标题不能为空
                # 2、三个地址都是空的不添加
                # 3、没有发帖人昵称的不添加
                # 4、三个地址所属论坛不一样的不添加 : 默认是 True
                isHaveTile = dataRow['title'] != ''

                isEmpty = dataRow['page_1'] == '' and dataRow[
                    'page_2'] == '' and dataRow['page_3'] == ''

                isHaveNickName = dataRow['nickName'] != ''

                # 为了判断三个地址是不是属于一个论坛, 这里需要临时创建一个数组
                # 把不是空的链接放进去
                urls = []
                if dataRow['page_1'] != '':
                    urls.append(getForumName(dataRow['page_1']))

                if dataRow['page_2'] != '':
                    urls.append(getForumName(dataRow['page_2']))

                if dataRow['page_3'] != '':
                    urls.append(getForumName(dataRow['page_3']))

                consol.suc(
                    '解析完成: 论坛地址%s  标题: %s  发帖人昵称: %s' %
                    (urls, dataRow['title'], dataRow['nickName']), pathTaget)

                # 把每一行的数据添加到 sheet 里
                if isHaveTile and not isEmpty and isHaveNickName:
                    consol.suc('数据格式正常,已经添加到数据库...\n', pathTaget)
                    dataSheet.append(dataRow)
                else:
                    consol.err('数据格式错误,请检查论坛地址, 标题, 昵称是否输入正确\n', pathTaget)

            dataExcel[sheetName] = dataSheet
            consol.suc(
                '%s ==> %s 的数据读取完成: %s\n' %
                (fileName, sheetName, dataExcel[sheetName]), pathTaget)

        data[fileName] = dataExcel
        consol.suc('%s 的数据读取完成: %s\n\n\n' % (pathFile, data[fileName]),
                   pathTaget)

consol.suc('数据读取成功: %s\n\n\n' % (data), pathTaget)
consol.suc('开始处理审核任务...\n\n\n', pathTaget)

# 这里开始就是处理任务
# 会一个表格一个表格的来
# 每个人先和自己的历史记录对比一下, 看有没有处理过的
for dk, dv in data.items():  #文件 也是这个人
    # 先看看是不是有这个人的历史记录
    # 如果有的话就调出来
    if not dk in history.keys():
        history[dk] = {
            'failure': [],  #审核失败的论坛
            'repeated': [],  #和别人重复的论坛
            'successful': [],  #审核通过的论坛
            'process': 0  #处理总数量
        }
    for sk, sv in dict(dv).items():  #sheet 表格的页码
        sallIndex = 0
        for mi in list(sv):  #处理表格每一行的数据
            url_1 = mi['page_1']
            url_2 = mi['page_2']
            url_3 = mi['page_3']
            title = mi['title']
            nick = mi['nickName']

            keywords = str(title).strip()
            keywords = keywords.replace('\r', '')
            keywords = keywords.replace('\r', '')
            keywords = keywords.replace('\t', '')
            keywords = keywords.replace('\n', '')

            sallIndex += 1
            sall = len(list(sv))

            # 默认都是审核通过
            isPass = False

            logStr = '%s > %s > 当前的进度: %s / %s' % (dk, sk, sallIndex, sall)
            consol.log(logStr, pathTaget)
            consol.log('%s > %s > 帖子的标题: %s' % (dk, sk, title), pathTaget)
            consol.log('%s > %s > 发帖人昵称: %s' % (dk, sk, nick), pathTaget)

            urls = []

            if url_1 != '':
                urls.append(url_1)

            if url_2 != '':
                urls.append(url_2)

            if url_3 != '':
                urls.append(url_3)

            isAddRe = False

            i = 0
            for url in urls:
                logStr = '%s > %s > 论坛的地址: %s' % (dk, sk, url)
                consol.log(logStr, pathTaget)

                logStr = '%s > %s > 论坛的名字: %s' % (
                    dk,
                    sk,
                    getForumName(url),
                )
                consol.log(logStr, pathTaget)

                # 先看这个论坛需不需要处理
                # 1、和历史记录有重复的不处理
                if getForumName(url).upper() in ' '.join(
                        history[dk]['successful']).upper():
                    logMes = '这个地址处理过'
                    logStr = '%s > %s > 论坛的处理: %s' % (dk, sk, logMes)
                    consol.err(logStr, pathTaget)
                    break

                # 再看和别人是不是重复的
                # 先把 data 数据复制一份出来
                # 然后删掉自己名字的值
                # 然后循环判断有没有重复
                dataTemp = data.copy()
                dataTemp.pop(dk)
                reWords = ''
                rePer = 0
                for dk_1, dv_1 in dataTemp.items():
                    isRe = False
                    for sk_1, sv_1 in dict(dv_1).items():
                        for mi_1 in list(sv_1):
                            or_1 = getForumName(url).upper() in str(
                                mi_1['page_1']).upper()
                            or_2 = getForumName(url).upper() in str(
                                mi_1['page_2']).upper()
                            or_3 = getForumName(url).upper() in str(
                                mi_1['page_3']).upper()
                            if or_1 or or_2 or or_3:
                                isRe = True
                                rePer += 1
                                reWords += '%s | ' % (dk_1)
                                break
                        if isRe:
                            break

                # 如果重复的论坛数量大于0
                # 说明三个地址里面肯定有一个是重复的
                # 那么重复的条件成立
                if rePer > 0:
                    reWords = reWords[0:-3]
                    logStr = '%s > %s > 重复的对象: %d (%s)' % (dk, sk, rePer,
                                                           reWords)
                    consol.err(logStr, pathTaget)
                    if not isAddRe:
                        isAddRe = True
                        logRe = '%s => 和 %d 人重复 (%s)' % (url, rePer, reWords)
                        if not getForumName(url).upper() in ' '.join(
                                history[dk]['repeated']).upper():
                            history[dk]['repeated'].append(url)
                        if not getForumName(url).upper() in ' '.join(
                                repeated).upper():
                            repeated.append(url)

                # 开始审核
                # 审核需要打开网页进行检查
                requests = response.get(url)
                if not requests is None:

                    isImportTitle = keywords.upper(
                    ) in requests.page_source.upper()
                    isImportNick = str(
                        nick).upper() in requests.page_source.upper()

                    if isImportTitle or isImportNick:
                        isPass = True
                        logMes = '审核通过'
                        logStr = '%s > %s > 论坛的处理: %s' % (dk, sk, logMes)
                        consol.suc(logStr, pathTaget)

                        index = 0
                        while index < len(failure):
                            if getForumName(url).upper() in ''.join(
                                    failure).upper():
                                failure.remove(failure[index])
                            else:
                                index += 1

                        if not getForumName(url).upper() in ' '.join(
                                successful).upper():
                            successful.append(url)

                        if not getForumName(url).upper() in ' '.join(
                                history[dk]['successful']).upper():
                            history[dk]['successful'].append(url)
                        break

                    else:
                        logMes = '审核失败'
                        logStr = '%s > %s > 论坛的处理: %s' % (dk, sk, logMes)
                        consol.err(logStr, pathTaget)

                        logRe = '%s => 审核失败' % (url)

                        if not getForumName(url).upper() in ' '.join(
                                failure).upper():
                            failure.append(url)

                        if not getForumName(url).upper() in ' '.join(
                                history[dk]['failure']).upper():
                            history[dk]['failure'].append(url)

                else:
                    logMes = '访问失败'
                    logStr = '%s > %s > 论坛的处理: %s' % (dk, sk, logMes)
                    consol.err(logStr, pathTaget)
                    logRe = '%s => 访问失败' % (url)

                    if not getForumName(url).upper() in ' '.join(
                            failure).upper():
                        failure.append(url)

                    if not getForumName(url).upper() in ' '.join(
                            history[dk]['failure']).upper():
                        history[dk]['failure'].append(url)

                i += 1

            if isPass:
                logMes = '审核通过'
                logStr = '%s > %s > 处理的结果: %s (总数: %d  通过: %d  不通过: %d  重复: %d  重复率:%.2f%%)\n\n' % (
                    dk,
                    sk,
                    logMes,
                    len(history[dk]['successful']) +
                    len(history[dk]['failure']),
                    len(history[dk]['successful']),
                    len(history[dk]['failure']),
                    len(history[dk]['repeated']),
                    len(history[dk]['repeated']) /
                    (len(history[dk]['successful']) +
                     len(history[dk]['failure'])) * 100,
                )
                consol.suc(logStr, pathTaget)
            else:
                logMes = '审核不通过'
                logStr = '%s > %s > 处理的结果: %s (总数: %d  通过: %d  不通过: %d  重复: %d  重复率:%.2f%%)\n\n' % (
                    dk,
                    sk,
                    logMes,
                    len(history[dk]['successful']) +
                    len(history[dk]['failure']),
                    len(history[dk]['successful']),
                    len(history[dk]['failure']),
                    len(history[dk]['repeated']),
                    len(history[dk]['repeated']) /
                    (len(history[dk]['successful']) +
                     len(history[dk]['failure'])) * 100,
                )
                consol.err(logStr, pathTaget)

    # 写入结果
    history[dk]['process'] = len(history[dk]['successful']) + len(
        history[dk]['failure'])

    resaultTile = '========== %s ==========\n\n' % (dk)
    resaultNumber = '处理总数: %d (通过 %d  不通过 %d  和别人重复 %d  重复率 %.2f%%)\n\n' % (
        history[dk]['process'],
        len(history[dk]['successful']),
        len(history[dk]['failure']),
        len(history[dk]['repeated']),
        len(history[dk]['repeated']) /
        (len(history[dk]['successful']) + len(history[dk]['failure'])) * 100,
    )

    resaultSus = '通过的论坛: %d\n%s\n\n' % (
        len(history[dk]['successful']),
        '\n'.join(history[dk]['successful']),
    )

    resaultFair = '不通过的论坛: %d\n%s\n\n' % (
        len(history[dk]['failure']),
        '\n'.join(history[dk]['failure']),
    )

    resaultRe = '重复的论坛: %d\n%s\n\n\n' % (
        len(history[dk]['repeated']),
        '\n'.join(history[dk]['repeated']),
    )

    resauletStr = '%s%s%s%s%s' % (
        resaultTile,
        resaultNumber,
        resaultSus,
        resaultFair,
        resaultRe,
    )
    consol.suc(resauletStr, pathTaget)
    pathResault = os.path.join(
        pathTaget,
        '%s的结果.txt' % (str(dk).replace('.xlsx', '')),
    )
    file.write(pathResault, resauletStr, 'w+')

consol.log('正在写入数据和表格...')

pathHistory = os.path.join(pathTaget, 'history.json')
file.write(pathHistory, json.dumps(history), 'w+')

xlsxData = {'成功统计': successful}
exls.write(pathSuccessful, xlsxData, '成功统计表')

xlsxData = {'失败统计': failure}
exls.write(pathFailure, xlsxData, '失败统计表')

xlsxData = {'重复统计': repeated}
exls.write(pathRepeated, xlsxData, '重复统计表')

consol.suc('写入完成...')
