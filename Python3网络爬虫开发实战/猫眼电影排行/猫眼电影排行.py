import requests
import re

file = open('Ranking.txt', 'w')
for page in range(1, 101):
    url = "http://maoyan.com/board/4?offset=" + str((page - 1) * 10)
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3486.0 Safari/537.36'}
    content = requests.get(url, headers=header)
    ranking_pattern = re.compile('<i class="board-index board-index.*?>(.*?)</i>' +
                                 '.*?<a href=.*?title="(.*?)" class="image-link"' +
                                 '.*?<p class="star">(.*?)</p>' +
                                 '.*?<p class="releasetime">(.*?)</p>' +
                                 '.*?<p class="score"><i class="integer">(.*?)</i></p>', re.S)
    result = ranking_pattern.findall(content.text)
    #print(result)
    for i in range(0,len(result)):
        result[i] = list(result[i])
        result[i][2] = result[i][2].strip()
        result[i][4] = result[i][4].replace('</i><i class="fraction">', '')
        file.write("--*--第" + result[i][0] + '--*--评分' + result[i][4] + '\n')
        file.write(result[i][1] + '\n' + result[i][2] + '\n' + result[i][3] + '\n\n')

    print("第"+str(page)+"页写入完成！")
file.close()