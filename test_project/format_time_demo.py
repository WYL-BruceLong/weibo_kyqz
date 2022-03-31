# #!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/31 15:59
# @Author : BruceLong
# @FileName: format_time_demo.py
# @Email   : 18656170559@163.com
# @Software: PyCharm
# @Blog ：http://www.cnblogs.com/yunlongaimeng/
from untils.tools import formatting_time

# 月份时间映射字典
month_dict = {
    'Jan ': '01-',
    'Feb ': '02-',
    'Mar ': '03-',
    'Apr ': '04-',
    'May ': '05-',
    'June ': '06-',
    'July ': '07-',
    'Aug ': '08-',
    'Sep ': '09-',
    'Oct ': '10-',
    'Nov ': '11-',
    'Dec ': '12-',
}
ft_time = lambda ttime: formatting_time([ttime.replace(k, v) for k, v in month_dict.items() if k in ttime][0])

print(ft_time('Thu Mar 31 16:17:04 +0800 2022'))
