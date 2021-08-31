from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import Markdown, display

def md(input):
    return display(Markdown(input))

def get_wc(data):
    # mask style: https://github.com/amueller/word_cloud/blob/master/examples/masked.py
    wordcloud = WordCloud(width = 400, height = 400,
                            background_color ='black',
                            min_font_size = 10
                            ).generate(" ".join(data))
    return wordcloud.to_image()

def plot_keywords(df,title='Title'):
    fig = plt.figure(figsize=(20,10))
    plt.title(title)
    sns.set(font_scale=1.1)
    sns.barplot(y='token',x='count',data=df,orient="h")
#     plt.xticks(rotation=45)
    return fig    

def extract_keywords(text,num=50, begin=None, exclude = []):
    if begin:
        tokens = [token for token in text.split() if token.startswith(begin)]
    else:
        tokens = [token for token in text.split() if token not in exclude]
    tokens = [token for token in text.split()]
    most_common_tokens = Counter(tokens).most_common(num)
    return pd.DataFrame(most_common_tokens, columns=('token','count'))

def get_target(group):
    '''
    Takes the political group as an argument
    Returns 'droite' or 'gauche'
    Else returns 'centre' e.g. if it is a group of the center
    '''
    target_dict = {
      "droite":["AGIR-E", "DLF", "LDS", "LR", "RN", "UDI_I"],
      "gauche":["EDS", "FI", "GDR", "GE", "LND", "SOC"],
    }
    if group in target_dict["droite"]:
      return "droite"
    elif group in target_dict["gauche"]:
      return "gauche"
    else:
      return "centre"    