from src.utils.database import Database
import streamlit as st
import requests
from src.utils.api import predict_tweet, predict_account, get_tweets
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import scipy
import altair as alt

def print_prediction(tweet):
    st.write(f"<div class='text'>{tweet['content']}</div>", unsafe_allow_html=True)
    st.write("<div class='label'><span class='label-droite'>droite: {}%</span><span class='label-gauche' >gauche: {}%</span></div>".format(round(tweet['droite']*100), round(tweet['gauche']*100)), unsafe_allow_html=True)

def render():
    sentences = [
        "C'est la lutte finale; Groupons nous et demain l'Internationale sera le genre humain.",
        "La france aux français d'abord.",
        "Si tout le monde travaillait moins, il y aurait du travail pour tout le monde.",
        "Nous devons fermer nos frontières.",
        "Des parents c'est un papa et une maman.",
        "Les riches ne paient pas assez d'impôts."
    ]
    with Database() as db:
        if st.sidebar.button("demo"):
            for s in sentences:
                res = predict_tweet({"content": s}, db)
                print_prediction(res)
        with st.sidebar.form("predict_input"):
            input = st.text_area("Texte", "les patrons ne devrait pas gagner plus que deux fois le salaire minimum.")
            submit = st.form_submit_button('predict')
        if submit and input:
            res = predict_tweet({"content": input}, db)
            print_prediction(res)
        with st.sidebar.form("add_account"):
            account_name = st.text_input("Compte", "JLMelenchon")
            submit = st.form_submit_button('predict account')
        if submit and account_name:
            with st.spinner('Wait for it...'):
                tweets = get_tweets(account_name)
            score = st.empty()
            if len(tweets) > 0:
                score_droite = []
                score_gauche = []                                           
                for i,tweet in enumerate(tweets):
                    prediction = predict_tweet(tweet, db)
                    score_droite.append(prediction['droite'])
                    score_gauche.append(prediction['gauche'])
                    mean_gauche = round(scipy.mean(score_gauche)*100)
                    mean_droite = round(scipy.mean(score_droite)*100)
                    score.markdown("<p class='scores'><span class='score-gauche'>G: {}% |</span>|<span class='score-droite'>| D: {}%</span></p>".format(mean_gauche, mean_droite), unsafe_allow_html=True)                      
                    print_prediction(prediction)
            

