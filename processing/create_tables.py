import sqlite3

conn = sqlite3.connect('stats.sqlite')

c = conn.cursor()
c.execute('''
            CREATE TABLE stats
            (id INTEGER PRIMARY KEY ASC,
            num_a_g_readings INTEGER NOT NULL,
            max_a_readings INTEGER,
            num_h_w_readings INTEGER NOT NULL,
            max_h_readings INTEGER,
            max_w_readings INTEGER,
            last_updateds VARCHAR(100) NOT NULL
            )
''')


conn.commit()
conn.close()