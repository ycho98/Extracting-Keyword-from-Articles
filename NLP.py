import newsapi
import spacy
from newsapi import NewsApiClient
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import string
from wordcloud import WordCloud


nlp = spacy.load('en_core_web_lg')
newsapi = NewsApiClient (api_key='b957a0e19b8c4037b10a1766c4a5cb17')

articles = []

for i in range(1, 6):
    temp = newsapi.get_everything(q='coronavirus', language='en', 
                                  from_param='2022-03-03', to='2022-03-24', 
                                  sort_by='relevancy', page = i)
    articles.append(temp)

def get_keywords_eng(text):
    result = []
    pos_tag = ['VERB', 'NOUN', 'PROPN']
    
    for token in nlp(text):
        if (token.text in nlp.Defaults.stop_words or token.text in string.punctuation):
            continue
        if (token.pos_ in pos_tag):
            result.append(token.text)
    return result

data = []
for i, article in enumerate(articles):
    for x in article['articles']:
        title = x['title']
        date = x['publishedAt']
        description= x['description']
        content = x['content']
        
        data.append({'title':title, 'date':date, 'description':description, 'content':content})

df = pd.DataFrame(data)
df = df.dropna()
df.head()

results = []

for content in df.content.values:
    results.append([('#' + x[0]) for x in Counter(get_keywords_eng(content)).most_common(5)])
df['keywords'] = results
df.to_excel("ArticlesAboutCovid.xlsx")

#print(results)

words = str(results)
wordcloud = WordCloud(max_font_size=50, max_words=200).generate(words)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()