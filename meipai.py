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
import re
import openpyxl as op # 写入excel表格

def get_goods(driver):
    try:
        # time.sleep(1)
        goods = driver.find_elements_by_tag_name('li')
        
        video_list = []
        for good in goods: 
            detail = good.find_elements_by_css_selector('a[href][target="_blank"][class="content-l-p pa"]')
            if len(detail) == 0:
                break
            d = detail[0]     
            detail_url = d.get_attribute('href')
             # 去掉标题上的链接 和 换行符
            title = d.get_attribute('title').replace('\n', '')
            title = title.replace('https://h5.meipai.com/emotion/7?source=1021','')
               
            video_info = {}
            video_info['url'] = detail_url
            video_info['name'] = title
            video_info.setdefault('src','')
            video_info.setdefault('nums','')

            # print(video_info)
            video_list.append(video_info)        
    except Exception:
        pass
    finally:
        return video_list


def get_video_src(video_list,driver):
    for v in video_list:
        driver.get(v['url'])
        try:
            src = driver.find_element_by_tag_name('video').get_attribute('src')
            playnums = driver.find_element_by_class_name('detail-location').text
           
            v['src'] = src
            v['nums'] = playnums

        except Exception:
            pass


def op_toExcel(data, fileName):      
    wb = op.Workbook()                  # 创建工作簿对象
    ws = wb['Sheet']                     # 创建子表
    ws.append(['NAMBER', 'TITLE', 'URL','SRC','PLAYNUMS'])     # 添加表头
    for i in range(len(data)):
        d = i+1, data[i]["name"], data[i]["url"], data[i]["src"], data[i]["nums"]
        ws.append(d)            # 每次写入一行
    wb.save(fileName)


def spider(url, fileName):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(3)  # 使用隐式等待
    try:
        video_list = get_goods(driver)
        get_video_src(video_list,driver)
    finally:
        driver.close()
        op_toExcel(video_list, fileName)



if __name__ == '__main__':
    # 爬取有关视频
    keyword='赵丽颖冯绍峰离婚'
    spider(url='https://www.meipai.com/topic/'+keyword, fileName='meipai.xlsx')

