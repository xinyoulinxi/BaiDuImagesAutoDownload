from url_get import get_html
import time
import urllib
from urllib.request import urlretrieve
import re
import threading

def get_keyword_urllist(keyword):                #爬取当前关键词下的图片地址
	keyword=urllib.parse.quote(keyword)
	search_url="http://image.baidu.com/search/flip?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1546580974349_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&ctd=1546580974351%5E00_1519X723&word="
	search_url=search_url+keyword                #加上关键字
	html_code=get_html(search_url)
	html_str=html_code.decode(encoding = "utf-8")#将二进制码解码为utf-8编码，即str
	reg_str = r'"objURL":"(.*?)",'               #正则表达式
	reg_compile = re.compile(reg_str)
	pic_list = reg_compile.findall(html_str)
	return pic_list


#以下两变量是可修改变量
thread_word_index=int(5)               #每个线程被分配的任务量
keyword="栗山未来"                      #关键词


pic_list=get_keyword_urllist(keyword)  #获取所有图片的地址并存储在pic_list中


print("successful get_keyword_urllist")


def download_pic(address,name):        #下载图片
	urllib.request.urlretrieve(address, name)

def auto_download(x):                  #线程自动下载自己的任务
	i=0
	while i<thread_word_index:

		pic=pic_list[x+i]
		if pic[len(pic)-1]=='g':
			name = keyword+str(x+i)
			download_pic(pic,'./images1/%s.jpg' %name)
			#time.sleep(0.01)
			print ("{0} get {1} html success".format(threading.current_thread().name ,x+i))
		i+=1

def _main():#主线程

	list_len=len(pic_list)
	thread_len=int(list_len/thread_word_index)
	print(thread_len)
	i_thread=0
	while i_thread<thread_len:
		print("thread",i_thread,"successful created")
		t =threading.Thread(target=auto_download, name='Thread'+str(i_thread),args=(i_thread*thread_word_index,))
		t.start()
		i_thread+=1
	#以下主线程执行剩下的任务
	main_thread_begin=i_thread*thread_word_index
	mthread_i=0
	while mthread_i+main_thread_begin<list_len:
		pic=pic_list[main_thread_begin+mthread_i]
		if pic[len(pic)-1]=='g':
			name = keyword+str(main_thread_begin+mthread_i)
			download_pic(pic,'./images1/%s.jpg' %name)
			print ("{0} get {1} html success".format(threading.current_thread().name ,x+i))
		mthread_i+=1

_main()


