import datetime
import time

from servers.consol import consol


class timer:
    '''
    时间的处理
    '''

    # 得到13位时间戳
    def timetuple(time_str: str):
        '''### 生成13位的时间戳'''

        # 将时间转成特定格式
        datetime_obj = datetime.datetime.strptime(
            time_str,
            '%Y-%m-%d %H:%M:%S',
        )

        # 得到10位的时间戳,时间点相当于从1.1开始的当年时间编号
        date_stamp = str(int(time.mktime(datetime_obj.timetuple())))

        # 精确到豪秒：得到毫秒的值
        data_microsecond = str("%06d" % datetime_obj.microsecond)[0:3]

        # 最后吧结果连起来生成13位的字符串
        date_stamp = date_stamp + data_microsecond

        # 返回13位整数
        return int(date_stamp)

    # 等待 N 秒
    def wait(duration: int):
        '''
        等待 N 秒
        '''
        _duration = 0
        while _duration < duration:
            if duration < 60:
                consol.log('%d 秒后开始...' % (duration - _duration))
            elif duration < 3600:
                _m = (duration - _duration) // 60
                _s = (duration - _duration) % 60
                consol.log('%d 分 %d 秒后开始...' % (_m, _s))
            else:
                _h = (duration - _duration) // 3600
                _m = ((duration - _duration) % 3600) // 60
                _s = ((duration - _duration) % 3600) % 60
                consol.log('%d 时 %d 分 %d 秒后开始...' % (_h, _m, _s))
            time.sleep(1)
            _duration += 1