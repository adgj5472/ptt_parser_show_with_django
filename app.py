
#----------------------------------------------------------------------
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloud.settings")
import django
django.setup()
#python外部腳本連接django model---------------------------------------
from img.models import img,ig_img
import json
import time
import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import schedule
import download_beauty

from new_ig_parser import little,parser

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
rs = requests.session()

#--------------------  I G  --------------------------------
from selenium import webdriver
import shutil
import sqlite3

#-------------------------------------------
def little(username):
    username=username[0]
    print(username)
    
    
    #driver = webdriver.PhantomJS(executable_path='./phantomjs.exe')  # PhantomJs
    url='https://www.instagram.com'
    driver.get(url+'/'+username)                #要爬的網址
    try:
        #driver.find_element_by_link_text("載入更多內容").click(): #按下"載入更多內容"
        driver.find_element_by_css_selector("._8imhp").click()
        #driver.find_element_by_css_selector("._glz1g").click()
    except:
        time.sleep(0.5)

    while(True):
        old=driver.execute_script('return document.body.scrollHeight;')         #原本網頁頁面高度
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  # 重複往下捲動
        time.sleep(0.8)
        new=driver.execute_script('return document.body.scrollHeight;')         #新的網頁頁面高度
        if(old==new):   	                                                    #判斷式成立為已到頁面底部
            break

    urllist=[]
    pageSource = driver.page_source  # 取得網頁原始碼
    soup=BeautifulSoup(pageSource,"html.parser")

    for img in soup.select('img'):
        #print(img['src'])
        urllist.append(img['src'])
    for i in range(1,len(urllist)):
        is_exist=ig_img.objects.filter(url=urllist[i])
        if is_exist:
            print('a')
            break
        if not is_exist:
            data=urllist[i]
            name=username
            ig_img.objects.create(username=name,url=data)




def get_page_number(content):
    start_index = content.find('index')
    end_index = content.find('.html')
    page_number = content[start_index + 5: end_index]
    return int(page_number) + 1


def over18(board):
    res = rs.get('https://www.ptt.cc/bbs/{}/index.html'.format(board), verify=False)
    # 先檢查網址是否包含'over18'字串 ,如有則為18禁網站
    if 'over18' in res.url:
        print("18禁網頁")
        load = {
            'from': '/bbs/{}/index.html'.format(board),
            'yes': 'yes'
        }
        res = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=load)
    return BeautifulSoup(res.text, 'html.parser')


def craw_page(res, push_rate):
    soup_ = BeautifulSoup(res.text, 'html.parser')
    article_seq = []
    for r_ent in soup_.find_all(class_="r-ent"):
        try:
            # 先得到每篇文章的篇url
            link = r_ent.find('a')['href']
            if link:
                # 確定得到url再去抓 標題 以及 推文數
                title = r_ent.find(class_="title").text.strip()
                rate_text = r_ent.find(class_="nrec").text
                url = 'https://www.ptt.cc' + link
                if rate_text:
                    if rate_text.startswith('爆'):
                        rate = 100
                    elif rate_text.startswith('X'):
                        rate = -1 * int(rate_text[1])
                    else:
                        rate = rate_text
                else:
                    rate = 0
                # 比對推文數
                if int(rate) >= push_rate:
                    article_seq.append({
                        'title': title,
                        'url': url,
                        'rate': rate,
                    })
        except Exception as e:
            print('本文已被刪除', e)
    return article_seq

def write_ig_db():
    global driver
    driver = webdriver.Chrome(executable_path=r'chromedriver.exe') # chrome瀏覽器
    conn=sqlite3.connect('db.sqlite3')
    cursor=conn.cursor()
    cursor.execute('select distinct username from img_ig_img')
    values= cursor.fetchall()
    print(values)
    for user in values:
        little(user)
        
    driver.close()  # 關閉瀏覽器
    driver.quit()   # 結束全部視窗
    del driver

    
def write_db(images):
    for image in images:
        is_exist=img.objects.filter(photo=image)
        #print(is_exist)
        if not is_exist:
            data=image
            name="未設定"
            img.objects.create(title=name,photo=data)

def main(crawler_pages=2):
    #engine, session = connect_db(DB_connect)
    # python beauty_spider2.py [版名]  [爬幾頁] [推文多少以上]
    board, page_term, push_rate = 'beauty', crawler_pages, 10
    start_time = time.time()
    print('start_time:%d' %(start_time))
    soup = over18(board)
    all_page_url = soup.select('.btn.wide')[1]['href']
    start_page = get_page_number(all_page_url)

    print("Analytical download page...")
    index_list = []
    article_list = []
    for page in range(start_page, start_page - page_term, -1):
        page_url = 'https://www.ptt.cc/bbs/{}/index{}.html'.format(board, page)
        index_list.append(page_url)

    # 抓取 文章標題 網址 推文數
    while index_list:
        
        index = index_list.pop(0)
        res = rs.get(index, verify=False)
        # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
        if res.status_code != 200:
            index_list.append(index)
            time.sleep(1)
        else:
            article_list += craw_page(res, push_rate)
        time.sleep(0.05)
    
    print(article_list[0]['title'])
    
    total = len(article_list)
    #print(article_list)
    count = 0
    image_seq = []
    title_seq = []
    # 進入每篇文章分析內容
    while article_list:
        article = article_list.pop(0)
        res = rs.get(article['url'], verify=False)
        # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
        if res.status_code != 200:
            article_list.append(article)
            time.sleep(1)
        else:
            count += 1
            image_seq += download_beauty.store_pic(article['url'])
            title_seq.append(article['title'])
            #print(title_seq)
            #print('image_seq')
            #print(image_seq)
            write_db(image_seq)
            print('download: {:.2%}'.format(count / total))
        time.sleep(0.05)
    #print(title_seq)
    #print(image_seq)
    write_ig_db()    #IG 爬蟲

    print("下載完畢...")
    print('execution time: {:.3}s'.format(time.time() - start_time))


if __name__ == '__main__':
    print('main')
    main()
#    schedule.every(30).minutes.do(main)
#    while True:
#        print('wating......')
#        schedule.run_pending()
#        time.sleep(1)
