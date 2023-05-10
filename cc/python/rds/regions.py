import argparse
import concurrent.futures
import time
import logging
import boto3
import botocore.exceptions
import botocore.errorfactory

session = boto3.session.Session()
rds_client = session.client('rds')

try:
    result = rds_client.describe_global_clusters(GlobalClusterIdentifier='sandbox-test-upgrade-aurora-global-cluster')
    # result = rds_client.describe_global_clusters(GlobalClusterIdentifier='sand1-app-aurora-db-aurora-cluster')
    secondary_rds_client = session.client('rds',region_name='eu-west-2')
except botocore.exceptions.ClientError as error:
    if error.response['Error']['Code'] == 'GlobalClusterNotFoundFault':
        print("NOT GLOBAL")
    else:
        raise error

print(result)