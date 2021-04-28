# -*- coding: utf-8 -*-
#!/usr/bin/env Python 3.8.5
# Author: cherry-licongyi
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys  # 键盘按键操作
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
import time
import requests
import re
import openpyxl as op # 写入excel表格


def get_video(driver):
    try:
        goods = driver.find_elements_by_class_name('news-stream-newsStream-news-item-infor')
  
        video_list = []
        for good in goods:
            video_info = {}
            detail_url = good.find_element_by_tag_name('a').get_attribute('href')
            p_name = good.find_element_by_tag_name('a').get_attribute('title')
                        
            p_name = p_name.replace('<em>','')
            p_name = p_name.replace('</em>','')
            video_info['name'] = p_name
            video_info['url'] = detail_url
            video_info['src'] = ''
        
            video_list.append(video_info)

    except Exception:
        pass
    finally:
        return video_list


def get_video_src(video_list):
    # 请求头信息
    myheader = {'User-Agent':'Mozila/5.0 (Windows NT 10.0;WOW64) AppleWebKit/537.36(KHTML,like Gecko) Chrome/83.0.4103.61 Safari/537.36'}

    #获取单元格值：
    for v in video_list: 
        url_ = v['url']
        response = requests.get(url=url_,headers=myheader)
        if response.status_code == 200:        
            try:
                video_url = re.findall('https://ips.ifeng.com/video19.ifeng.com/.+mp4',response.text)[0]            
                v['src'] = video_url
            except Exception:
                pass
           
def op_toExcel(data, fileName):      # openpyxl库储存数据到excel
    wb = op.Workbook()                  # 创建工作簿对象
    ws = wb['Sheet']                     # 创建子表
    ws.append(['NAMBER', 'TITLE', 'URL','SRC'])     # 添加表头
    for i in range(len(data)):
        d = i+1, data[i]["name"], data[i]["url"], data[i]['src']
        ws.append(d)            # 每次写入一行
    wb.save(fileName)


def spider(url,fileName):
    driver = webdriver.Chrome()     # chrome webdriver插件
    driver.get(url)
    driver.implicitly_wait(3)        # 使用隐式等待
    try:
        video_list = get_video(driver)        
    finally:
        driver.close()
        get_video_src(video_list)        
        op_toExcel(video_list,fileName)
        

if __name__ == '__main__':
    # 爬取福岛核废水有关视频
    keyword='福岛核废水'
    spider('https://so.ifeng.com/?q='+keyword+'&c=1','ifeng.xlsx')



