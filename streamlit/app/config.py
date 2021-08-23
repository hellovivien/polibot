from dotenv import dotenv_values
import streamlit as st

env_dict = dotenv_values()
# streamlit
if 'db_password' not in env_dict:
    env_dict['db_password'] = st.secrets["db_password"]
    
conf = {
    'mongo_uri': 'mongodb+srv://politweet:{}@cluster0.0rn9i.mongodb.net/politweet?retryWrites=true&w=majority'.format(env_dict['db_password']),
    'groups_colors': {'AGIR-E': '#5B17E3', 'DEM': '#415291', 'DLF': '#328855', 'EDS': '#BA7096', 'FI': '#626539', 'GDR': '#99A8F7', 'GE': '#52B62B', 'LAREM': '#1484CB', 'LDS': '#248913', 'LND': '#64AE81', 'LR': '#BA2261', 'LT': '#14C55C', 'RN': '#4E1D74', 'SOC': '#7C6437', 'UDI_I': '#9C7621'},
    'positions': {
        "AGIR-E": "centre-droit", # https://fr.wikipedia.org/wiki/Groupe_Agir_ensemble
        "DEM": "centre", # https://fr.wikipedia.org/wiki/Mouvement_d%C3%A9mocrate_(France)
        "DLF": "droite-plus", # https://fr.wikipedia.org/wiki/Debout_la_France
        "EDS": "centre-gauche", # https://fr.wikipedia.org/wiki/Groupe_%C3%89cologie_d%C3%A9mocratie_solidarit%C3%A9
        "FI": "gauche-plus", # https://fr.wikipedia.org/wiki/La_France_insoumise
        "GDR": "gauche-plus", # https://fr.wikipedia.org/wiki/Groupe_de_la_Gauche_d%C3%A9mocrate_et_r%C3%A9publicaine
        "GE": "centre-gauche", # https://fr.wikipedia.org/wiki/G%C3%A9n%C3%A9ration_%C3%A9cologie
        "LAREM": "centre", # https://fr.wikipedia.org/wiki/La_R%C3%A9publique_en_marche
        "LDS": "droite-plus", # https://fr.wikipedia.org/wiki/Ligue_du_Sud_(France)
        "LND": "gauche", # https://fr.wikipedia.org/wiki/Les_Nouveaux_D%C3%A9mocrates
        "LR": "droite", # https://fr.wikipedia.org/wiki/Les_R%C3%A9publicains
        "LT": "centre", # https://fr.wikipedia.org/wiki/Groupe_Libert%C3%A9s_et_territoires
        "RN": "droite-plus", # https://fr.wikipedia.org/wiki/Rassemblement_national
        "SOC": "gauche", # https://fr.wikipedia.org/wiki/Groupe_socialiste_(Assembl%C3%A9e_nationale)
        "UDI_I": "centre-droit", # https://fr.wikipedia.org/wiki/Union_des_d%C3%A9mocrates_et_ind%C3%A9pendants
    },
    "binary_positions": {
        "gauche": ["gauche", "centre-gauche", "gauche-plus"],
        "droite": ["droite", "centre-droit", "droite-plus"], 
    }
}