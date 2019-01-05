# python 百度图片自动爬取程序——多线程升级版

## python 版本  —— `Python 3.7.0`

# 优化版本 1.0   ——多线程优化
相比起我博客的代码，这里的代码进行了一点优化，就是我发现博客写的单线程爬取还是有点太慢了，所以这里加上了多线程的操作，
将原来需要十多秒的爬取优化到了一秒以内，还是挺不错的，大家可以试试。


# 以下是正常的爬虫程序编写步骤
## 1、确立需求

- 可以修改关键词爬取我们想要的不同的图片集
- 可以选择爬取的图片数量
- 爬取的图片大小是原图片大小
- 爬取鲁棒性


暂时就确定上面的几个需求吧，然后开始真正的爬虫代码的编写

## 2、观察网页源码
首先打开百度图片，随意搜索一个关键词，比如这次用我比较喜欢的动漫角色  **栗山未来**  来进行测试

右键查看网页源代码之后可以看到，每张图片的原地址开头都是很简单的`"objURL"`，结尾都是一个小逗号，如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190104162331379.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NvZGVkb2N0b3I=,size_16,color_FFFFFF,t_70)

根据这点我们可以确定这个爬虫该如何进行操作了，很简单——从网页源码中提取出这些url并进行下载就可以了 `\(^o^)/~`
## 3、获取网页源码

其实这一步我有点不想写的，不过担心有看我的博客刚学`python`的朋友可能会出现错误，还是说一下吧。

首先，我们需要引入`python`中的网络库`urllib`,由于我们要用到的`urlopen`和`read`方法在我这个版本的`python`中，直接引用`urllib`会出现错误，所以一般采用此`import`：`import urllib.request`

整个的提取网页源码的方法如下：

```python
import urllib.request
def get_html(httpUrl):
	page = urllib.request.urlopen( httpUrl )#打开网页
	htmlCode = page.read( )#读取网页
	return htmlCode
```

我们可以把这个方法打包成一个py文件，以后直接就可以在其他py文件中`import`一下这个方法，然后直接使用我们写好的`get_html`方法就可以了。

然后将上方获取到的二进制文件，解码成一个正常地字符串：

```python
html_code=get_html(search_url)
html_str=html_code.decode(encoding = "utf-8")#将二进制码解码为utf-8编码，即str
```


## 4、提取图片地址

说到提取网页源码中的关键数据，其实就是字符串匹配，这要是在`C++`里面估计得把我累死，当然我也的确写过类似的，甚至更复杂的，实在是惨痛的回忆。

这里向大家推荐一下比较简单的字符串检索和匹配方案——**正则表达式**，又称规则表达式。（英语：`Regular Expression`，在代码中常简写`为regex`、`regexp`或`RE`）

当然具体的如何使用正则表达式我就不多说了，大家自行搜索各个视频网站，看个大概就够了，或者直接看这里——[正则表达式基础](http://www.runoob.com/regexp/regexp-syntax.html)

了解一下正则表达式的基本逻辑就ok了。

进入正题，上面的一步已经分析了每张图片的原地址开头都是很简单的`"objURL"`，所以我们正则的关键就是把`"objURL"`后方的地址拿出来就够了，这很简单，我就直接把写好的正则表达式拿出来了：

```python
reg=r'"objURL":"(.*?)",'
```
ps:字符串前的r主要是防止少写了转义字符引起的字符缺失

这个正则的作用如下：
**匹配以`"objURL":"`开头，并且以`",`结尾的任意字符串**

然后就是简单地编译一下这个正则（记得`import`一下`re`包)：
```python
import re
reg=r'"objURL":"(.*?)",'
reg_str = r'"objURL":"(.*?)",'      #正则表达式
reg_compile = re.compile(reg_str)
```


然后用上方编译之后的正则表达式对第三步获取到的字符串进行解析，如下：

```python
pic_list = reg_compile.findall(html_str)
```
上方的`pic_list`就是一个简单的列表
将列表中的数据输出：
```python
    for pic in pic_list:
      print(pic)
```
输出如下：

```
http://b-ssl.duitang.com/uploads/item/201609/02/20160902174427_4H2V8.jpeg
http://b-ssl.duitang.com/uploads/item/201607/18/20160718133442_cnmKP.jpeg
http://cdnq.duitang.com/uploads/item/201504/05/20150405H2814_VvZfS.jpeg
http://wxpic.7399.com/nqvaoZtoY6GlxJuvYKfWmZlkxaJhpc-bna-SmqKfYm/lmqN-oo5Gop3nXfWqYhdpxmoPGZHOozqx7fpyToXCcmYaMvIe0g6GuocOqdnmP1WGrsLCZoY-ub36elaeBr42tb6nSh5qApHqCrnyPq6K0emd6152Ti7Crh3ZiYHGvq5acpNpu
http://i1.hdslb.com/bfs/archive/801e00579f4b5bd2b83dcdd665dcc7819fce4470.jpg
http://wxpic.7399.com/nqvaoZtoY6GlxJuvYKfWmZlkxaJhpc-bna-SmqKfYm/lmqN-oo5Gop3nXfWqYhdpxmoPGZHOozqx7fpyToXCcmYaHv3vFrntnotGGeaRpsKp8nbqmZnCXh5-tqZOIrqOgmZDWmsNxoJ2bs4Jsqoy-fm2BznWlf82clpxiYHGvq5acpNpu
```
可以明显地看到，其中有几个地址并不是图片地址，这可以说是我的正则出了一点问题，不过也并无伤大雅（实际是我懒得改了），稍微一点判断即可完美解决（由于所有图片地址结尾都为g，如`png、jpg、jpeg`  `^_^`）



