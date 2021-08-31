import streamlit as st
import snscrape.modules.twitter as sntwitter
from src.config import conf
from pymongo import MongoClient
from bson.objectid import ObjectId
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) # hide pymongo DeprecationWarning
from math import ceil
import locale
import requests
from pathlib import Path
from src.pages import bot, tweets, scrape

st.set_page_config(layout="wide")


# load css files
def local_css(file_name):
    with open('{}/{}'.format(Path(__file__).with_name('css'), file_name)) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

def main():
    # locale.setlocale(locale.LC_ALL, 'fr_FR.utf8') # todo fix for linux
            
    local_css('style.css')

    # menu
    # menu_dict = {
    #     'Polibot': bot,
    #     'Politweets': tweets,
    # }
    # menu_choice = st.sidebar.radio("menu", list(menu_dict.keys()))
    # if menu_choice:
    #     menu_dict[menu_choice].render()
    
    bot.render()
    
if __name__ == '__main__':
    main()

    


 

            
