import argparse
import re
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
import time
import logging
from operator import itemgetter
import boto3
import botocore.exceptions

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(threadName)-10s %(message)s', datefmt='%H:%M:%S')

def wait_for_cluster_attachment(cluster, client):
    '''Waits for cluster parameter groups to be attached'''

    t_end = time.time() + 10 * 60
    while time.time() < t_end:
        response = client.describe_db_clusters(DBClusterIdentifier=cluster)
        
        reboot = all(members["DBClusterParameterGroupStatus"] != "applying" for i in response['DBClusters'] for members in i['DBClusterMembers'])

        if reboot:
            break

        logging.info(f"{cluster} Waiting for cluster parameter group to attach...")
        time.sleep(15)


def wait_for_attachment(cluster, client):
    '''Waits for parameter groups to be attached'''

    t_end = time.time() + 5 * 60
    while time.time() < t_end:
        response = client.describe_db_instances(
                Filters=[
                {
                    'Name': 'db-cluster-id',
                    'Values': [
                        cluster,
                    ]
                },
            ])

        reboot = all(groups["ParameterApplyStatus"] != "applying" for i in response['DBInstances'] for groups in i['DBParameterGroups'])

        if reboot:
            break

        logging.info(f"{cluster} Waiting for parameter group attaching...")
        time.sleep(15)

def cluster_pg_name(cluster_name, client):
    '''Calculates cluster parameter group name from cluster name'''
    group_name = cluster_name[:cluster_name.rfind("-")]

    all_cpg_groups = []

    paginator = client.get_paginator('describe_db_cluster_parameter_groups')
    response_iterator = paginator.paginate()

    for page in response_iterator:
        all_cpg_groups.extend(page['DBClusterParameterGroups'])

    return [x['DBClusterParameterGroupName'] for x in all_cpg_groups if bool(re.search(f"{group_name}[0-9]+", x['DBClusterParameterGroupName']))]

def db_pg_name(cluster_name, client):
    '''Calculates db parameter group name from cluster name'''
    all_db_pg_groups = []

    group_name = cluster_name[:cluster_name.rfind("-")]

    paginator = client.get_paginator('describe_db_parameter_groups')
    response_iterator = paginator.paginate()

    for page in response_iterator:
        all_db_pg_groups.extend(page['DBParameterGroups'])

    return [x['DBParameterGroupName'] for x in all_db_pg_groups if bool(re.search(f"{group_name}[0-9]+", x['DBParameterGroupName']))]
    
def check_cluster_pg(cluster_name, client):
    '''Checks wether cluster parameter group is available'''

    cpg_groups = cluster_pg_name(cluster_name, client)

    if len(cpg_groups) == 1:
        return True, 'cluster pg available: True'
    else:
        return False, 'cluster pg available: False'

def check_db_pg(cluster_name, client):
    '''Checks wether db parameter group is available'''

    db_pg_groups = db_pg_name(cluster_name, client)

    if len(db_pg_groups) == 1:
        return True, 'db pg available: True'
    else:
        return False, 'db pg available: False'

def check_param_groups(cluster, client):
    '''Check wether cluster can be upgraded'''

    ok_to_upgrade = True

    (check_cluster_pg_ok, check_cluster_pg_msg) = check_cluster_pg(cluster, client)
    (check_db_pg_ok, check_db_pg_msg) = check_db_pg(cluster, client)

    if check_cluster_pg_ok is False or check_db_pg_ok is False:
        ok_to_upgrade = False

    logging.info(f'{cluster}, {check_cluster_pg_msg}, {check_db_pg_msg}')

    return ok_to_upgrade

def reboot_cluster_instances(cluster, client):
    '''Reboots clusters instances'''

    response = client.describe_db_clusters(DBClusterIdentifier=cluster)
    sorted_instances = sorted(response['DBClusters'][0]['DBClusterMembers'], key=itemgetter('IsClusterWriter'), reverse=True)

    for instance in sorted_instances:
        logging.info(f'{instance["DBInstanceIdentifier"]} rebooting...')
        client.reboot_db_instance(
            DBInstanceIdentifier=instance["DBInstanceIdentifier"],
            ForceFailover=False)

    waiter = client.get_waiter('db_instance_available')
    waiter.wait(Filters=[{
                    'Name': 'db-cluster-id',
                    'Values': [cluster]
                }],
                WaiterConfig={
                    'Delay': 15,
                    'MaxAttempts': 30
                })

