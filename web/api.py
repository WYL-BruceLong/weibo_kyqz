# #!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/31 21:18
# @Author : BruceLong
# @FileName: api.py
# @Email   : 18656170559@163.com
# @Software: PyCharm
# @Blog ：http://www.cnblogs.com/yunlongaimeng/
import pymongo
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # 允许跨域的源列表，例如 ["http://www.example.org"] 等等，["*"] 表示允许任何源
    allow_origins=["*"],
    # 跨域请求是否支持 cookie，默认是 False，如果为 True，allow_origins 必须为具体的源，不可以是 ["*"]
    allow_credentials=False,
    # 允许跨域请求的 HTTP 方法列表，默认是 ["GET"]
    allow_methods=["*"],
    # 允许跨域请求的 HTTP 请求头列表，默认是 []，可以使用 ["*"] 表示允许所有的请求头
    # 当然 Accept、Accept-Language、Content-Language 以及 Content-Type 总之被允许的
    allow_headers=["*"],
    # 可以被浏览器访问的响应头, 默认是 []，一般很少指定
    # expose_headers=["*"]
    # 设定浏览器缓存 CORS 响应的最长时间，单位是秒。默认为 600，一般也很少指定
    # max_age=1000
)

mongo_local = pymongo.MongoClient("mongodb://localhost:27017/")
table = mongo_local['weibo_kyqz']['detail_source_data']

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()


@app.get('/')
async def index():
    skip = 0
    limit = 0
    pipeline = [
        # 过滤条件
        # {
        #     "$match": {
        #     }
        # },
        # 映射
        {
            '$sort': {
                'created_at': -1
            }
        },
        {
            "$project": {
                '_id': 0,
                '作者': '$user_name',
                '详情页': '$detail_url',
                '私信作者': '$chat_message_box_url',
                '发布时间': '$created_at',
                '是否有手机号': '$is_phone_number',
                '省': '$province',
                '市': '$city',
                '区': '$county',
                '分类': '$categories',
                '等级': '$level',
            }
        }
        # # 跳过
        # {
        #     "$skip": skip
        # },
        # # 分页
        # {
        #     "$limit": limit
        # }
    ]
    table_data = list(table.aggregate(pipeline=pipeline))
    fields = list(table_data[0].keys())
    thead = '\n'.join([f'<th>{field}</th>' for field in fields])
    tbody = '\n'.join([
        '<tr>' + ''.join([
            f'<th>{data.get(field, "")}</th>'
            for field in fields
        ]) + r'</tr>'
        for data in table_data
    ])
    tb = f'''<thead>
        <tr>
        {thead}
        </tr>
        </thead>
        <tbody>
        {tbody}
        </tbody>'''
    # 处理逻辑
    # 合并
    html_source = html.format(table_content=tb)
    return HTMLResponse(html_source)


if __name__ == '__main__':
    uvicorn.run(app, port=9999, host="0.0.0.0")
