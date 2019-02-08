import jieba
from wordcloud import WordCloud, STOPWORDS
from PIL import Image

print("正在绘制词云...\n")
text = open('./tips.txt', encoding='utf-8').read()
wordlist = ' '.join(jieba.cut(text))
wordcloud = WordCloud(
    font_path='C:/Windows/Fonts/simhei.ttf',
    background_color='white',
    stopwords=STOPWORDS.add('时候'),
    width=2000,
    height=1720
).generate(wordlist)
'''
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
'''
wordcloud.to_file('./wordCloud.png')
Image.open('./wordCloud.png').show()