## README

#### 文件目录

1. ##### 代码文件

以下每个代码文件对应自动爬取相应网站的相应话题视频，并获取视频信息存到对应创建的excel表格中

`ifeng.py`
`baidu.py`
`thepaper.py`
`haokan.py`
`meipai.py`
`cntv.py`

2. ##### 表格文件

一下每个文件对应存储相应网站爬取到的视频信息，如视频标题，源url，播放量，简介等，视具体网站会有不同

`ifeng.xlsx`
`baidu.xlsx`
`thepaper.xlsx`
`haokan.xlsx`
`meipai.xlsx`
`cntv.xlsx`

3. ##### 视频自动下载代码

以下文件实现从以上目录中excel表格读取每个网站视频源url，创建网站文件夹，每个网站下载3个视频到对应文件夹中，(除了cntv)

`video_download.py`



#### 运行说明

先依次运行1.中的所有程序，然后运行3.中的程序