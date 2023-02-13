import os

import numpy as np
from servers.consol import consol
from servers.exls import exls
from servers.file import file
from servers.response import response


def get_forum_name(url: str):
    domain = url.replace('www.', '')
    domain = domain.replace('forum.', '')
    domain = domain.split('//')[-1]
    domain = domain.split('.')[0]
    return domain


# 找出根目录里所有的文件夹
listdir = os.listdir()

# 输入目录名称
is_path_name_pass = False
input_path_name = ''
while not is_path_name_pass:
    input_path_name = input('请输入目录名称 : ')

    if input_path_name != '':
        if input_path_name in listdir:
            consol.suc('目录查找成功')
            is_path_name_pass = True
        else:
            consol.err('没有找到相关的目录，请重新输入')

    else:
        consol.err('不能输入空的')

log_file = ''

for dir in listdir:
    if dir == input_path_name:
        forum_path = os.path.join('', dir)
        list_exls = os.listdir(forum_path)
        file.check(list_exls, forum_path)

        # 开始遍历每一个表格文件
        # exls_file 就是文件单个人的表格
        for exls_file in list_exls:
            if '.exls'.upper() in exls_file.upper() or '.xlsx'.upper(
            ) in exls_file.upper():
                # 表格的路径
                exls_path = os.path.join(forum_path, exls_file)

                print()
                print()

                consol.log('正在检查文件: %s ' % (exls_file))

                # 历史记录
                history = []

                # 开始读取表格信息
                # 读取的是单个表格文件的所有 sheet
                exls_data = exls.read(exls_path)

                for sheet_name, sheet_data in exls_data.items():
                    # 格式化表格文件
                    sheet_data = sheet_data.to_dict(orient='records')

                    consol.log('正在审核: %s ==> %s' % (exls_file, sheet_name))

                    # 单个表格的成功数量
                    successful = 0

                    # 单个表格的失败数量
                    failure = 0
                    failure_forum = ''

                    # 单个表格相同的帖子总数量
                    same = 0
                    same_forum = ''

                    # 单个表格处理的论坛总数量
                    process_all = 0

                    print()
                    print()

                    # 读取每一行的信息
                    for row_data in sheet_data:

                        # 单个链接失败的理由
                        failure_why = ''

                        # 把每一行的信息转成数组
                        row_data = list(row_data.values())

                        # 单行的三个链接，需要有至少 1 个包含标题
                        # 否则的话，审核不通过
                        single_sus = 0

                        # 解析论坛地址的方法
                        domain = get_forum_name(str(row_data[0]))

                        keywords = str(row_data[3]).strip()
                        keywords = keywords.replace('\r', '')
                        keywords = keywords.replace('\r', '')
                        keywords = keywords.replace('\t', '')
                        keywords = keywords.replace('\n', '')

                        consol.log('正在审核论坛：%s' % (domain))
                        consol.log('帖子标题：%s' % (keywords))
                        consol.log('发帖人昵称：%s' % (str(row_data[4])))

                        # 如果帖子的标题为空，跳过不检查
                        if keywords == '' or keywords is np.nan or keywords == 'nan':
                            consol.err('帖子的标题看起来不太对，跳过处理')
                            continue

                        # 如果帖子的发帖人为空，跳过不检查
                        if str(row_data[4]
                               ) == '' or row_data[4] is np.nan or str(
                                   row_data[4]) == 'nan':
                            consol.err('发帖人的昵称看起来不太对，跳过处理')
                            continue

                        # 处理一行的时候
                        # 处理的总数需要 +1
                        process_all += 1

                        # 三页里面是否有重复的帖子
                        is_same = False

                        # 和其他人相同的人数
                        same_person = 0
                        same_person_name = ''

                        # 论坛页码的下标
                        # 一共检查3页
                        index = 0
                        while index < 3:

                            # 首先看地址的合法性
                            if str(row_data[index]) != '' and not str(
                                    row_data[index]) is np.nan and str(
                                        row_data[index]
                                    ) != 'nan' and 'http' in str(
                                        row_data[index]):

                                # 解析论坛地址的方法
                                domain = get_forum_name(str(row_data[index]))

                                # 检查和其他人的论坛
                                # 和其他人论坛重复率很高的给予提示
                                # 提示语：和另外 5 个人的论坛相同
                                # 和其他人相同的论坛数量给一个总数统计就，再算一下相同率
                                if not is_same:
                                    for same_file in list_exls:

                                        if ('.exls'.upper()
                                                in same_file.upper()
                                                or '.xlsx'.upper()
                                                in same_file.upper()
                                            ) and same_file != exls_file:
                                            # 表格的路径
                                            same_path = os.path.join(
                                                forum_path, same_file)
                                            # 开始读取表格信息
                                            # 读取的是单个表格文件的所有 sheet
                                            same_data = exls.read(same_path)
                                            same_data = str(same_data)

                                            if domain in same_data:
                                                same_person += 1
                                                same_person_name += '%s | ' % (
                                                    same_file)
                                                is_same = True

                                # 检查是否和之前的论坛相同，一个人不能有重复的论坛出现
                                if domain in history:
                                    failure_why += '地址重复 | '
                                    consol.log('正在访问论坛 %s 的第 %d 页: 地址重复' %
                                               (domain, index + 1))
                                    index += 1
                                    continue

                                consol.log(
                                    '正在访问论坛 %s 的第 %d 页: %s' %
                                    (domain, index + 1, row_data[index]))

                                requests = response.get(row_data[index])

                                if not requests is None:

                                    if keywords.upper() in requests.upper(
                                    ) or str(row_data[4]) in requests.upper():
                                        single_sus += 1
                                        consol.suc('访问成功: 已检查到关键字')

                                    else:
                                        failure_why += '未检测到关键字 | '
                                        consol.suc('访问成功: 未检测到关键字')

                                else:
                                    failure_why += '访问失败 | '
                                    consol.err('访问失败')

                            else:
                                failure_why += '地址不合法 | '
                                consol.log('正在访问论坛 %s 的第 %d 页: %s' %
                                           (domain, index + 1, '地址不合法'))

                            index += 1

                        if same_person > 0:
                            same += 1
                            same_forum += '%s (%d: %s)\n' % (
                                str(row_data[0]), same_person,
                                same_person_name[0:-3])
                            consol.err(
                                '论坛 %s 和其他 %d 个人重复，重复总数 %d , 处理论坛总数 %d , 重复率 %f'
                                % (domain, same_person, same, process_all,
                                   same / process_all))

                        if single_sus > 0:
                            consol.suc('审核结果: 通过')
                            successful += 1
                            history.append(domain)
                        else:
                            consol.err('审核结果: 不通过(原因：%s)' %
                                       (failure_why[0:-3]))
                            failure_forum += '%s (原因：%s)\n' % (str(
                                row_data[0]), failure_why[0:-3])
                            failure += 1

                        consol.suc('论坛处理总数: %d (审核通过总：%d , 审核不通过: %d)' %
                                   (process_all, successful, failure))

                        print()
                        print()

                    # 处理完了一个表格需要输出日志
                    consol.suc('%s ==> 成功发帖 %d 个 , 处理的论坛总数量: %d' %
                               (exls_file, successful, process_all))

                    consol.log('正在写入日志...')

                    # 没有处理的就不写入日志里
                    # 处理总数量大于0为判定条件
                    log_path = os.path.join(forum_path, 'log.txt')
                    if process_all > 0:
                        with open(log_path, 'a') as f:
                            f.write(
                                str('%s ==> %s 论坛处理总数: %d (通过: %d , 不通过: %d , 重复: %d , 重复率 %f)\n===== 审核不通过的论坛 =====\n%s\n===== 和别人重复的论坛 =====\n%s\n'
                                    % (exls_file, sheet_name, process_all,
                                       successful, failure, same, same /
                                       process_all if process_all != 0 else 0,
                                       failure_forum, same_forum)))

                    f.close()

                    consol.suc('日志写入完成...')
                    print()
                    print()

consol.suc('任务处理完成，程序退出...')
