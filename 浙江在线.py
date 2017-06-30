# -*- coding: utf-8 -*-
"""

@author: PC
"""
import  requests
from lxml import etree
import  os
os.chdir('F:/python/pachong/pc/zjzx')

#获取主url列表,num为页数
def get_base_url(num):
    bash_url_list1=['http://js.zjol.com.cn/ycxw_zxtf/index.shtml']
    bash_url_list2=['http://js.zjol.com.cn/ycxw_zxtf/index_'+str(i)+'.shtml' for i in range(1,num)]
    bash_url_list1.extend(bash_url_list2)
    return  bash_url_list1

#解析每个url
def get_url_html(url):
    headers = {
        'host': "s.zjol.com.cn",
        'connection': "keep-alive",
        'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
        'accept': "image/webp,image/*,*/*;q=0.8",
        'referer': "http://s.zjol.com.cn/cse/search?s=6048247431686495421&loc=http%3A%2F%2Fjs.zjol.com.cn%2Fycxw_zxtf%2F201706%2Ft20170628_4445807.shtml&width=650&rec=1&wt=1&ht=3&pn=3&qfrom=3&q=%20%E7%96%BC%E7%97%9B",
        'accept-encoding': "gzip, deflate, sdch",
        'accept-language': "zh-CN,zh;q=0.8",
        'cookie': "_trs_uv=dvih_1_j459yi1s; Hm_lvt_419cfa1cc17e2e1dc6d4f431f8d19872=1497945305,1498616362; Hm_lpvt_419cfa1cc17e2e1dc6d4f431f8d19872=1498632846",
        'cache-control': "no-cache",
        'postman-token': "ccb308e6-edb7-cfec-3e91-af4eed43ae1a"
    }

    response = requests.request("GET", url, headers=headers)
    html = etree.HTML(response.content)
    # result = etree.tostring(html)  显示解析后的html
    return  html

#获取每个主url的页面元素,主要是它的子url
def get_child_url(html):
    child_url_list=html.xpath('//ul[@class ="listUl"]//li/a/@href')
    return  child_url_list

##获取每个子url的页面元素
def get_child_text(html):
    child_html=get_url_html(url) #子页面解析
    title=html.xpath('//title')[0].text #标题
    time=html.xpath('//*[@id="pubtime_baidu"]/text()')[1]   #时间
    paragraph= html.xpath('//div[@class ="contTxt"]/p')     #段落
    contxt=''
    for p in paragraph:
        if type(p.text) == unicode:
            contxt += p.text
        else:
            continue
    filename=title+'.txt'
    with open(filename,'wb') as f:
        f.write((title+'\r\n'+time+'\r\n'+contxt).encode('utf-8'))

if __name__ == '__main__':
    bash_url=get_base_url(50)  #取50页
    for url in bash_url:
        child_url=get_child_url(get_url_html(url))
        for c_url in child_url:
            get_child_text(get_url_html(c_url))



