import mysql.connector

db_conn = mysql.connector.connect(host="mykafka.eastus.cloudapp.azure.com", user="user", 
password="password", database="events") 
 
db_cursor = db_conn.cursor() 
 
db_cursor.execute(''' 
                  DROP TABLE age_n_gender, height_n_weight 
                  ''') 
 
db_conn.commit() 
db_conn.close()