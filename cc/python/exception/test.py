#!/usr/bin/env python3

import time
import logging
import boto3
from botocore.exceptions import RefreshWithMFAUnsupportedError

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(threadName)-10s %(message)s', datefmt='%H:%M:%S')

def wait():

    session = boto3.session.Session(profile_name='sandbox')
    client = session.client('rds')

    cluster_name = 'sand1-et-test-aurora-cluster'

    sleep_time = 60
    wait_minutes = 60 * 70

    t_end = time.time() + wait_minutes
    while time.time() < t_end:
        try:
            cluster_status_request = client.describe_db_clusters(DBClusterIdentifier=cluster_name)
            logging.info('Made "descibe_db_clusters" request...')

            response  = client.describe_events(SourceIdentifier=cluster_name, SourceType='db-cluster')
            logging.info('Made "describe_events" request...')

            time.sleep(sleep_time)
        except RefreshWithMFAUnsupportedError as refresh_error:
            logging.error(f'In while - {str(refresh_error)}')
            raise

try:
    wait()
    print('After wait function call')
except Exception as error:
    logging.error(f'In main - {str(error)}')
