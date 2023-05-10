from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
import concurrent.futures
import logging
import boto3

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(threadName)-10s %(message)s', datefmt='%H:%M:%S')

def describe(rds_client):
    db_instance_name = "stg1-app-aurora-db-aurora-node-0"

    response = rds_client.describe_db_instances(DBInstanceIdentifier=db_instance_name)

    logging.info(response['DBInstances'][0]['DBInstanceStatus'])

session = boto3.session.Session()
client = session.client('rds')

describe(client)