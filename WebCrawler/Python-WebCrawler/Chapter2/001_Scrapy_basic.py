"""
1. Scrapy是一个命令行加上python script合起来一起用的工具, 所以如果是有多个python编译器的情况下
   最好还是为Scrapy开启一个venv, 使用时激活这个venv从而使得可以直接输入scrapy.exe来运行Scrapy命令行工具

2. 由于Scrapy中使用了一些可能需要额外编译的依赖库,所以官方文档建议先安装 Anaconda or Miniconda再使用它们来安装Scrapy
   但是如果知道怎么去解决一些依赖库的额外编译问题(实际上多数是需要一个C / C++编译器),实际上使用pip install scrapy也是可以成功安装的

3. 安装好Scrapy之后, 可以尝试在控制台(Terminal)直接运行scrapy, 如果scrapy已经加入运行路径中并且依赖库完全没问题的话, 会出现版本信息

4. 安装没问题之后, 可以运行scrapy startproject [project_name]来建立一个Scrapy项目, 建立Scrapy项目后, Scrapy工具会自动生成以下文档:

   project_name
       spiders  spider文件夹, 用于存放使用python编写的spider, spider实际上是Scrapy解释网页内容的核心(规则)
           __init__.py  默认的spider代码, 实际上啥都没只有几句TODO
       items.py  数据模型定义, 实际上就是把spider要爬回来的内容分类定义好, 比如爬到了网页的title, 就可以在items中定义为webtitle这样
       pipelines.py  管道模型定义, 实际上就处理爬到的原始的items数据(比如保存,过滤, 去重什么的)然后输出处理后的items数据
       settings.py    配置文件, 可以指定一些Scrapy运行的选项,比如可以定义请求头, spider与pipelines之间的关联
       scrapy.cfg  Scrapy的运行配置文件, 实际上就是约等于IDE的project文件(比如VS的.sln文件)
"""

"""

"""