import urllib.request


def get_html(httpUrl):
    page = urllib.request.urlopen(httpUrl)  #打开网页
    htmlCode = page.read()  #读取网页
    return htmlCode


'''
def store_html_code(html_code,file_name):
	f_html=open(file_name,'w',encoding='utf-8')
	html_str=html_code.decode(encoding = "utf-8")#将二进制码解码为utf-8编码，即str
	f_html.write(html_str)#存入
	f_html.close()
=======
import urllib.request
def get_html(httpUrl):
	page = urllib.request.urlopen( httpUrl )#打开网页
	htmlCode = page.read( )#读取网页
	return htmlCode

'''
'''
def store_html_code(html_code,file_name):
	f_html=open(file_name,'w',encoding='utf-8')
	html_str=html_code.decode(encoding = "utf-8")#将二进制码解码为utf-8编码，即str
	f_html.write(html_str)#存入
	f_html.close()
>>>>>>> f33034e8adc15bf3936bfb2728a296695b8d216b
'''