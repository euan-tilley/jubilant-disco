#!/usr/bin/env python3

'''Script to upgrade rds clusters from 5.6 to 5.7'''

import time
import logging
import boto3
from botocore.exceptions import ClientError, WaiterError

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(threadName)-10s %(message)s', datefmt='%H:%M:%S')

def wait_until_db_cluster_ready(db_cluster_name):
    sleep_time = 5

    session = boto3.session.Session()
    rds_client = session.client('rds')

    # time.sleep(30) # this is added because sometimes cluster status not updated immediately when you modify it

    cluster_status_request = rds_client.describe_db_clusters(DBClusterIdentifier=db_cluster_name)

    t_end = time.time() + 60 * 60
    while time.time() < t_end:
        if cluster_status_request['DBClusters'][0]['Status'] != 'available':
            logging.info(f"{db_cluster_name} is available")
            break
        else:
            response  = rds_client.describe_events(SourceIdentifier=db_cluster_name, SourceType='db-cluster')
            if response['Events']:
               logging.info(f"updating... {response['Events'][-1]['Message']}")

            time.sleep(sleep_time)

    # except Exception as e:
    #     logging.info(f"An error occurred trying to get db cluster status, exiting the script. Error: { e }")

wait_until_db_cluster_ready('sand1-et-test-aurora-cluster')
# wait_until_db_cluster_ready('sand1-upgrade-test-aurora-cluster')