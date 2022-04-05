import yaml
import requests
import connexion
import logging.config
import json
from datetime import datetime
from platform import python_branch
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from apscheduler.schedulers.background import BackgroundScheduler
from base import Base
from stats import Stats
from flask_cors import CORS, cross_origin

global total
global total_hw

total = []
total_hw = []

'''Loading the app configuration file'''
with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())



'''Loading the logs configuration file'''
with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine("sqlite:///%s" % app_config["datastore"]["filename"])
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)








def get_stats():
    # session = DB_SESSION()
    # results = session.query(Stats).order_by(Stats.last_updated.dec())
    # session.close()
    # return results

    logger.info("\n******************* GET request has been started **************************\n")
    session = DB_SESSION()
    stats = session.query(Stats).order_by(Stats.last_updateds.desc()).first()
    if not stats:
        logger.error(f"\n*********************** No statistics exist ****************************\n")
        return 404, 
    else:
        result = {}
        result["num_a_g_readings"] = stats.num_a_g_readings
        result["max_a_readings"] = stats.max_a_readings
        result["num_h_w_readings"] = stats.num_h_w_readings
        result["max_h_readings"] = stats.max_h_readings
        result["max_w_readings"] = stats.max_w_readings
        result["last_updateds"] = stats.last_updateds
        print(result)

        logger.debug(f"\n*********************** Returning python dictionary of ****************************\n{result}")
        
        logger.info(f"\n*********************** Request has been completed ****************************\n")
        return result, 200



