
import re
import os
import requests
import json

# 下载抖音的用户视频列表


# 用户主页， 获取方法， 点开该用户的右上角三个点->分享->复制链接

user_url = "https://v.douyin.com/e62AuTG"
# user_url = "https://aid.im/OADJ"
tmp_dir = "tmp" # 该文件夹不上传到git

def get_video():
    headers = {
        # 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1'
        'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X; Linux; Android 8.0; Pixel 4 Build/NOBUILD; Nexus 10 Build/N4F26I; Nexus 4 Build/NOBUILD; ${RANDOM_STRING}) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile/14G60 Safari/604.1"
    }
    
    url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid="

    global user_url
    v = re.findall(r'http[s]?://[-.\w]+/[^\s]*', user_url)
    for link in v:
        print(link)
        response = requests.get(link)
        # 获取重定向后地址
        redirect_url = response.url

        # print(redirect_url)
        # 正则匹配规则
        reg = ".*sec_uid=(.*?)&"
        # 获取到sec_uid
        sec_uid = re.match(reg, redirect_url).group(1)
        
        # 拼接最终url
        url += sec_uid
        # 设置一个较大的视频数
        url += "&count=10000"

        # 多次遍历
        for _ in range(100):
            result = requests.get(url, headers)
            json_str = result.text
            print(json_str)
            json_type = json.loads(json_str)
            length = len(json_type["aweme_list"])
            if length != 0:
                print("总共 %d 个" % length)
                i = 1
                # 获取所有视频地址
                for item in json_type["aweme_list"]:
                    # 获取视频博主昵称
                    nickname = item["author"]["nickname"]
                    # 当前视频标题
                    title = item['desc']
                    # 去除windows中不允许的文件名字符
                    forbid = {'\\','/',':','*','?','"','<','>','|','#','$'}
                    for v in forbid:
                        title = title.replace(v, '-')
                    # 无水印视频地址
                    video_url = item["video"]["play_addr"]["url_list"][0]
                    # print(video_url)
                    est = requests.get(url=video_url, headers=headers)
                    # 为该用户创建文件夹
                    global tmp_dir
                    if not os.path.exists(tmp_dir + '/' + nickname):
                        print(tmp_dir + '/' + nickname)
                        os.makedirs(tmp_dir + '/' + nickname)
                        
                    # 保存视频
                    with open(f'{tmp_dir}/{nickname}/{nickname}_{title}.mp4', 'wb') as f:
                        f.write(est.content)
                        print('完成...%d....%s_%s.mp4' % (i, nickname,title))
                        i+=1
                        
                print("已经完成，共 %d 个" % i)
                os._exit(0)
                        

if __name__ == '__main__':
        get_video()
