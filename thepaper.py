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
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)") # 滑到页面底部
        time.sleep(1)                                                          # 加载更多结果
        goods = driver.find_elements_by_class_name('search_res')

        video_list = []
        for good in goods:
            author = good.find_element_by_css_selector('.search_trbs a').text
            if author != 'World湃':
                continue
            detail_url = good.find_element_by_tag_name('a').get_attribute('href')    
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
            name = driver.find_element_by_class_name('video_txt_t').text
            abstract = driver.find_element_by_css_selector('.video_txt_l p').text
            src = driver.find_element_by_tag_name('source').get_attribute('src')
            if '.mp4' in src:
                v['src'] = src
                v['name'] = name
                v['abs'] = abstract
                print(v)
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


def spider(url, keyword,fileName):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(3)  # 使用隐式等待
    try:
        driver.find_element_by_class_name('hdifani').click()
        time.sleep(1)
        input_tag = driver.find_element_by_id('hds_inp')
        input_tag.send_keys(keyword)
        input_tag.send_keys(Keys.ENTER)

        video_list = get_goods(driver)
        get_video_src(video_list,driver)
    finally:
        driver.close()
        op_toExcel(video_list, fileName)



if __name__ == '__main__':
    # 爬取福岛核废水有关视频
    spider(url='https://www.thepaper.cn/', keyword='福岛核废水', fileName='thepaper.xlsx')

