import re
import time
from datetime import datetime




def validate_and_match_datetime(text):
    '''验证日期+时间格式+正则表达式提取文本所有日期+时间
        :param text: 待检索文本
    '''
    pattern = r'(\d{4}-\d{1,2}-\d{1,2}T\d{1,2}:\d{1,2}:\d{1,2})'
    pattern = re.compile(pattern)
    result = pattern.findall(text)
    try:
        if result[0] != datetime.strptime(result[0], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S'):
            raise ValueError
        return result[0].replace('T', " ")
    except ValueError:
        return False


def calculate_days(loginTime):
    loginTime = validate_and_match_datetime(loginTime)
    loginTime = datetime.strptime(loginTime, '%Y-%m-%d %H:%M:%S')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # str
    current_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')  # datetime
    days = (current_time - loginTime).days
    return days  # int


if __name__ == '__main__':
    text = '2020-02-18T01:00:34.240Z'
    print(type(text))
    date = validate_and_match_datetime(text)
    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    print('date:', date)
    print('date_type:', type(date))
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_time = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
    #
    # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("current_time:", current_time)
    print("current_time_type:", type(current_time))
    if current_time >= date:
        print('hah')
    #
    # date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    # current_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
    #
    # active_date = (current_time - date).days












