# #!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/31 20:45
# @Author : BruceLong
# @FileName: map_dict.py
# @Email   : 18656170559@163.com
# @Software: PyCharm
# @Blog ：http://www.cnblogs.com/yunlongaimeng/
category_dict = {
    # 疾病类
    '病人': '疾病',
    '化疗': '疾病',
    '肿瘤': '疾病',
    '癌': '疾病',
    '患者': '疾病',
    '血透': '疾病',
    # 孕妇类
    '产妇': '孕妇',
    '孕妇': '孕妇',
    '怀孕': '孕妇',
    # 物资类
    '奶粉': '物资',
}
# 等级字典
level_dict = {
    '急需': '一级',
    '突然': '一级',
    '救命': '一级',
    '确诊': '二级',
    '阳性': '二级',
    '密接者': '三级',
    '发烧': '三级',
}

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