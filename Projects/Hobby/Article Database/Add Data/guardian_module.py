### This module to access the Guardian API is for specifically for my usecase
### there is no ambition to make a universally applicable library


import pandas as pd
import sqlite3
import requests
from pandas import json_normalize
from flatten_json import flatten
import json
import numpy as np

class Guardian_Cursor:
    def __init__(self, key):
        self.guardian_key = key


    def url_generator(self, search_term, date_from, date_to, page):
        url = ("https://content.guardianapis.com/search?q=" + search_term + "&from-date=" + date_from + 
            "&to-date=" + date_to +"&page=" + str(page) + "&page-size=200&show-tags=contributor&show-blocks=all&&api-key=" + self.guardian_key)
        print(url)
        return(url)

    def get_search_id(self):
        self.c.execute("""SELECT COUNT(*) as count_searches FROM article_search""")
        search_count = self.c.fetchone()[0]
        return(search_count)
    
    def get_text(self, initial_search):
        article_text = []
        for article in initial_search['response']['results']:
            try:
                article_text.append(article['blocks']['body'][0]['bodyTextSummary'])
            except:
                article_text.append(None)
        return article_text

    def split_dates(self, date):
        split_month = int(date[5:7])/2

        date_1 = date[:5] + '0' + str(split_month)[:1] + '-30'
        date_2 = date[:5] + '0' + str(split_month+1)[:1] + '-01'
        return(date_1, date_2)

    def search_generator(self, search_term, date_from, date_to):
        initial_url = self.url_generator(search_term, date_from, date_to, 1)
        initial_search = requests.get(initial_url).json()
        num_pages = initial_search['response']['pages']
        if num_pages == 0:
            return(None, None, None)
        
        elif num_pages > 14:
            split_date_1, split_date_2 = self.split_dates(date_to)
            df_1, df_authors_1, df_a_links_1 = self.search_generator(search_term, date_from, split_date_1)
            df_2, df_authors_2, df_a_links_2 = self.search_generator(search_term, split_date_2, date_to)

            df = pd.concat([df_1, df_2])
            df_authors = pd.concat([df_authors_1, df_authors_2])
            df_a_links = pd.concat([df_a_links_1, df_a_links_2])

            return(df, df_authors, df_a_links)

        elif num_pages > 1:
            df = json_normalize(initial_search['response']['results'])

            df_authors, df_a_links = self.get_authors(initial_search)
            article_text = self.get_text(initial_search)
            for page_number in range(2, num_pages+1):
                url = self.url_generator(search_term, date_from, date_to, page_number)
                search = requests.get(url).json()
                try:
                    df_new = json_normalize(search['response']['results'])
                except:
                    continue
                df = pd.concat([df, df_new])
                df_authors_new, df_alink_new = self.get_authors(search)
                df_authors = pd.concat([df_authors, df_authors_new])
                df_a_links = pd.concat([df_a_links, df_alink_new])
                article_text.extend(self.get_text(search))
        
        else:
            df = json_normalize(initial_search['response']['results'])
            article_text = self.get_text(initial_search)
            # article_text = [article['blocks']['body'][0]['bodyTextSummary'] for article in initial_search['response']['results']]

            df_authors, df_a_links = self.get_authors(initial_search)
        df['article_text'] = article_text
        df = df[df.type == 'article']

        df['length'] = [len(x) for x in df.article_text]
        df = df[df.length <= 60000]
        df = df.drop(columns=['length'])

        return(df, df_authors, df_a_links)

    def get_authors_article(self, json_path):

        id = []
        names = []
        twitters = []
        bios = []

        for author in json_path['tags']:
            try:
                id.append(author['id'])
            except:
                id.append('NA')
            try:
                names.append(author['webTitle'])
            except:
                names.append('NA')
            try:
                bios.append(author['bio'])
            except:
                bios.append('NA')
            try:
                twitters.append(author['twitterHandle'])
            except:
                twitters.append('NA')

        df_article_link = pd.DataFrame()
        
        df_article_link['person_id'] = id
        df_article_link['article_id'] = json_path['id']

        df_authors = pd.DataFrame({'id':id, 'name':names, 'bio':bios, 'twitter':twitters})

        return(df_authors, df_article_link)

    def get_authors(self, json_data):


        df_links = pd.DataFrame(columns=['person_id', 'article_id'])
        df_authors = pd.DataFrame(columns=['id', 'name', 'bio', 'twitter'])

        for article in json_data['response']['results']:
            df_a, df_l = self.get_authors_article(article)
            df_links = pd.concat([df_links, df_l])
            df_authors = pd.concat([df_authors, df_a])

        df_authors.drop_duplicates(inplace=True)

        return(df_authors, df_links)


    def complete_search(self, keyword, date_from, date_to):

        df, df_authors, df_a_links = self.search_generator(keyword, date_from, date_to)

        if df is None:
            search_id = ''.join([keyword, date_from, date_to]).replace('-', '').replace(' ', '')
            search = {'search_id':[search_id], 'search_term':[keyword], 'date_from':[date_from], 
                'date_to':[date_to], 'newspaper':['Guardian'], 'n_results':[0]}
            df_search = pd.DataFrame.from_dict(search)
            return(None, None, None, df_search, None)

        df_select = df[['id', 'sectionName', 'webTitle', 'webUrl', 'webPublicationDate', 'article_text']]
        df_select = df_select.rename(columns={"webPublicationDate":"PublishedDate"})

        search_id = ''.join([keyword, date_from, date_to]).replace('-', '').replace(' ', '')
        search = {'search_id':[search_id], 'search_term':[keyword], 'date_from':[date_from], 
            'date_to':[date_to], 'newspaper':['Guardian'], 'n_results':[len(df)]}
        df_search = pd.DataFrame.from_dict(search)

        df_search_link = pd.DataFrame()
        df_search_link['article_id'] = df_select['id']
        df_search_link['search_id'] = search_id
        df_search_link['search_rank'] = df_select.index.values + 1

        df_select.columns = ['article_id', 'section', 'title', 'web_url', 'date', 'text']

        df_authors.columns = ['person_id', 'name', 'bio', 'twitter']
        df_authors['position'] = 'Journalist'
        df_authors['country'] = np.nan
        df_authors['gender'] = np.nan
        df_authors['age'] = np.nan

        

        return(df_select, df_authors, df_a_links, df_search, df_search_link)