def attach_db_param_group(cluster, instance, client):
    '''attach custom db parameter groups to instance'''

    response = client.modify_db_instance(
                ApplyImmediately=True,
                DBInstanceIdentifier=instance,
                DBParameterGroupName=db_pg_name(cluster, client)[0])

    logging.info(f"{response['DBInstance']['DBInstanceIdentifier']} attaching db parameter group...")

def attach_cluster_param_group(cluster, client):
    '''attach custom parameter groups to cluster'''

    response = client.modify_db_cluster(
                ApplyImmediately=True,
                DBClusterIdentifier=cluster,
                DBClusterParameterGroupName=cluster_pg_name(cluster, client)[0])

    logging.info(f"{response['DBCluster']['DBClusterIdentifier']} attaching cluster parameter group...")

def attach_param_groups(cluster, client):
    '''attach parameter groups to cluster & instances'''

    attach_cluster_param_group(cluster, client)

    response = client.describe_db_clusters(DBClusterIdentifier=cluster)

    for member in response['DBClusters'][0]['DBClusterMembers']:
        attach_db_param_group(cluster, member['DBInstanceIdentifier'], client)

    wait_for_cluster_attachment(cluster, client)
    wait_for_attachment(cluster, client)

    reboot_cluster_instances(cluster, client)
    logging.info(f"{cluster} - parameter groups attached & rebooted")
    status(client, cluster)

def status(client, cluster):
    '''log status of cluster'''

    time.sleep(5)

    cluster_response = client.describe_db_clusters(DBClusterIdentifier=cluster)
    cluster_status = cluster_response['DBClusters'][0]['Status'] == 'available'
    cluster_param_group_status = all(groups["DBClusterParameterGroupStatus"] == "in-sync"
                                        for i in cluster_response['DBClusters']
                                            for groups in i['DBClusterMembers'])

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
    instance_param_status = all(groups["ParameterApplyStatus"] == "in-sync"
                                        for i in instance_response['DBInstances']
                                        for groups in i['DBParameterGroups'])

    if cluster_status and cluster_param_group_status and instance_status and instance_param_status:
        logging.info(f"{cluster} available & in-sync")
    else:
        raise Exception(f"{cluster}, "\
                        f"cluster available: {cluster_status}, "\
                        f"param groups in-sync: {cluster_param_group_status}, "\
                        f"instances available: {instance_status}, "\
                        f"instance param groups in-sync: {instance_param_status}")
    
def main():
    '''main'''

    parser = argparse.ArgumentParser(description='Upgrade 5.6 RDS Cluster to 5.7')

    parser.add_argument('file', type=argparse.FileType('r'), help='file with list of clusters names to upgrade')
    parser.add_argument('-e', '--envname', required=True, help='Envname used to identify clusters')
    parser.add_argument('-r', '--region', default='eu-west-1',help='AWS region to run against')
    parser.add_argument('-c', '--check', action='store_true', help='check wether cluster can be upgraded')

    args = parser.parse_args()

    with args.file as f:
        cluster_list = list(filter(None, f.read().splitlines()))

    client_config = botocore.config.Config(
        max_pool_connections=50
    )

    session = boto3.session.Session()
    rds_client = session.client('rds', region_name=args.region, config=client_config)

    if args.check:
        with ThreadPoolExecutor(30) as executor:
            futures = [executor.submit(check_param_groups, f"{args.envname}-{cluster}-aurora-cluster", rds_client) for cluster in cluster_list]
            wait(futures)
    else:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(attach_param_groups, f"{args.envname}-{cluster}-aurora-cluster", rds_client) for cluster in cluster_list]
            wait(futures)

if __name__ == '__main__':
    main()
