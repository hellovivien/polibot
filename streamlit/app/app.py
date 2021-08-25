import streamlit as st
import snscrape.modules.twitter as sntwitter
from config import conf
from pymongo import MongoClient
from bson.objectid import ObjectId
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) # hide pymongo DeprecationWarning
from math import ceil
import locale


client = MongoClient(conf['mongo_uri'])
db = client.politweet

# load css files
def local_css(file_name):
    with open('app/css/{}'.format(file_name)) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

def menu_polibot():
    st.write('en construction')

def menu_polibase():
    match = {}
    # accounts widget
    accounts = db.accounts.find({},{'first_name':1, 'last_name':1, 'group':1}).sort('last_name')
    current_accounts = st.sidebar.multiselect('Account', accounts, format_func=lambda x: "{} {}".format(x['last_name'], x['first_name']))
    if current_accounts:
        accounts_ids = [ObjectId(account['_id']) for account in current_accounts]
        if len(accounts_ids)>0:
            match['account_id'] = {'$in': accounts_ids}


    binary_dict = conf['binary_positions']
    positions_dict = conf['positions']
    def get_groups_from_binary(binary_value, binary_dict, positions_dict):
        positions = binary_dict[binary_value]
        return get_groups_from_position(positions, positions_dict)

    def get_groups_from_position(current_positions, positions_dict):
        return [group for group,position in positions_dict.items() if position in current_positions]

    # droite/gauche widget
    labels = ['']+list(binary_dict.keys())
    current_binary = st.sidebar.selectbox('Droite | Gauche', labels)
    if current_binary:
        groups_from_binary = get_groups_from_binary(current_binary, binary_dict, positions_dict)
        match['group'] = {'$in': groups_from_binary} 

    # position widget
    labels = set(conf['positions'].values())
    current_positions = st.sidebar.multiselect('Position', labels)
    if current_positions and not current_binary:
        groups_from_positions = get_groups_from_position(current_positions, positions_dict)
        match['group'] = {'$in': groups_from_positions}            

    # groups widget
    short_groups = db.accounts.distinct('group')
    groups_list = []
    for short_name in short_groups:
        res = db.accounts.find_one({'group':short_name}, {'_id':0, 'group_name':1})
        label = "{} ({})".format(res['group_name'], short_name)
        groups_list.append({'label':label, 'value':short_name})
    current_groups = st.sidebar.multiselect('Group', groups_list, format_func=lambda x: x['label'])
    if current_groups and (not current_binary and not current_positions):
        values = [group['value'] for group in current_groups]
        match['group'] = {'$in': values}
    tweets_by_page = 50
    tweets = db.tweets.find(match).sort('date', -1)
    tweet_count = tweets.count()
    max_page = ceil(tweet_count/50)
    page_number = st.sidebar.number_input('Page ({})'.format(max_page), min_value=1, max_value=max_page)
    start_pagination = (page_number-1)*tweets_by_page
    end_pagination = start_pagination + tweets_by_page
    for tweet in tweets[start_pagination:end_pagination]:       
        st.markdown('<small>**{}** | {}</small>'.format(tweet['account_first_name']+' '+tweet['account_last_name'],tweet['date'].strftime('%A %d/%m/%Y à %H:%M:%S')), unsafe_allow_html=True)
        st.markdown('{}'.format(tweet['content']))
        st.write("""
        <div class='label'>
            <a href='{}'>voir le tweet</a>
            <span class='label-{}' >{}</span>
        </div>
        """.format(tweet['url'], tweet['group'], tweet['group']), unsafe_allow_html=True)
        st.write('<hr />',  unsafe_allow_html=True)


def main():
    # locale.setlocale(locale.LC_ALL, 'fr_FR.utf8') # todo fix for linux
    st.set_page_config(layout="wide")        
    local_css('style.css')

    # menu
    menu_dict = {
        'Polibase':menu_polibase,
        'Polibot':menu_polibot,
    }
    menu_choice = st.sidebar.radio("menu", list(menu_dict.keys()))
    if menu_choice:
        menu_dict[menu_choice]()
    
if __name__ == '__main__':
    main()

    


 

            
