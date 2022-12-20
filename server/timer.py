import datetime
import time

from server.util import MyUtil


class MyTimer:
    # 得到13位时间戳
    def getTimer13(time_str: str):
        # 生成13时间戳   eg:1557842280000
        datetime_obj = datetime.datetime.strptime(time_str,
                                                  '%Y-%m-%d %H:%M:%S')
        # 10位,时间点相当于从1.1开始的当年时间编号
        date_stamp = str(int(time.mktime(datetime_obj.timetuple())))
        # 3位,微秒
        data_microsecond = str("%06d" % datetime_obj.microsecond)[0:3]
        date_stamp = date_stamp + data_microsecond
        return int(date_stamp)

    # 等待 N 秒
    def waitTime(duration: int):
        _duration = 0
        while _duration < duration:
            if duration < 60:
                MyUtil.consol('%d 秒后开始...' % (duration - _duration), 1)
            elif duration < 3600:
                MyUtil.consol(
                    '%d 分 %d 秒后开始...' % ((duration - _duration) // 60,
                                         (duration - _duration) % 60), 1)
            else:
                MyUtil.consol(
                    '%d 时 %d 分 %d 秒后开始...' %
                    ((duration - _duration) // 3600,
                     ((duration - _duration) % 3600) // 60,
                     ((duration - _duration) % 3600) % 60), 1)
            time.sleep(1)
            _duration += 1