import logging
import connexion
import datetime
import json
import os.path
import requests
import yaml
import logging.config
from time import sleep
from pykafka import KafkaClient
from random import random
from datetime import datetime
from connexion import NoContent
from flask import appcontext_popped
from runpy import run_path
from time import time

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())
    # print(app_config)

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger("basicLogger")


def trace_id(time_stamp):
    return str(f"{time_stamp}{str(random())}")




retry_count = 0


while retry_count < app_config["events"]["retry_count"]:
    try:
        logger.info(f"trying to connect {retry_count}")
        client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
        topic = client.topics[str.encode(app_config['events']['topic'])]
        producer = topic.get_sync_producer()
        break
    except:
        logger.error("It does not work, lOL")
        retry_count = retry_count + 1
        sleep(app_config["events"]["sleep_time"])


def report_age_n_gender_reading(body):
    now = datetime.now()
    run_path = app_config['eventstore1']['url']
    trace_rec = trace_id(body['timestamp'])
    logger.info(f"Recieved event 'age_n_gender' request with a trace id of {trace_rec}")
    body["date_created"]=now.strftime(f"%Y-%m-%dT%H:%M:%SZ")
    body["trace_id"]= str(trace_rec)
    print(body)
    # r = requests.post(run_path, json=body
    """ 
    Kafka setup
    """
#    client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
#    topic = client.topics[str.encode(app_config['events']['topic'])]
    #producer = topic.get_sync_producer()
    msg = {"type": "Age and Gender",
            "datetime": datetime.now().strftime(f"%Y-%m-%dT%H:%M:%S"),
            "payload": body
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    logger.info(f"Returned event 'age_n_gender' response {trace_rec} with status 201")
    return NoContent, 201

def report_height_n_weight_reading(body):
    now = datetime.now()
    run_path = app_config['eventstore2']['url']
    trace_rec = trace_id(body['timestamp'])
    logger.info(f"Recieved event 'height_n_weight' request with a trace id of {trace_rec}")
    body["date_created"]=str(now.strftime(f"%Y-%m-%dT%H:%M:%SZ"))
    body["trace_id"]= str(trace_rec)
    # r = requests.post(run_path, json=body)

    """ 
    Kafka setup
    """
 #   client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
  #  topic = client.topics[str.encode(app_config['events']['topic'])]
   # producer = topic.get_sync_producer()
    msg = {"type": "Height and Weight",
            "datetime": datetime.now().strftime(f"%Y-%m-%dT%H:%M:%S"),
            "payload": body
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    logger.info(f"Returned event 'height_n_weight' response {trace_rec} with status 201")
    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml")


if __name__ == "__main__":
    app.run(port=8080)
