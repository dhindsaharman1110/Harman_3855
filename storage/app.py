from operator import and_
import connexion
import datetime
import time
import json
import os.path
import logging
import yaml
import logging.config
from base import Base
from age_n_gender import Age_n_gender
from height_weight import Height_n_weight
from random import random
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from platform import python_branch
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
from sqlalchemy import and_





if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"


with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())
# External Logging Configuration
with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)


logger = logging.getLogger('basicLogger')
logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)


DB_ENGINE = create_engine(f"mysql+pymysql://{app_config['datastore']['user']}:{app_config['datastore']['password']}@{app_config['datastore']['hostname']}:{app_config['datastore']['port']}/{app_config['datastore']['db']}")

Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def trace_id(time_stamp):
    return str(f"{time_stamp}{str(random())}")


def write_data_into_file(data):
    EVENT_FILE="data.json"
    MAX_EVENTS=10
    if os.path.isfile(EVENT_FILE) == False:
        c=open(EVENT_FILE, "w")
        c.write("[]")
        c.close()

    f=open(EVENT_FILE, "r")
    old_data = f.read()
    f.close()
    
    old_data=json.loads(old_data)
    
    if len(old_data) == MAX_EVENTS:
        old_data.pop(0)
    old_data.append(data)
    
    h=open(EVENT_FILE, "w")
    h.write(json.dumps(old_data, indent=4))
    h.close()



compare_old = []

def get_age_n_gender_readings(timestamp, end_timestamp):
    logger.info(f"(Connecting to DB. Hostname: {app_config['datastore']['hostname']}, Port: {app_config['datastore']['port']} )")
    """ Gets new age and gender readings after the timestamp """
    session = DB_SESSION()
    
    time_format = f"%Y-%m-%dT%H:%M:%SZ"
    
    timestamp_datetime = datetime.datetime.strptime(timestamp, time_format)
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, time_format)
    readings = session.query(Age_n_gender).filter(
        and_(Age_n_gender.date_created >= timestamp_datetime,
            Age_n_gender.date_created <  end_timestamp_datetime))
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for Age and Gender readings after %s returns %d results" %(timestamp, len(results_list)))
    return results_list, 200

def get_height_n_weight_readings(timestamp, end_timestamp):
    logger.info(f"(Connecting to DB. Hostname: {app_config['datastore']['hostname']}, Port: {app_config['datastore']['port']} )")
    """ Gets new age and gender readings after the timestamp """
    session = DB_SESSION()
    
    time_format = f"%Y-%m-%dT%H:%M:%SZ"
    
    timestamp_datetime = datetime.datetime.strptime(timestamp, time_format)
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, time_format)
    
    readings = session.query(Height_n_weight).filter(
        and_(Height_n_weight.date_created >= timestamp_datetime,
             Height_n_weight.date_created < end_timestamp_datetime))
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for Height and Weight readings after %s returns %d results" %(timestamp, len(results_list)))
    return results_list, 200

def process_messages():
    """ Process event messages """
    hostname = f"%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    
    max_count = 0
    while max_count < app_config["events"]["num"]:
   #     logger.info(f"Trying to connect and current count is {max_count}")
        try:
            logger.info(f"Trying to connect and current count is {max_count}")
            client = KafkaClient(hosts=hostname)
            topic = client.topics[str.encode(app_config["events"]["topic"])]
            logger.info("Connected")
            break
        except:
            logger.error("Connection Failed")
            time.sleep(app_config["events"]["s_time"])
            max_count = max_count + 1
    
            
    
    
    
    consumer = topic.get_simple_consumer(consumer_group=b'event_group', reset_offset_on_start=False, auto_offset_reset=OffsetType.LATEST)
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]        
        if msg["type"] == "Age and Gender": # Change this to your event type
            session = DB_SESSION()
            agd = Age_n_gender(payload['user_id'],
                               payload['user_name'], 
                               payload['user_age'], 
                               payload['user_gender'],
                               payload['timestamp'],
                               payload['trace_id'])
            session.add(agd)
            session.commit()            
            session.close()
        elif msg["type"] == "Height and Weight":
            session = DB_SESSION()
            hnw = Height_n_weight(payload['user_id'],
                               payload['user_name'], 
                               payload['user_height'], 
                               payload['user_weight'],
                               payload['timestamp'],
                               payload['trace_id'])
            session.add(hnw)
            session.commit()
            session.close()
        consumer.commit_offsets()





app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", base_path="/storage", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
