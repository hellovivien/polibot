from wordcloud import WordCloud
from collections import Counter
import pandas as pd

def get_wc(corpus):
    # mask style: https://github.com/amueller/word_cloud/blob/master/examples/masked.py
    wordcloud = WordCloud(width = 800, height = 800,
                            background_color ='black',
                            min_font_size = 10
                            ).generate(corpus)
    return wordcloud.to_image()

def extract_keywords(text,num=50):
    tokens = [token for token in text.split()]
    most_common_tokens = Counter(tokens).most_common(num)
    return pd.DataFrame(most_common_tokens, columns=('token','count'))    