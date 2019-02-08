#__author: ZhangWP
#date : 2018/8/7
import urllib.request

def proxy_handle (url, proxy_ip):
    proxy = urllib.request.ProxyHandler({'http':proxy_ip})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(url).read().decode('utf-8','ignore')
    return data

def main():
    url = 'http://www.baidu.com'
    ip = '61.135.217.7:80'
    print(proxy_handle(url, ip))

main()
