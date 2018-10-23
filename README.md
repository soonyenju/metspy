# Python metspy教程
Version: 0.1.10

Author: soonyenju@foxmail.com

License: MIT

## 简介

metspy是一个可以爬取全球环境参数（AQI），包括PM2.5、NO2等，以及气象参数的Python包。
metspy基于Python3，依赖项包括：
* socket
* datetime
* pathlib
* bs4
* requests
* pickle
* pandas
* urllib
* time

#### metspy由5个子模块组成：
* config: 基础配置模块，伪装成浏览器进行数据爬取。如设置headers、设置socket连接时间。
* initializer: 
* 1. 初始化目标路径的dict，key为各个国家，value为各国对应的url。
* 2. 若路径存在，则加载对应pkl文件。
* 3. 将用户自定义下载路径的txt文件转换为所需的pkl格式。
* spyder: 爬虫蜘蛛，最核心的模块。可选择用户自定义爬取模式或默认爬取模式进行；默认爬取模式还可以选择国家。
* processor: 将爬取的records按站点保存成csv文件
* dispatcher: 调度模块，也是所有程序的入口。主要功能：
* 1. 监听，从定义的时间开始到整点进行爬取
* 2. 选择用户自定义模式或默认模式
* 3. 结合调度其它模块，完成爬取。

#### 开始

* 模块安装：在终端键入：
```
pip install metspy
```
* 简易运行
1. 默认模式：自动爬取全球各个站点的数据，如果设置country_name参数则爬取指定国家。设置的运行小时为当日24小时制对应值的字符串。
```
from metspy.dispatcher import Dispatcher

def main():
	disp = Dispatcher(start_hour = "13")
	disp.deft_run(country_name = "China")

if __name__ == '__main__':
	main()

```
2. 用户自定义模式：./static/user_url.txt中添加目标站点url，以回车间隔。该文件在初始化中自动生成。
```
from metspy.dispatcher import Dispatcher

def main():
	disp = Dispatcher(start_hour = "13")
	disp.cust_run("./static/urls.pkl")

if __name__ == '__main__':
	main()

```
结果保存在./records/目录下