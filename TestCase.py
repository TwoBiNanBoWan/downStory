# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup



'''
下方为获取小说插入两章小说章节，因为章节过多，先确保插入两次小范围通过，如须抓取所有章节，去掉if限制即可
本次脚本参考链接：https://blog.csdn.net/baidu_26678247/article/details/75086587（使用源码阅读）
涉及到相关知识链接：
BeautifulSoup（https://wiki.jikexueyuan.com/project/python-crawler-guide/beautiful-soup.html）
Python I/O文件操作（https://www.runoob.com/python/python-files-io.html）
BeautifulSoup解析器比较（https://blog.csdn.net/Winterto1990/article/details/47806175）
正则表达式（https://www.runoob.com/regexp/regexp-syntax.html）
re（https://blog.csdn.net/zcmlimi/article/details/47709049）
'''


#小说下载函数
#txt_id：小说编号
#txt字典项介绍
#id：小说编号
# title：小说题目
# first_page：第一章页面
# txt_section：章节地址
# section_name：章节名称
# section_text：章节正文
# section_ct：章节页数


#小说获取参数
req_header = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Accept-Encoding": " gzip, deflate",
"Accept-Language": " zh-CN,zh;q=0.9",
"Cache-Control": " no-cache",
"Connection": " keep-alive",
"Cookie: UM_distinctid=178a6e4f76e6a8-03955265887ca9-336d7708-13c680-178a6e4f76f785; __gads=ID=29db6f7d3453d07b-2287395207c700c3:T=1617707727:RT=1617707727": "S=ALNI_Ma8TtV0WzIk4LqOT2f7Wdrbcg7AdA; CNZZDATA1257098929=532664813-1617703372-%7C1617850031",
"Host": " m.rengshu.com",
"Pragma": " no-cache",
"Upgrade-Insecure-Requests": " 1",
"User-Agent": " Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
}
req_url_base = 'http://m.rengshu.com'   #小说主地址

def get_txt(txt_id):
    txt = {}
    txt['title'] = ''
    txt['id'] = str(txt_id)

    #获取小说目录
    res = requests.get(req_url_base + "/book/" + txt['id'] + "/chapter", params=req_header)
    res.encoding = 'gb18030'
    print("小说编号：" + txt['id'])
    soups = BeautifulSoup(res.text, "html.parser")

    #获取小说所有章节信息
    all_page_address = soups.select(".cover .chapter li a")

    #打开本地文件用于存储
    fo = open("/Users/dengyunpeng/Downloads/1.txt", "ab+")

    i = 0
    for one_page_info in all_page_address:
        # 请求当前章节页面  params为请求参数
        r = requests.get(req_url_base + one_page_info['href'], params=req_header)
        r.encoding = 'gb18030'

        # #soup转换
        soup = BeautifulSoup(r.text, "html.parser")
        # print(soup.prettify())

        # 获取章节名称
        section_name = soup.select('#nr_title')[0].text
        fo.write(('\r' + section_name + '\r\n').encode("UTF-8"))
        # 获取章节文本
        section_text = soup.select('#nr #nr1')[0]

        # 按照指定格式替换章节内容，运用正则表达式
        section_text = re.sub('\s+', '\r\n\t', section_text.text).strip('\r\n')
        fo.write((section_text).encode("UTF-8"))

        i = i+1
        if i == 2:
            fo.close()
            break

#小说编号自定义调用
get_txt(3796)







