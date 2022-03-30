import mysql.connector

db_conn = mysql.connector.connect(host="mykafka.eastus.cloudapp.azure.com", user="user", password="password", database="events")
db_cursor = db_conn.cursor()

db_cursor.execute(''' 
          CREATE TABLE age_n_gender
          (id INT NOT NULL AUTO_INCREMENT, 
           user_id VARCHAR(250) NOT NULL,
           user_name VARCHAR(250) NOT NULL,
           user_age INTEGER NOT NULL,
           user_gender VARCHAR(250) NOT NULL, 
           timestamp VARCHAR(100) NOT NULL,
           trace_id VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT age_n_gender_pk PRIMARY KEY (id)) 
          ''')

db_cursor.execute('''
           CREATE TABLE height_n_weight
           (id INT NOT NULL AUTO_INCREMENT, 
           user_id VARCHAR(250) NOT NULL,
           user_name VARCHAR(250) NOT NULL,
           user_height INTEGER NOT NULL,
           user_weight INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           trace_id VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
            CONSTRAINT height_n_weight_pk PRIMARY KEY (id))
          ''')

db_conn.commit()
db_conn.close()