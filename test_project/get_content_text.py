# #!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/31 15:21
# @Author : BruceLong
# @FileName: get_content_text.py
# @Email   : 18656170559@163.com
# @Software: PyCharm
# @Blog ：http://www.cnblogs.com/yunlongaimeng/
from scrapy import Selector

text = '''<a  href="https://m.weibo.cn/p/index?extparam=%E6%8A%97%E7%96%AB%E6%B1%82%E5%8A%A9&containerid=10080889902a1e60cd81187b008223d86da809" data-hide=""><span class='url-icon'><img style='width: 1rem;height: 1rem' src='https://n.sinaimg.cn/photo/5213b46e/20180926/timeline_card_small_super_default.png'></span><span class="surl-text">抗疫求助</span></a><span class="url-icon"><img alt=[悲伤] src="https://h5.sinaimg.cn/m/emoticon/icon/default/d_beishang-c95268c034.png" style="width:1em; height:1em;" /></span><span class="url-icon"><img alt=[悲伤] src="https://h5.sinaimg.cn/m/emoticon/icon/default/d_beishang-c95268c034.png" style="width:1em; height:1em;" /></span><span class="url-icon"><img alt=[悲伤] src="https://h5.sinaimg.cn/m/emoticon/icon/default/d_beishang-c95268c034.png" style="width:1em; height:1em;" /></span>求助🆘🆘🆘上海市东海老年护理医院，96岁外婆瘫痪在床无人照料！！！<br />护理院在疫情爆发之后就不让家属进入探望了，只能通过护工阿姨了解外婆的大致情况。96岁的外婆已经没有自理能力了，耳朵听不见，眼睛看不清，每天吃的食物都要靠阿姨用料理机打碎喂食。但是两天前护工阿姨检测出阳性，被带去了世博方舱。之后我们了解到，护理院内现在的情况可怕到令人窒息，疫情如此严重的情况下，阳性病人与阴性病人完全不隔离，连身穿防护服的护工和护士医生都被传染了，让毫无防疫措施的老人们怎么办。老人们的核酸检测已经五六天没做了，外婆现在到底有没有阳性我们也不知道。由于院内疫情泛滥严重，一半以上的医生护士和护工都被带出去隔离了，在我外婆的病区只有一个护士一个医生，那么多需要照顾的老人怎么办！我们现在不知道外婆是否已经被感染了新冠，也不知道如此混乱的情况下外婆是否能够得到医疗及生活照顾，甚至是正常的吃饭还能否保证。在外面的我们家属每天担心焦虑夜不能寐，但是身在护理院的外婆她的恐惧害怕我们根本无法想象。 '''
selector = Selector(text=text)
print(''.join(Selector(text=text).xpath('//text()').extract()))
