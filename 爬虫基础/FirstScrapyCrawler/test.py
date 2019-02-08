import re
import urllib.request
import json

links = None
for i in range(1, 2):
    url = "https://list.jd.com/list.html?cat=670,671,672&page=" + str(
        i) + "&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main"
    page = urllib.request.urlopen(url).read().decode('utf-8', 'ignore')
    link_pattern = '<a target="_blank" title="" href="(.*?)">'
    if links is None:
        links = re.findall(link_pattern, page)
    else:
        links = links.extend(re.findall(link_pattern, page))
for link in links:
    link = 'https:' + link
    good_id = re.findall('.*/(.*?).html',link)[0]
    price_url = 'https://p.3.cn/prices/mgets?&skuIds=J_' + good_id
    content = urllib.request.urlopen(price_url).read()
    Json = json.loads(content)[0]
    price = Json['p']
    print(price)