def populate_stats():

    global total
    global total_hw


    #logger message to show process has started
    logger.info("\n*******************Started the Periodic Statistic Processing**************************\n")

    #Read the default values from the sqlite database
    session = DB_SESSION()
    stats = session.query(Stats).order_by(Stats.last_updateds.desc()).first()

    if not stats:
        now = datetime.now()
        logger.info("\n*******************Adding Default values, Because database was empty**************************\n")
        #ADD DATA VALUES
        stats_add = Stats(num_a_g_readings = 0,
                          max_a_readings = 0,
                          num_h_w_readings = 0,
                          max_h_readings = 0,
                          max_w_readings = 0,
                          last_updateds = now)
        session.add(stats_add)
        session.commit()
        session.close()
        # time_to_put = stats_add.last_updateds.strftime(f"%Y-%m-%dT%H:%M:%SZ")
        return 
    else:
        result = {}
        result["num_a_g_readings"] = stats.num_a_g_readings
        result["max_a_readings"] = stats.max_a_readings
        result["num_h_w_readings"] = stats.num_h_w_readings
        result["max_h_readings"] = stats.max_h_readings
        result["max_w_readings"] = stats.max_w_readings
        result["last_updateds"] = stats.last_updateds
        time_to_put = result["last_updateds"].strftime(f"%Y-%m-%dT%H:%M:%SZ")
        print(time_to_put)
        # return
    



    
    now = datetime.now()  
    
    current_timestamp = str(now.strftime(f"%Y-%m-%dT%H:%M:%S"))    
    # print(time_to_put)
    
    # print(f"{stats.last_updateds}*************")

    
    # r_ag = requests.get("http://localhost:8090/readings/age_n_gender", params={'timestamp': time_to_put})
    r_ag = requests.get(app_config["eventstore"]["url"] + 
                        "/readings/age_n_gender?timestamp=" + 
                        time_to_put + "&end_timestamp=" + current_timestamp)
    
    if r_ag.status_code != 200:
        logger.error(f"\n******************* Storage service returns a status code other that 200 **************************\n")
    else:    
        # # my_json_ag = json.loads(r_ag.content.decode('utf8').replace("'", '"'))
        my_json_ag = r_ag.json()
        # if len(total) == 0:
        #     lent = 0 
        #     total.append(my_json_ag)
        #     logger.info(f"\n******************* Recieved an event of having {len(my_json_ag)} new results **************************\n")
        # else:
        #     # print(f"{total[0]}\n")
        #     lent = len(total[0])
        #     # print(f"{my_json_ag}\n")
        #     total[0] = total[0] + my_json_ag
        #     # print(f"{total[0]}@@@@@@@@@@@@@@@@@@@")
        #     logger.info(f"\n******************* Recieved an event of having {len(my_json_ag)} new results **************************\n")
        logger.info(f"\n******************* Recieved an event of having {len(my_json_ag)} new results **************************\n")





    # r_hw = requests.get("http://localhost:8090/readings/height_n_weight", params={'timestamp': time_to_put})
    r_hw = requests.get(app_config["eventstore"]["url"] + 
                        "/readings/height_n_weight?timestamp=" + 
                        time_to_put + "&end_timestamp=" + current_timestamp)
    
    if r_hw.status_code != 200:
        logger.error(f"\n******************* Storage service returns a status code other that 200 **************************\n")
    else:
        my_json_hw = r_hw.json()
        # if len(total_hw) == 0:
        #     lent_hw = 0 
        #     total_hw.append(my_json_hw)
        #     logger.info(f"\n******************* Recieved an event of having {len(my_json_hw)} results **************************\n")
        # else:
        #     lent_hw = len(total_hw[0])
        #     total_hw[0] = total_hw[0] + my_json_hw
        logger.info(f"\n******************* Recieved an event of having {len(my_json_hw)} results **************************\n")





    """Code to write the statistical vlaues to the sqlite databae"""
    if len(my_json_ag) != 0 and len(my_json_hw) != 0:
        # for item in my_json_ag:
        #     logger.debug(f"\n******************* Recieved a Age and Reading event for stats of having trace_id of {item['trace_id']} **************************\n")

        # for item in my_json_hw:
        #     logger.debug(f"\n******************* Recieved a Height and Weight event for stats of having trace_id of {item['trace_id']} **************************\n")


        new_stats = {}
        new_stats["num_a_g_readings"] = len(my_json_ag) + result['num_a_g_readings']
        new_stats["num_h_w_readings"] = len(my_json_hw) + result['num_h_w_readings']

        seq_a = [x['user_age'] for x in my_json_ag]
        new_stats["max_a_readings"] = max(seq_a)

        seq_h = [x['user_height'] for x in my_json_hw]
        new_stats["max_h_readings"] = max(seq_h)


        seq_w = [x['user_weight'] for x in my_json_hw]
        new_stats["max_w_readings"] = max(seq_w)

        curr_date_time = str(now.strftime(f"%Y-%m-%dT%H:%M:%S"))
        new_stats["last_updateds"] = curr_date_time

        print(new_stats)
        
        
        session = DB_SESSION()

        stats_to_be_added = Stats(num_a_g_readings = new_stats["num_a_g_readings"],
                                max_a_readings = new_stats["max_a_readings"],
                                num_h_w_readings = new_stats["num_h_w_readings"],
                                max_h_readings = new_stats["max_h_readings"],
                                max_w_readings = new_stats["max_w_readings"],
                                last_updateds = datetime.strptime(new_stats["last_updateds"], f"%Y-%m-%dT%H:%M:%S"))


        session.add(stats_to_be_added)

        session.commit()
        session.close()

    elif len(my_json_ag) != 0 and len(my_json_hw) == 0:
        new_stats = {}
        new_stats["num_a_g_readings"] = len(my_json_ag) + result['num_a_g_readings']
        new_stats["num_h_w_readings"] = len(my_json_hw) + result['num_h_w_readings']

        seq_a = [x['user_age'] for x in my_json_ag]
        new_stats["max_a_readings"] = max(seq_a)

        # seq_h = [x['user_height'] for x in my_json_hw]
        new_stats["max_h_readings"] = 0 


        # seq_w = [x['user_weight'] for x in my_json_hw]
        new_stats["max_w_readings"] = 0

        curr_date_time = str(now.strftime(f"%Y-%m-%dT%H:%M:%S"))
        new_stats["last_updateds"] = curr_date_time

        print(new_stats)
        
        
        session = DB_SESSION()

        stats_to_be_added = Stats(num_a_g_readings = new_stats["num_a_g_readings"],
                                max_a_readings = new_stats["max_a_readings"],
                                num_h_w_readings = new_stats["num_h_w_readings"],
                                max_h_readings = new_stats["max_h_readings"],
                                max_w_readings = new_stats["max_w_readings"],
                                last_updateds = datetime.strptime(new_stats["last_updateds"], f"%Y-%m-%dT%H:%M:%S"))


        session.add(stats_to_be_added)

        session.commit()
        session.close()


    elif len(my_json_ag) == 0 and len(my_json_hw) != 0:
        new_stats = {}
        new_stats["num_a_g_readings"] = len(my_json_ag) + result['num_a_g_readings']
        new_stats["num_h_w_readings"] = len(my_json_hw) + result['num_h_w_readings']

        # seq_a = [x['user_age'] for x in my_json_ag]
        new_stats["max_a_readings"] = 0

        seq_h = [x['user_height'] for x in my_json_hw]
        new_stats["max_h_readings"] = max(seq_h) 


        seq_w = [x['user_weight'] for x in my_json_hw]
        new_stats["max_w_readings"] = max(seq_w)

        curr_date_time = str(now.strftime(f"%Y-%m-%dT%H:%M:%S"))
        new_stats["last_updateds"] = curr_date_time

        print(new_stats)
        
        
        session = DB_SESSION()

        stats_to_be_added = Stats(num_a_g_readings = new_stats["num_a_g_readings"],
                                max_a_readings = new_stats["max_a_readings"],
                                num_h_w_readings = new_stats["num_h_w_readings"],
                                max_h_readings = new_stats["max_h_readings"],
                                max_w_readings = new_stats["max_w_readings"],
                                last_updateds = datetime.strptime(new_stats["last_updateds"], f"%Y-%m-%dT%H:%M:%S"))


        session.add(stats_to_be_added)

        session.commit()
        session.close()
    else:
        session = DB_SESSION()
        curr_date_time = str(now.strftime(f"%Y-%m-%dT%H:%M:%S"))
        stats_to_be_added = Stats(num_a_g_readings = result['num_a_g_readings'],
                                max_a_readings = 0,
                                num_h_w_readings = result['num_h_w_readings'],
                                max_h_readings = 0,
                                max_w_readings = 0,
                                last_updateds = datetime.strptime(curr_date_time, f"%Y-%m-%dT%H:%M:%S"))


        session.add(stats_to_be_added)

        session.commit()
        session.close()







def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats, 
                  'interval', 
                  seconds=app_config['scheduler']['period_sec'])
    sched.start()

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)


if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100)
