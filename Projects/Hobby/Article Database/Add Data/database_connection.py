import pandas as pd
import mysql.connector as mc
from sqlalchemy import create_engine as ce
import guardian_module as gm
import unicodedata

class database:
    def __init__(self, user, password, database_name):
        mysql_connection = mc.connect(
                host='localhost',
                user=user,
                passwd=password,
                database=database_name)

        self.ae = ce(f'mysql+pymysql://{user}:{password}@localhost:3306/{database_name}')
        self.ae.connect

        self.conn = mysql_connection
        self.cursor = self.conn.cursor()

    def get_cursor(self):
        return self.cursor
    def get_connection(self):
        return self.conn

    def get_table_names(self):
        self.cursor.execute("SHOW TABLES;")
        table_names = [x[0] for x in self.cursor]
        return(table_names)

    def append(self, df, table):
        if not table in self.get_table_names():
            print('No such table in database, you need to separately add a new table')
            return

        try:
            self.cursor.execute(f"SHOW KEYS FROM {table} WHERE Key_name = 'PRIMARY'")
            primary_key = self.cursor.fetchall()[0][4]
            df = df.drop_duplicates(primary_key, keep='first')
        except:
            self.cursor.execute(f"SHOW KEYS FROM {table}")
            primary_key = self.cursor.fetchall()[0][4]

        self.drop_table('temptable', True)
        df.to_sql("temptable", con=self.ae, if_exists='replace', index=False, schema="")

        column_names = str(tuple(df.columns)).replace("'", "")
        column_names_t = ", ".join(['t.' + str(x) for x in column_names.replace('(', '').replace(')', '').split(", ")])


        sql = f"""INSERT IGNORE INTO {table} {column_names}
                        SELECT {column_names_t}
                        FROM temptable t
                        WHERE NOT EXISTS 
                            (SELECT * FROM {table} f
                            WHERE t.{primary_key} = f.{primary_key})"""

        self.cursor.execute(sql)
        self.conn.commit()

    def new(self, df, table_name, primary_key=False):
        if table_name in self.get_table_names():
            print('Table already exists')
        else:
            df.head(1).to_sql(table_name, con=self.ae, if_exists='fail', index=False)
            
        if not primary_key == False:
            assert primary_key in df.columns, "No column is named after the key"
            if df[primary_key].dtypes == 'int64':
                add_primary_key = f"ALTER TABLE {table_name} ADD PRIMARY KEY ({primary_key});"
            else:
                add_primary_key = f"ALTER TABLE {table_name} ADD PRIMARY KEY ({primary_key}(200));"
            df[primary_key] = [unicodedata.normalize('NFD', x).encode('ascii', 'replace') for x in df[primary_key]]
            df.drop_duplicates('name', keep='first', inplace=True)
            df = df[(df[primary_key]!= '') & (df[primary_key]!= ' ')]


        else:
            add_primary_key = f"ALTER TABLE {table_name} ADD id_{table_name} INT NOT NULL AUTO_INCREMENT PRIMARY KEY"

        

        self.cursor.execute(add_primary_key)
        self.append(df, table_name)

    def drop_table(self, table, instantly = False):
        if not table in self.get_table_names():
            print('no such table')
        else:
            if instantly == False:
                confirmation = input(f'Do you really want to drop table {table}? yes/no\n')

                if confirmation == 'yes':
                    self.cursor.execute(f"""DROP TABLE {table};""")
                else:
                    print('Table has not been deleted')
            else:
                self.cursor.execute(f"""DROP TABLE {table};""")

    def get_table(self, table_name):
        df = pd.read_sql(table_name, con=self.ae)
        return(df)



