#__author: ZhangWP
#date : 2018/8/8
import urllib.request
import urllib.error
import re

header = ('user-agent',"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3486.0 Safari/537.36")
opener = urllib.request.build_opener()
opener.add_handlers=[header]
urllib.request.install_opener(opener)

def get_comments_of_video(page):
    try:
        first_id = '6430642772367600825'
        next_url = 'http://video.coral.qq.com/filmreviewr/c/upcomment/33bfp8mmgakf0gi?callback=_filmreviewrcupcomment33bfp8mmgakf0gi&reqnum=3&commentid='+first_id+'&_=1533703850956'
        next_id_pattern = '"last":"(.*?)"'
        comment_pattern = '"content":"(.*?)",'
        file = open('Tencent_Video_Comments.txt', 'w')
        count = 0
        for i in range(0,page):
            page = urllib.request.urlopen(next_url).read().decode('utf-8', 'ignore')
            comments = re.findall(comment_pattern,page)
            if comments == []:
                file.close()
                print("全部爬取完毕！")
                exit(0)
            for comment in comments:
                file.write("---------------第"+str(count+1)+'条评论---------------\n'+eval('u"'+comment+'"')+"\n\n\n")
                print("第" + str(count + 1) + "条评论写入成功！")
                count += 1
            next_id = re.findall(next_id_pattern, page)[0]
            next_url = 'http://video.coral.qq.com/filmreviewr/c/upcomment/33bfp8mmgakf0gi?callback=_filmreviewrcupcomment33bfp8mmgakf0gi&reqnum=3&commentid='+next_id+'&_=1533703850956'
            #print(next_url)
        file.close()
    except urllib.error.URLError as e1:
        if hasattr(e1,'code'):
            print(e1.code)
        if hasattr(e1,'reason'):
            print(e1.reason)
        file.close()
    except Exception as e2:
        file.close()
        print(e2)

get_comments_of_video(5)