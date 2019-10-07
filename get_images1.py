__author__ = 'hjl'
'''
需要requests模块的支持，直接使用pip安装即可，命令：pip install requests
'''
import json
import itertools
import urllib
import requests
import os
import re
import sys
 
#############################################################
#word = "郑秀妍"  # 图片搜索的关键字，目前仅支持单个关键词
imageNum = 20  # 下载图片的数目
indexOffset = 0  # 图像命名起始点
#############################################################
 
str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}
 
char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}
 
# str 的translate方法需要用单个字符的十进制unicode编码作为key
# value 中的数字会被当成十进制unicode编码转换成字符
# 也可以直接用字符串作为value
char_table = {ord(key): ord(value) for key, value in char_table.items()}
 
# 解码图片URL
def decode(url):
    # 先替换字符串
    for key, value in str_table.items():
        url = url.replace(key, value)
    # 再替换剩下的字符
    return url.translate(char_table)
 
 
# 生成网址列表
def buildUrls(word):
    word = urllib.parse.quote(word)
    url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
    urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))
    return urls
 
# 解析JSON获取图片URL
re_url = re.compile(r'"objURL":"(.*?)"')
 
 
def resolveImgUrl(html):
    imgUrls = [decode(x) for x in re_url.findall(html)]
    return imgUrls
 
 
def downImg(imgUrl, dirpath, imgName):
    filename = os.path.join(dirpath, imgName)
    try:
        res = requests.get(imgUrl, timeout=15)
        if str(res.status_code)[0] == "4":
            print(str(res.status_code), ":", imgUrl)
            return False
    except Exception as e:
        print("抛出异常：", imgUrl)
        print(e)
        return False
    with open(filename, "wb") as f:
        f.write(res.content)
    return True
 
 
def mkDir(dirName):
    dirpath = os.path.join(sys.path[0], dirName)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    return dirpath
 

def dowmloadPic(txt):
    f = open(txt, "r")
    names = []
   

    # if no label is provided just read input file names
    print("reading names form the file ")
    for line in f:
        tokens = line.split()
        for i in range(len(tokens)):
            names.append(tokens[i]) 
    return  names
def download(txt):
    
    words=dowmloadPic(txt)
    for i in range(len(words)):
        print("=" * 50)
        # word = input("请输入你要下载的图片关键词：\n")
        saveImagePath ="/home/power/桌面/hjl/数据集百度抓取/%s"%words[i]
        dirpath = mkDir(saveImagePath)
    
        urls = buildUrls(words[i])
        index = 0
        for url in urls:
            print("正在请求：", url)
            try:            
                html = requests.get(url, timeout=1).content.decode('utf-8')
                imgUrls = resolveImgUrl(html)
            except:
                print('【错误】当前图片无法下载')
                continue
            if len(imgUrls) == 0:  # 没有图片则结束
                break
            for url in imgUrls:
                if downImg(url, dirpath, str(index + indexOffset) + ".jpg"):
                    index += 1
                    print("正在下载第 %s 张" % (index + indexOffset))
                    if index == imageNum:
                        break
            if index == imageNum:
                print("下载完成\n下载结果保存在脚本目录下的文件夹中，文件名字：" + saveImagePath)
                break
            
if __name__ == '__main__':
    download("/home/power/桌面/hjl/数据集百度抓取/people.txt")
