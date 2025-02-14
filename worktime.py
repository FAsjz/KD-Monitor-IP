import datetime


def is_workday_and_time(start_time_str, end_time_str,current_weekday,current_time):
    # 转换工作时间字符串为datetime.time对象
    start_time = datetime.datetime.strptime(start_time_str, "%H:%M").time()
    end_time = datetime.datetime.strptime(end_time_str, "%H:%M").time()


    # 检查是否是工作日（周一至周五）且在工作时间内-更新7天
    if current_weekday < 7 and start_time <= current_time <= end_time:
        return True
    else:
        return False