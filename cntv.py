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
import openpyxl as op # 写入excel表格

def get_goods(driver):
    try:                                             
        goods = driver.find_elements_by_class_name('jvedio')

        video_list = []
        for good in goods:
            detail_url = good.find_element_by_tag_name('a').get_attribute('lanmu1') 
            video_info = {}
            video_info['url'] = detail_url
            video_info.setdefault('name','')
            video_info.setdefault('src','')
            video_info.setdefault('abs','')
            video_list.append(video_info)    
    except Exception:
        pass
    finally:
        return video_list


def get_video_src(video_list,driver):
    for v in video_list:
        driver.get(v['url'])
        try:
            name = driver.find_element_by_class_name('cnt_nav').find_element_by_tag_name('h3').text
            src = driver.find_element_by_tag_name('source').get_attribute('src')
            abstract = driver.find_element_by_class_name('text_box_02').find_element_by_tag_name('p:nth-last-child(1)').text
 
            v['src'] = src.replace('/h5e','')
            v['name'] = name
            v['abs'] = abstract
        except Exception:
            pass


def op_toExcel(data, fileName):      
    wb = op.Workbook()                  # 创建工作簿对象
    ws = wb['Sheet']                     # 创建子表
    ws.append(['NAMBER', 'TITLE', 'URL','SRC','ABS'])     # 添加表头
    for i in range(len(data)):
        d = i+1, data[i]["name"], data[i]["url"], data[i]["src"], data[i]["abs"]
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

    # 爬取福岛核废水有关视频;将正常url中type从web改成video
    keyword='福岛核废水'
    spider(url='https://search.cctv.com/search.php?qtext='+keyword+'&type=video',  fileName='cntv.xlsx')

