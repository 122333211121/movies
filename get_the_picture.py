import os
import xlrd
import requests

def get_picture(picture_list):
    file_path = './img'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    i = 1
    try:
        for url in picture_list:
            response = requests.get(url)
            img_path = '{}/{}.{}'.format(file_path, str(i), 'jpg')
            if not os.path.exists(img_path):
                with open(img_path, 'wb')as f:
                    f.write(response.content)
                    i += 1
                    print('下载成功')
            else:
                print('已经下载', img_path)
    except requests.ConnectionError:
        print('下载失败')

def main():
    excel = xlrd.open_workbook("豆瓣电影Top250.xls")
    sheet = excel.sheet_by_name("豆瓣电影TOP250")
    picture_list = sheet.col_values(1)
    del (picture_list[0])
    get_picture(picture_list)

if __name__ == '__main__':
    main()

