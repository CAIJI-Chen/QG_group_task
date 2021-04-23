
from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import xlwt
import pymysql





#影片详情链接
findLink = re.compile(r'<a class="" href="(.*?)">')
#影片图片链接
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)  #让换行符包含在字符中
#影片标题
findTitle = re.compile(r'<span class="title">(.*)</span>')
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#影片评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
#影片概述
findInq = re.compile(r'<span class="inq">(.*)</span>')
#影片相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)
#影片简介
findIntro = re.compile(r'<span class="" property="v:summary">(.*?)</span>',re.S)
#class="">(.*?)</span>
def main():
    baesurl = "https://movie.douban.com/top250?start="
    #print(baesurl)
    datalist = getData(baesurl)
    savepath = ".\\豆瓣电影top250.xls"

    #askURL("https://movie.douban.com/top250?start=")
    return datalist




def askURL(url):
    head = {
        #"User-Agent": "Mozilla / 5.0(Windows NT 6.1;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 90.0.4430.85Safari / 537.36"
        "User-Agent": "Mozilla / 5.0(Windows NT 6.1;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 90.0.4430.85Safari / 537.36"
    }

    request = urllib.request.Request(url,headers=head )
    html = ""
    try:

        response = urllib.request.urlopen(request)  #.request
        html = response.read().decode('utf-8')
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html



#爬取网页
def getData(baseurl):
    datalist = []
    for i in range(1,10):     #调用页面信息的函数，10次  可分两次，1-6和6-10
        url = baseurl + str(i*25)
        html = askURL(url)   #保存获取到网页的源码
        #print(html)
        #逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):
            #print(item)      #测试：查看电影item全部信息
            data = []         #保存一部电影的所有信息
            item = str(item)

            link = re.findall(findLink,item)[0]
            data.append(link)                      #添加链接

            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)                    #添加图片

            titles = re.findall(findTitle, item)
            if(len(titles) == 2):
                ctitle = titles[0]                 #中文名
                data.append(ctitle)
                otitle = titles[1].replace("/","")  #外文名 去掉无关的符号"/"
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')                      #外文名留空

            rating = re.findall(findRating, item)[0] #添加评分
            data.append(rating)

            judgeNum = re.findall(findJudge, item)[0] #添加评价人数
            data.append(judgeNum)

            inq = re.findall(findInq, item)        #添加概述
            if len(inq) != 0:
                inq = inq[0].replace("。","")
                data.append(inq)
            else:
                data.append(" ")             #留空

            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)   #去掉<br/>
            bd = re.sub('/'," ",bd)              #替换/
            data.append(bd.strip())           #去掉前后的空格




            html_2 = askURL(data[0])   # 保存获取到网页的源码
            # 解析数据
            soup_2 = BeautifulSoup(html_2, "html.parser")
            #item_2 = soup_2.find_all('div',class_="article")
            item_2 = soup_2.find_all('div',class_="article")
            item_3 = soup_2.find_all('div')
            item_2 = str(item_2)
            infort = re.findall(findIntro, item_2)
            infort = str(infort)
            infort = re.sub('<br(\s+)?/>(\s+)?', " ", infort)  # 去掉<br/>
            infort = re.sub('/', " ", infort)  # 替换/
            infort = infort.strip()
            infort = infort.replace(" ","")

            if(len(infort)==2):
                infort = ' no'
            print(len(infort))
            data.append(infort.strip())  # 去掉前后的空格
            datalist.append(data)  # 把处理好的一部电影信息放入datalist
            #print(html_2)
            #print(data[0])
            #print(item_3)
            #print(item_2)
            #print(infort)
            #print(data)

        #print(datalist)     #测试
#1
    return datalist



if __name__=="__main__":
    datalist = main()

    conn = pymysql.connect(
        host="localhost",          #"localhost"
        port=3306,
        user='root',
        password='1622674681',
        db='test',
        charset='utf8'
    )
    #
    cursor=conn.cursor()
    print(datalist)
    #
    sql = 'insert into douban_2(link,imglilnk,ctitle,otitle,rating,judgeNum,inq,bd,infort) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'

    row = cursor.executemany(sql,datalist)
    print(row)

    conn.commit()

    cursor.close()
    conn.close()
    print(datalist)




