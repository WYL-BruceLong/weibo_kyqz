# #!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/31 16:05
# @Author : BruceLong
# @FileName: tools.py
# @Email   : 18656170559@163.com
# @Software: PyCharm
# @Blog ：http://www.cnblogs.com/yunlongaimeng/
# -*- coding: utf-8 -*-
import datetime
import re


# 二、数据过滤
# 通用文本过滤
def universal_filter(text):
    if text:
        # \u1234
        text = text.replace(u'\u200b', '')
        text = text.replace(u'\u2002', '')
        text = text.replace(u'\u3000', '')
        text = text.replace(u'\ufeff', '')
        # \x??
        text = text.replace(u'\xa0', '')
        text = text.replace(u'\x7f', '')
        # &??
        text = text.replace('&nbsp', ' ')
        text = text.replace('&ldquo;', '"')
        text = text.replace('&rdquo;', '"')
        text = text.replace('&bull;', '•')
        text = text.replace('&mdash;', '—')
        text = text.replace('&lsquo;', "'")
        text = text.replace('&rsquo;', "'")
        text = text.replace('&hellip;', '…')
        text = text.replace('&middot;', '·')
        text = text.replace('&quot;', '"')
        text = text.replace('&amp;', '&')
        text = text.replace('&#39;', "'")
        text = text.replace('&deg;', "°")
        text = text.replace('&times;', "×")
        text = text.replace('&beta;', "β")
        text = text.replace('&ndash;', "–")
        # \n, \r, \t
        # text = text.replace('\n', '')
        text = text.replace('\r', '')
        text = text.replace('\t', '')
        # '  ?  '
        text = text.strip()
    return text


# 发布时间过滤
def release_time_filter(text):
    if text:
        text = universal_filter(text)
    return formatting_time(text)


# 格式化时间为'yyyy-mm-dd hh:mm:ss'
def formatting_time(my_time):
    if my_time:

        # 保留数字, '-', ':'
        re_time = r'[^\d\-\:\：]'
        # 匹配数字间的空格, '-', ':', '：'
        re_inter_betw_ymdhms = r'[\-\:\：\s]+'
        # re_inter_betw_hms = r'[\:\：\s]+'
        # 匹配头尾的空格, '-', ':', '：'
        re_head_and_tail_symbol = '[\-\:\：\s]*'
        # 匹配年月日
        re_year = r'^' + re_head_and_tail_symbol + r'(\d{4}' + re_inter_betw_ymdhms + ')'
        re_month = re_head_and_tail_symbol + r'(1[012]' + re_inter_betw_ymdhms + r'|0?[1-9]' + re_inter_betw_ymdhms + ')'
        re_day = r'3[01]|[12]\d|0?[1-9]'
        re_day = r'(' + re_day + r'\s|' + re_day + '$)'
        # 匹配时分秒
        re_hour = r'(2[0-3]' + re_inter_betw_ymdhms + r'|[01]?\d' + re_inter_betw_ymdhms + ')'
        re_minute = r'[0-5]?\d'
        re_minute = r'(' + re_minute + re_head_and_tail_symbol + r'$|' + re_minute + re_inter_betw_ymdhms + ')'
        re_second = r'([0-5]?\d)' + re_head_and_tail_symbol + r'$'

        my_time = re.sub(re_time, ' ', my_time).strip()
        my_time = ' '.join(my_time.split())
        y_m_d_h_m_s = re.findall(re_year + re_month + re_day + re_hour + re_minute + re_second, my_time)
        if y_m_d_h_m_s:
            year, month, day, hour, minute, second = y_m_d_h_m_s[0]
        else:
            re_month = r'^' + re_month
            re_second = r'^' + re_second

            second = ''

            _year = re.findall(re_year, my_time)
            year = _year[0] if _year else str(datetime.datetime.now().year)
            my_time = re.sub(re_year, '', my_time).strip()

            m_d_h_m = re.findall(re_month + re_day + re_hour + re_minute, my_time)
            if m_d_h_m:
                month, day, hour, minute = m_d_h_m[0]
                my_time = re.sub(re_month + re_day + re_hour + re_minute, '', my_time).strip()
            else:
                re_day = r'^' + re_day
                re_hour = r'^' + re_hour
                re_minute = r'^' + re_minute

                _month = re.findall(re_month, my_time)
                month = "".join(_month[0]) if _month else '01'
                my_time = re.sub(re_month, '', my_time).strip()

                _day = re.findall(re_day, my_time)
                day = "".join(_day[0]) if _day else '01'
                my_time = re.sub(re_day, '', my_time).strip()

                _hour = re.findall(re_hour, my_time)
                hour = "".join(_hour[0]) if _hour else '00'
                my_time = re.sub(re_hour, '', my_time).strip()

                _minute = re.findall(re_minute, my_time)
                minute = "".join(_minute[0]) if _minute else '00'
                my_time = re.sub(re_minute, '', my_time).strip()

            if not second:
                _second = re.findall(re_second, my_time)
                second = "".join(_second[0]) if _second else '00'

        year = auto_add_0(year)
        month = auto_add_0(month)
        day = auto_add_0(day)
        hour = auto_add_0(hour)
        minute = auto_add_0(minute)
        second = auto_add_0(second)

        my_time = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second

        my_datetime = datetime.datetime.strptime(my_time, "%Y-%m-%d %H:%M:%S")
        if (my_datetime - datetime.datetime.now()) > datetime.timedelta(seconds=0):
            year = int(year) - 1
            my_time = str(year) + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second

    return my_time


# 年月日时分秒自动补0
# ValueError: invalid literal for int() with base 10: ''
def auto_add_0(text):
    if text:
        text = str(text)
        # little error
        text = int(re.sub(r'^0|[\s\-\:\：]', '', text))
        if text < 10:
            text = '0' + str(text)
        else:
            text = str(text)
    return str(text)
