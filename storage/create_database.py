import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE age_n_gender
          (id INTEGER PRIMARY KEY ASC, 
           user_id VARCHAR(250) NOT NULL,
           user_name VARCHAR(250) NOT NULL,
           user_age INTEGER NOT NULL,
           user_gender VARCHAR(250) NOT NULL, 
           timestamp VARCHAR(100) NOT NULL,
           trace_id VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE height_n_weight
          (id INTEGER PRIMARY KEY ASC, 
           user_id VARCHAR(250) NOT NULL,
           user_name VARCHAR(250) NOT NULL,
           user_height INTEGER NOT NULL,
           user_weight INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()
