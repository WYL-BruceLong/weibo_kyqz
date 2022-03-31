# #!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/31 16:55
# @Author : BruceLong
# @FileName: parse_msg_info.py
# @Email   : 18656170559@163.com
# @Software: PyCharm
# @Blog ：http://www.cnblogs.com/yunlongaimeng/
import jionlp as jio

print('111111')
location_text = '抗疫求助#浦东疫情# 【所在城市】上海【居住地址】浦东新区三林镇东明村池河队养鸭滩20号1楼【联系方式】魏女士13761824714【具体描述】由于疫情，家里80多岁的老人独自隔离在上述地址！老人没有手机电话，不识字也不会讲普通话，与家人失联已经三四天了，家人目前不知道老人什么情况，到底是密接还是确诊，更担心老人情绪激动害怕，只希望能和老人通个电话！我们打了各种能求助的热线，也留了联系方式，暂时也没有回复。家里人非常担心和着急，希望能和老人通个电话！万分感谢！！'
print(jio.parse_location(location_text=location_text))
