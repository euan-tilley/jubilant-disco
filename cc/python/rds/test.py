#!/usr/bin/env python3

'''Script to upgrade rds clusters from 5.6 to 5.7'''

import argparse
import concurrent.futures
import time
import logging
import boto3

ENGINE_VERSION = "5.7.mysql_aurora.2.10.2"
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(threadName)-10s %(message)s', datefmt='%H:%M:%S')


def status(client, cluster):
    '''log status of cluster'''

    cluster_response = client.describe_db_clusters(DBClusterIdentifier=cluster)
    cluster_status = cluster_response['DBClusters'][0]['Status'] == 'available'
    cluster_engine = cluster_response['DBClusters'][0]['EngineVersion'] == ENGINE_VERSION
    cluster_param_group_status = all(groups["DBClusterParameterGroupStatus"] == "in-sync" for i in cluster_response['DBClusters'] for groups in i['DBClusterMembers'])

    instance_response = client.describe_db_instances(
                    Filters=[
                    {
                        'Name': 'db-cluster-id',
                        'Values': [
                            cluster,
                        ]
                    },
                ])

    instance_status = all(i['DBInstanceStatus'] == 'available' for i in instance_response['DBInstances'])
    instance_param_status = all(groups["ParameterApplyStatus"] == "n-sync" for i in instance_response['DBInstances'] for groups in i['DBParameterGroups'])

    if cluster_status and cluster_engine and cluster_param_group_status and instance_status and instance_param_status:
        logging.info("All good")
    else:
        raise Exception(f"{cluster}, "\
                        f"cluster available: {cluster_status}, "\
                        f"engine upgraded: {cluster_engine}, "\
                        f"param groups in-sync: {cluster_param_group_status}, "\
                        f"instances available: {instance_status}, "\
                        f"instance param groups in-sync: {instance_param_status}")


def main():
    '''main'''

    cluster = 'sand1-upgrade-test-aurora-cluster'

    session = boto3.session.Session()
    rds_client = session.client('rds')

    try:

        status(rds_client, cluster)

    except Exception as error:
        logging.error(f'Unexpected error {str(error)}')



if __name__ == '__main__':
    main()