```
for pic in pic_list:
	if pic[len(pic)-1]=='g':
		print(pic)
```

完美解决，w(ﾟДﾟ)w

ps：哈哈哈，当然是开玩笑的啦这里，大家记得自己想个好方法进行改正，算是一个小测试吧，毕竟真的无伤大雅。


## 5、下载图片

下载图片也很简单，我最开始已经说过，图片其实就是存在远端服务器的一个图片文件，只要服务器允许，我们一个GET请求就可以轻松地拿到这个图片了，毕竟浏览器也是这么做的，至于你拿到干什么，是用来真的填充网页还是自己用就没人在乎了。

下载图片`python`有很多的方法，如下存在三种

(以下代码非本人所写，版本是否正确也不确定，存在错误请自行百度，第一种在我的版本未出现问题）：

```python
def urllib_download(url):
    from urllib.request import urlretrieve
    urlretrieve(url, '1.png')     
 
def request_download(url):
    import requests
    r = requests.get(url)
    with open('1.png', 'wb') as f:
        f.write(r.content)                      
 
def chunk_download(url):
    import requests
    r = requests.get(url, stream=True)    
    with open('1.png', 'wb') as f:
        for chunk in r.iter_content(chunk_size=32):
            f.write(chunk)
 
```
所以我们只需要把上方的列表中的每个图片网址进行下载就可以了，我选择的是上方的第一种，这是存在于`urllib.request`中的一个方法，其定义如下：

```python
urllib.request.urlretrieve(url, filename, reporthook, data)
参数说明：
url：外部或者本地url
filename：指定了保存到本地的路径（如果未指定该参数，urllib会生成一个临时文件来保存数据）；
reporthook：是一个回调函数，当连接上服务器、以及相应的数据块传输完毕的时候会触发该回调。我们可以利用这个回调函数来显示当前的下载进度。
data：指post到服务器的数据。该方法返回一个包含两个元素的元组(filename, headers)，filename表示保存到本地的路径，header表示服务器的响应头。
```

然后就是简单的一个循环下载就ok了：


```python
def download_pic(pic_adr,x):
	urllib.request.urlretrieve(pic_adr, '%s.jpg' %x)
	# './images/%s.jpg'，这里也可以自己选择创建一个文件吧所有图片放进去，而不是直接放在当前目录下
	
x=0
for pic in pic_list:
	if pic[len(pic)-1]=='g':
		print(pic)
		download_pic(pic,x)
		x += 1
```
给每一个图片取一个土逼的名字当然是必须的，就递增1234这样取名就可以了。

这样我们就已经结束了整个爬虫的过程，执行之后，效果如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190104162525413.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NvZGVkb2N0b3I=,size_16,color_FFFFFF,t_70)

可以看到，效果还是不错的，毕竟放在那里让它自己下载就可以了，大家也可以想一下如何翻页之类的效果，其实也很简单，我就随便说一下实现一个更改关键词的效果来提示吧（其实是因为有点懒不想写）

## 6、更改搜索关键词

看百度搜索页面的网址：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190104162535863.png)

观察这一网址，我们可以很简单地发现，原来最后的keyword后面的就是关键词啊，复制下来改一下就可以了嘛，但是复制下来发现事情并不简单：

```
http://image.baidu.com/search/flip?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1546589116401_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=0&height=0&face=0&istype=2&ie=utf-8&ctd=1546589116402%5E00_1519X723&word=%E6%A0%97%E5%B1%B1%E6%9C%AA%E6%9D%A5
```
为什么`word`后面变成了`%E6%A0%97%E5%B1%B1%E6%9C%AA%E6%9D%A5`
这么一堆东西？

很简单，因为`url`是`ASCII`码，而这里我们用到了中文，用一点小操作转一下就可以了：

```python
keyword=urllib.parse.quote(keyword)
search_url="http://image.baidu.com/search/flip?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1546580974349_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&ctd=1546580974351%5E00_1519X723&word="
search_url=search_url+keyword       #加上关键字
```
`urllib.parse.quote`就是解码的代码，在后面加上关键字就oK了。

简单吧，这个简单的python爬虫就写完了。。

虽然还是想自己写字符串识别，但是正则实在是太好用了。还是推荐大家多学一点正则的骚技巧吧。




