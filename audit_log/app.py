import os
import logging
import connexion
import datetime
import json
import os.path
import requests
import yaml
import logging.config

from pykafka import KafkaClient
from random import random
from datetime import datetime
from connexion import NoContent
from flask import appcontext_popped
from runpy import run_path
from time import time
from flask_cors import CORS, cross_origin

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


def get_age_n_gender_reading(index):
    """ Get Age and Gender Reading in History """
    hostname = "%s:%d" % (app_config["events"]["hostname"],
    app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
    consumer_timeout_ms=1000)
    logger.info("Retrieving Age and Gender at index %d" % index)
    index_a=0
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            # if i == index and msg['type'] == "Age and Gender":
            #     return msg['payload'], 200
            # else:
            #     i=i+1     
            if msg['type'] == "Age and Gender":
                index_a = index_a + 1
                if index_a == index:
                    return msg['payload'], 200
    except:
        logger.error("No more messages found")  
    logger.error("Could not find Age and Gender at index %d" % index)
    return { "message": "Not Found"}, 404


def get_height_n_weight_reading(index):
    """ Get Height and Weight Reading in History """
    hostname = "%s:%d" % (app_config["events"]["hostname"],
    app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
    consumer_timeout_ms=1000)
    logger.info("Retrieving Height and Weight at index %d" % index)
    index_b=0
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg['type'] == "Height and Weight":
                index_b = index_b + 1
                if index_b == index:
                    return msg['payload'], 200
    except:
        logger.error("No more messages found")  
    logger.error("Could not find Height and Weight Reading at index %d" % index)
    return { "message": "Not Found"}, 404


app = connexion.FlaskApp(__name__, specification_dir='')
if "TARGET_ENV" not in os.environ or os.environ["TARGET_ENV"] != "test":
    CORS(app.app)
    app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yml", base_path="/audit_log", strict_validation=True, validate_responses=True)


if __name__ == "__main__":
    app.run(port=9898)
