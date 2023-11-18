import guardian_module as gm
import database_connection as dc
import pandas as pd
import unicodedata
import numpy as np

# Create Database Connection to local database via the database_connection.py module
username = open('database_login.txt', 'r').readlines()[0].replace('\n', '')
password = open('database_login.txt', 'r').readlines()[1].replace('\n', '')
database = open('database_login.txt', 'r').readlines()[2].replace('\n', '')
db = dc.database(username, password, database)

guardian_key = open('guardian_key.txt', 'r').readlines()[0]
gc = gm.Guardian_Cursor(guardian_key)


# Method to search articles for companies and add them to the database
def get_insert(search_input):
    for company in search_input['companies']:
        print('company: ' + company)
        for year in search_input['years']:
            print('year: ' + str(year))
            date_from = str(year) + '-01-01'
            date_to = str(year) + '-12-31'
            df_article, df_authors, df_author_links, df_search, df_search_links = gc.complete_search(company, date_from, date_to)


            if not df_article is None:
                if len(df_article) > 100:
                    n_splits = int(len(df_article)/100)
                    df_split = np.array_split(df_article, n_splits) 
                    for df in df_split:
                        df.to_csv('temp.csv')
                        db.append(df, 'article')
                else:
                    db.append(df_article, 'article')         
                db.append(df_authors, 'person')
                db.append(df_author_links, 'written_by')      
                db.append(df_search, 'search')
                db.append(df_search_links, 'article_search')
            else:
                db.append(df_search, 'search')
            

            df_company_search = pd.DataFrame()
            df_company_search['search_id'] = df_search.search_id
            df_company_search['company_name'] = company
            db.append(df_company_search, 'company_search')


# Get selection of companies to search articles for
cursor = db.get_cursor()
cursor.execute("""SELECT name 
    FROM company 
    ORDER BY current_employee_estimate DESC
    LIMIT 50
    """)

companies = [x[0] for x in cursor.fetchall()]

removing = ['tata consultancy services', 'cognizant technology solutions', 'at&t', 
    'education nationale', 'department of veterans affairs', 'unitedhealth group', 'united states postal service',
    'wipro technologies', 'united states air force']

# Main reason to remove these companies is the composition of their name.
# The "Problem" here lays in the search algorithm of the Guardian API

companies = [x for x in companies if x not in removing]

search_input = {'companies':companies[7:], 'years':list(range(2010, 2023))}

get_insert(search_input)