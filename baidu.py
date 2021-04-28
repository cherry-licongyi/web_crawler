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

def get_video(driver):
    try:
        goods = driver.find_elements_by_class_name('result')
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


def get_video_src(video_list,driver):
    for v in video_list:
        driver.get(v['url'])
        try:
            src = driver.find_element_by_tag_name('video').get_attribute('src')
            if '.mp4' in src:
                v['src'] = src
        except Exception:
            pass


def op_toExcel(data, fileName):      
    wb = op.Workbook()                  # 创建工作簿对象
    ws = wb['Sheet']                     # 创建子表
    ws.append(['NAMBER', 'TITLE', 'URL','SRC'])     # 添加表头
    for i in range(len(data)):
        d = i+1, data[i]["name"], data[i]["url"], data[i]["src"]
        ws.append(d)            # 每次写入一行
    wb.save(fileName)


def spider(url,fileName):
    driver = webdriver.Chrome()     # chrome webdriver插件
    driver.get(url)
    driver.implicitly_wait(3)        # 使用隐式等待
    try:
        video_list = get_video(driver)
        get_video_src(video_list,driver)
    finally:
        driver.close()
        op_toExcel(video_list,fileName)  # openpyxl库储存数据到excel


if __name__ == '__main__':
    # 爬取福岛核废水有关视频
    keyword = '福岛核废水'
    spider('http://v.baidu.com/v?word='+keyword+'&c','baidu.xlsx')