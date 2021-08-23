import pandas as pd
import neattext as nt 
import demoji
import unicodedata
from pymongo import MongoClient

# flags emoji
flags = ['🇫🇷','🇬🇲']

class Cleaner():
    '''
    clean the input with pipeline func, you can pass a string, a list or a dataframe
    if to_str = true the input will be convert to string
    func available are in cleaning_func dictionnary
    define your pipeline on class init with base_pipeline or after with clean func
    /!\ pay attention to the order of functions in your pipeline /!\
    you can reset the input cleaning with reset func
    '''


    def __init__(self, input, to_str=False, base_pipeline=[], remove_char=[], replace_char=[], escape_char=[], custom_stopwords=[], df_field='content') -> None:
        
        if to_str:
            if type(input) == list:
                input = ' '.join(input)
            elif type(input) == pd.DataFrame:
                input = input.to_dict('records')
                input = [row[df_field] for row in input]
                input = ' '.join(input)

        self.df_field = df_field
        self.input = input
        self.dirty_input = input
        self.remove_char = remove_char
        self.replace_char = replace_char
        self.escape_char = ["\n", "\r", "\t", "\b"]+escape_char
        self.custom_stopwords = custom_stopwords                

        if len(base_pipeline)>0:
            self.base_pipeline = base_pipeline
        else:
            self.base_pipeline = ['fix_escape', 'urls', 'emails', 'html_tags', 'multiple_spaces']        

        self.cleaning_func = {
            "urls": nt.remove_urls,
            "emails": nt.remove_emails,
            "numbers": nt.remove_numbers,
            "phone_numbers": nt.remove_phone_numbers,
            "common_punctuations": nt.remove_puncts,
            "all_ponctuations": self.remove_all_ponctuations,
            "special_characters": nt.remove_special_characters, # agressive cut regex [^A-Za-z0-9 ]+
            "currencies": nt.remove_currencies,
            "currency_symbols": nt.remove_currency_symbols,
            "html_tags": nt.remove_html_tags,
            "dates": nt.remove_dates,
            "non_asci": nt.remove_non_ascii,
            "multiple_spaces": nt.remove_multiple_spaces,
            "street_address": nt.remove_street_address,
            "postoffice_box": nt.remove_postoffice_box,
            "shortwords": nt.remove_shortwords, # 3 or less char
            "userhandles": nt.remove_userhandles, # @myAccount
            "hashtags": nt.remove_hashtags, # remove all hashtag symbol and content
            "en_stopwords": nt.remove_stopwords, # multilang list: https://github.com/Jcharis/neatinput/blob/fbf0db07704352dafde3ec9493ce7e01f5a27ebd/neatinput/pattern_data/stopwords_list.py
            "fr_stopwords": self.remove_fr_stopwords,
            'custom_words': self.remove_custom_words,
            'custom_char': self.remove_custom_char,
            "emoji": self.remove_emoji,
            "replace_bad_quotes": nt.replace_bad_quotes,
            "replace_by_space": self.replace_by_space,
            "replace_emoji": self.replace_emoji,
            'fix_escape': self.fix_escape,
            "fix_contractions": nt.fix_contractions, # i'm -> i am
            "fix_unicode": self.fix_unicode,
        }        

    def remove_emoji(self, input):
        return demoji.replace(nt.remove_emojis(self.input), "")

    def replace_emoji(self, input):
        return demoji.replace_with_desc(self.input, sep="")

    def remove_all_ponctuations(self, input):
        return nt.remove_punctuations(self.input, most_common=False)

    def remove_fr_stopwords(self, input):
        return nt.remove_stopwords(self.input, lang="fr")

    def remove_custom_words(self, input):
        return nt.remove_custom_words(self.input, self.custom_stopwords)

    def replace_by_space(self, input, chars=[]):
        if len(chars) == 0:
            chars = self.replace_char  
        for char in chars:
            input = input.replace(char, ' ')
        return input

    def fix_escape(self, input):
        return self.replace_by_space(input, self.escape_char)   

    def remove_custom_char(self, input):
        for char in self.remove_char:
            input = input.replace(char, '')
        return input

    def fix_unicode(self, input):
        return unicodedata.normalize('NFKD', self.input.encode('utf-8').decode())

    def reset(self):
        '''
        back to dirty input
        '''
        self.input = self.dirty_input
        

    def clean_item(self, item, pipeline):
        for step in pipeline:
            item = self.cleaning_func[step](item)
        return item         

    def clean(self, pipeline=[]):
        pipeline = self.base_pipeline+pipeline
        if type(self.input) == list:
            self.input = map(lambda x: self.clean_item(x, pipeline), self.input)
        elif type(self.input) == pd.DataFrame:
            self.input[self.df_field] = self.input[self.df_field].apply(lambda x: self.clean_item(x, pipeline))
        else:
            self.input = self.clean_item(self.input, pipeline)