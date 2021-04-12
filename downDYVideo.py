import requests
import json
from urllib import parse
# 抖音视频的URL : Request URL:
url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=MS4wLjABAAAA0NL6UPqIabTDseE8xmFLBQPQBfdIYAF2qyWT9M2N-SHwOr5Jo9D_0BJsYfSQnAVH&count=21&max_cursor=0&aid=1128&_signature=R6Ub1QAAJ-gQklOOeJfpTEelG8&dytk="

headers = {
    'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
}
# 调用requests中的get获取抖音作者主页的网页链接
resp = requests.get(url=url, headers=headers, stream=True)
# 输出访问状态，如为<200>即为访问成功
print("初始访问状态:", resp)
# 使用json解析获取的网页内容
data_json = json.loads(resp.text)
# 使用json解析网页后，data_json的内容为dict格式，我们可以通过以下方式查看健名
print(data_json.keys())

has_more = data_json['has_more']
max_cursor = data_json['max_cursor']

# 接下来使用循环来解决我们之前所提到的“隐藏内容”问题
# 判断hasmore是否为true，如果为真则还有隐藏的内容，如果要继续显示剩下的内容
# name需要根据max_cursor 这个字段来进行分页读取
# url上次返回的结果中的max_cursor 就是下一次url需要替换的分页数
while has_more == True:
    print('has_more:', has_more)
    url_parsed = parse.urlparse(url)  # 打散url连接
    bits = list(url_parsed)  # 将url连接区分开来
    # ['https', 'www.iesdouyin.com', '/web/api/v2/aweme/post/', '', 'sec_uid=MS4wLjABA
    # AAA0NL6UPqIabTDseE8xmFLBQPQBfdIYAF2qyWT9M2N-SHwOr5Jo9D_0BJsYfSQnAVH&count=21&max
    # _cursor=0&aid=1128&_signature=R6Ub1QAAJ-gQklOOeJfpTEelG8&dytk=', '']
    qs = parse.parse_qs(bits[4])  # 选择第四个元素
    
    # {'sec_uid': ['MS4wLjABAAAA0NL6UPqIabTDseE8xmFLBQPQBfdIYAF2qyWT9M2N-SHwOr5Jo9D_0B
    # JsYfSQnAVH'], 'count': ['21'], 'max_cursor': ['0'], 'aid': ['1128'], '_signature
    # ': ['R6Ub1QAAJ-gQklOOeJfpTEelG8']}
    qs['max_cursor'] = max_cursor  # 替换掉这个字段的值
    bits[4] = parse.urlencode(qs, True)  # 将替换的字段拼接起来,并且url拼接时不转义
    url_new = parse.urlunparse(bits)  # 重新拼接整个url

    # 只要hasmore是否为true，则反复访问作者主页链接，直到成功返回这个为false
    r = requests.get(url=url_new, headers=headers, stream=True)
    data_json = json.loads(resp.text)
    has_more = data_json['has_more']  # 重置hasmore直到返回为false则退出循环
    max_cursor = data_json['max_cursor']  # 每次重置这个页数，继续替换url中下一页页码进行访问
    # print('has_more22:',has_more)
    print('maxcursor22:', max_cursor)
    # print('has_more22:',len(data_json['aweme_list']))
    # for i in range(len(data_json['aweme_list'])):
    #     print(data_json['aweme_list'][i]['video']['play_addr_lowbr']['url_list'][0])

# 我们要保存视频文件的主要路径
    path = "/tmp/dy/"
    for i in range(len(data_json['aweme_list'])):
        # url_1为我们获取的视频链接
        url_1 = data_json['aweme_list'][i]['video']['play_addr_lowbr']['url_list'][0]
        # t为我们获取的视频标题
        t = data_json['aweme_list'][i]['desc']
        # requests发送浏览器发送get请求，得到数据
        r = requests.get(url=url_1, headers=headers, stream=True)
        # path_1为完整文件保存路径
        path_1 = path+t+'.mp4'
        # 保存抖音视频mp4格式，二进制读取
        with open(path_1, "wb") as f:
            # 先定义初始进度为0
            write_all = 0
            for chunk in resp.iter_content(chunk_size=1000000):
                write_all += xh.write(chunk)
                # 打印下载进度
                print("下载进度：%02.6f%%" % (100 * write_all / reponse_body_lenth))
