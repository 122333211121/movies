import re
import urllib.error
import urllib.request
import xlwt
from bs4 import BeautifulSoup
from Proxy_pool.proxydb import RedisClient

def get_the_proxy():
    x = RedisClient()
    proxy = x.random()
    return proxy

def askURL(url, proxy):
    headers = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 84.0.4147.89Safari / 537.36"
    }
    proxy = urllib.request.ProxyHandler({'http': proxy,
                                         'https': proxy})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    request = urllib.request.Request(url, headers=headers)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")

    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
            proxy = get_the_proxy()
            askURL(url, proxy)
        if hasattr(e, "reason"):
            print(e.reason)
            proxy = get_the_proxy()
            askURL(url, proxy)
    return html


def getData(baseurl):
    datalist = []
    findlink = re.compile(r'<a href="(.*?)">')  # 影片详情链接
    findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # 让换行符包含在字符中 #影片图片链接
    findtitle = re.compile(r'<span class="title">(.*?)</span>')  # 影片片名
    findBd = re.compile(r'<p class="">(.*?)</p>', re.S)
    for i in range(0, 1):
        url = baseurl + str(i * 25)
        proxy = get_the_proxy()
        html = askURL(url, proxy)
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):
            data = []
            item = str(item)

            link = re.findall(findlink, item)[0]
            data.append(link)
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)
            titles = re.findall(findtitle, item)
            if len(titles) == 2:
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/", "")
                otitle = otitle.replace(' ', '')
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append('')

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)
            bd = re.sub('/', " ", bd)
            data.append(bd.strip())
            datalist.append(data)
        print(datalist)
        return datalist



def saveData(datalist, savepath):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('豆瓣电影TOP250', cell_overwrite_ok=True)
    col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "相关信息")
    for i in range(0, 5):
        sheet.write(0, i, col[i])
    for i in range(0, 250):
        data = datalist[i]
        for j in range(0, 5):
            sheet.write(i + 1, j, data[j])

    book.save(savepath)


def main():
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getData(baseurl)
    savepath = "豆瓣电影Top250.xls"
    saveData(datalist, savepath)

if __name__ == '__main__':
    main()
