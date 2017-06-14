#----------------------------------------------------------------------
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloud.settings")
import django
django.setup()
#python外部腳本連接django model---------------------------------------
from img.models import ig_img

import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import shutil
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def little(username):

    driver = webdriver.Chrome(executable_path=r'chromedriver.exe') # chrome瀏覽器
    #driver = webdriver.PhantomJS(executable_path='./phantomjs.exe')  # PhantomJs
    url='https://www.instagram.com'
    driver.get(url+'/'+username)                #要爬的網址
    try:
        #driver.find_element_by_link_text("載入更多內容").click(): #按下"載入更多內容"
        driver.find_element_by_css_selector("._8imhp").click()
        #driver.find_element_by_css_selector("._glz1g").click()
    except:
        print()

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
        print(img['src'])
        urllist.append(img['src'])
    for i in range(1,len(urllist)):  
        is_exist=ig_img.objects.filter(url=urllist[i])
        if not is_exist:
            data=urllist[i]
            name=username
            ig_img.objects.create(username=name,url=data)
        
    driver.close()  # 關閉瀏覽器
    driver.quit()   # 結束全部視窗
def parser(username):
    driver = webdriver.Chrome(executable_path=r'chromedriver.exe') # chrome瀏覽器
    #driver = webdriver.PhantomJS(executable_path='./phantomjs/bin/phantomjs.exe')  # PhantomJs
    url='https://www.instagram.com'
    driver.get(url+'/'+username)                #要爬的網址

    try:
        #driver.find_element_by_link_text("載入更多內容").click() #按下"載入更多內容"
        driver.find_element_by_css_selector("._8imhp").click()
        #driver.find_element_by_css_selector("._glz1g").click()
    except:
        print()

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
    for a in soup.select('._8mlbc'):
        #print(a['href'])
        urllist.append(a['href'])
        driver.get(url+a['href'])
        time.sleep(0.5)
        imgsource=driver.page_source
        s=BeautifulSoup(imgsource,"html.parser")
        imglist=[]
        for img in s.select('._icyx7'):
            urllist.append(img['src'])
            is_exist=ig_img.objects.filter(url=img['src'])
            if not is_exist:
                data=img['src']
                name=username
                ig_img.objects.create(username=name,url=data)
            print(img['src'])
    #return urllist
    driver.close()  # 關閉瀏覽器
    driver.quit()   # 結束全部視窗
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#main
#a=parser('cyc.85')
#print(a)
#parser('cyc.85')
#little('cyc.85')
