#!/usr/bin/env python3

'''Script to upgrade rds clusters from 5.6 to 5.7'''

import argparse
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
import time
import logging
from operator import itemgetter
import boto3
import botocore.exceptions

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(threadName)-10s %(message)s', datefmt='%H:%M:%S')

ENGINE_VERSION = "5.7.mysql_aurora.2.10.2"

def wait_until_db_cluster_ready(cluster_name, client):
    '''Wait for RDS cluster to become available'''

    sleep_time = 30
    wait_minutes = 60 * 60
    upgraded = False

    time.sleep(60) # this is added because sometimes cluster status not updated immediately when you modify it

    t_end = time.time() + wait_minutes
    while time.time() < t_end:
        cluster_status_request = client.describe_db_clusters(DBClusterIdentifier=cluster_name)
        if cluster_status_request['DBClusters'][0]['Status'] == 'available':
            logging.info(f"{cluster_name} is available")
            upgraded = True
            break
        else:
            response  = client.describe_events(SourceIdentifier=cluster_name, SourceType='db-cluster')
            if response['Events']:
                logging.info(f"{cluster_name} updating... {response['Events'][-1]['Message']}")

            time.sleep(sleep_time)

    if not upgraded:
        raise TimeoutError(f"Waited form more than {wait_minutes} minutes for cluster to upgrade")

def check_cluster(cluster_name, client):
    '''Checks wether the cluster is upgradable'''

    response = client.describe_db_clusters(DBClusterIdentifier=cluster_name)

    engine_upgradeable = True
    if response['DBClusters'][0]['Engine'] != 'aurora':
        engine_upgradeable = False

    cluster_available = True
    if response['DBClusters'][0]['Status'] != 'available':
        cluster_available = False

    upgradeable = True
    if engine_upgradeable is False or cluster_available is False:
        upgradeable = False

    return upgradeable, f'cluster available: {cluster_available}, engine upgradable: {engine_upgradeable}'

def check_global_cluster(cluster_name, client):
    '''Checks wether the cluster is upgradable'''

    response = client.describe_global_clusters(GlobalClusterIdentifier=cluster_name)

    engine_upgradeable = True
    if response['GlobalClusters'][0]['Engine'] != 'aurora':
        engine_upgradeable = False

    cluster_available = True
    if response['GlobalClusters'][0]['Status'] != 'available':
        cluster_available = False

    upgradeable = True
    if engine_upgradeable is False or cluster_available is False:
        upgradeable = False

    members = global_cluster_members(client, cluster_name)

    return members, upgradeable, f'global cluster available: {cluster_available}, engine upgradable: {engine_upgradeable}'

def global_cluster_members(client, cluster_name):
    '''get member of a global cluster'''

    response = client.describe_global_clusters(GlobalClusterIdentifier=cluster_name)

    members = []
    for member in response['GlobalClusters'][0]['GlobalClusterMembers']:
        members.append(member['DBClusterArn'].split(':')[-1])

    return members

def cluster_pg_name(cluster_name, client):
    '''Calculates cluster parameter group name from cluster name'''

    group_name = cluster_name[:cluster_name.rfind("-")]
    response = client.describe_db_cluster_parameter_groups(
        Filters=[
                {
                    'Name': 'engine',
                    'Values': [
                        'aurora-mysql',
                    ]
                },
            ]
        )
    all_cpg_groups = response['DBClusterParameterGroups']

    return [x['DBClusterParameterGroupName'] for x in all_cpg_groups if group_name in x['DBClusterParameterGroupName']]

def check_cluster_pg(cluster_name, client):
    '''Checks wether cluster parameter group is available'''

    cpg_groups = cluster_pg_name(cluster_name, client)

    if len(cpg_groups) == 1:
        return True, 'cluster pg available: True'
    else:
        return False, 'cluster pg available: False'

def primary_cluster_name(cluster_members):
    '''gets cluster identifier of primary cluster'''

    return [member for member in cluster_members if '1' in member][0]

def secondary_cluster_name(cluster_members):
    '''gets cluster identifier of secondary cluster'''

    return [member for member in cluster_members if '2' in member][0]

def check_cluster_pgs(cluster_members, primary_client, secondary_client):
    '''Checks wether cluster parameter group is available in primary & secondary regions'''

    primary_cpg_groups = cluster_pg_name(primary_cluster_name(cluster_members), primary_client)
    secondary_cpg_groups = cluster_pg_name(secondary_cluster_name(cluster_members), secondary_client)

    if len(primary_cpg_groups) == 1 and len(secondary_cpg_groups) == 1:
        return True, 'global cluster pgs available: True'
    else:
        return False, 'global cluster pgs available: False'

def db_pg_name(cluster_name, client):
    '''Calculates db parameter group name from cluster name'''
    group_name = cluster_name[:cluster_name.rfind("-")]
    response = client.describe_db_parameter_groups(
        Filters=[
                {
                    'Name': 'engine',
                    'Values': [
                        'aurora-mysql',
                    ]
                }
            ]
        )
    all_db_pg_groups = response['DBParameterGroups']
    return [x['DBParameterGroupName'] for x in all_db_pg_groups if group_name in x['DBParameterGroupName']]

def check_db_pg(cluster_name, client):
    '''Checks wether db parameter group is available'''

    db_pg_groups = db_pg_name(cluster_name, client)

    if len(db_pg_groups) == 1:
        return True, 'db pg available: True'
    else:
        return False, 'db pg available: False'

def check_db_pgs(cluster_members, primary_client, secondary_client):
    '''Checks wether db parameter group is available in primary & secondary regions'''

    primary_db_pg_groups = db_pg_name(primary_cluster_name(cluster_members), primary_client)
    secondary_db_pg_groups = db_pg_name(secondary_cluster_name(cluster_members), secondary_client)

    if len(primary_db_pg_groups) == 1 and len(secondary_db_pg_groups) == 1:
        return True, 'global db pgs available: True'
    else:
        return False, 'global db pgs available: False'

def check_upgradability(cluster, primary_rds_client, secondary_rds_client=None):
    '''Check wether cluster can be upgraded'''

    ok_to_upgrade = True

    if secondary_rds_client:
        (cluster_members, check_cluster_ok, check_cluster_msg) = check_global_cluster(cluster, primary_rds_client)
        (check_cluster_pg_ok, check_cluster_pg_msg) = check_cluster_pgs(cluster_members, primary_rds_client, secondary_rds_client)
        (check_db_pg_ok, check_db_pg_msg) = check_db_pgs(cluster_members, primary_rds_client, secondary_rds_client)
    else:
        (check_cluster_ok, check_cluster_msg) = check_cluster(cluster, primary_rds_client)
        (check_cluster_pg_ok, check_cluster_pg_msg) = check_cluster_pg(cluster, primary_rds_client)
        (check_db_pg_ok, check_db_pg_msg) = check_db_pg(cluster, primary_rds_client)

    if check_cluster_ok is False or check_cluster_pg_ok is False or check_db_pg_ok is False:
        ok_to_upgrade = False

    logging.info(f'{cluster}, Upgradable: {ok_to_upgrade}, {check_cluster_msg}, {check_cluster_pg_msg}, {check_db_pg_msg}')

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
                    'Delay': 10,
                    'MaxAttempts': 30
                })

def reboot_global_cluster(cluster, primary_client, secondary_client):
    '''reboot all instances in global cluster'''

    cluster_members = global_cluster_members(primary_client, cluster)

    reboot_cluster_instances(primary_cluster_name(cluster_members), primary_client)
    reboot_cluster_instances(secondary_cluster_name(cluster_members), secondary_client)

def upgrade_cluster(cluster, client):
    '''Upgrades clusters'''

    if check_upgradability(cluster, client):
        try:
            response = client.modify_db_cluster(
                            ApplyImmediately=True,
                            DBClusterIdentifier=cluster,
                            EngineVersion=ENGINE_VERSION,
                            AllowMajorVersionUpgrade=True,
                            DBClusterParameterGroupName=cluster_pg_name(cluster, client)[0],
                            DBInstanceParameterGroupName=db_pg_name(cluster, client)[0])

            logging.info(f"{response['DBCluster']['DBClusterIdentifier']} Upgrading...")

            wait_until_db_cluster_ready(cluster, client)

            reboot_cluster_instances(cluster, client)

            status(client, cluster)

        except Exception as error:
            logging.error(f'Unexpected error {str(error)}')

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
        time.sleep(5)

def attach_param_groups(cluster, client):
    '''attach parameter groups to cluster & instances'''

    attach_cluster_param_group(cluster, client)
    time.sleep(2)
    reboot_cluster_instances(cluster, client)

    response = client.describe_db_clusters(DBClusterIdentifier=cluster)

    for member in response['DBClusters'][0]['DBClusterMembers']:
        attach_db_param_group(cluster, member['DBInstanceIdentifier'], client)

    wait_for_attachment(cluster, client)

    reboot_cluster_instances(cluster, client)
    logging.info(f"{cluster} - parameter groups attached & rebooted")

def upgrade_global_cluster(cluster, primary_client, secondary_client):
    '''Upgrades clusters'''

    cluster_members = global_cluster_members(primary_client, cluster)

    if check_upgradability(cluster, primary_client, secondary_client):
        try:
            response = primary_client.modify_global_cluster(
                            GlobalClusterIdentifier=cluster,
                            EngineVersion=ENGINE_VERSION,
                            AllowMajorVersionUpgrade=True)

            logging.info(f"{response['GlobalCluster']['GlobalClusterIdentifier']} Upgrading...")

            wait_until_db_cluster_ready(primary_cluster_name(cluster_members), primary_client)
            logging.info(f'{cluster} upgraded')

            attach_param_groups(primary_cluster_name(cluster_members), primary_client)
            attach_param_groups(secondary_cluster_name(cluster_members), secondary_client)

            status(primary_cluster_name(cluster_members), primary_client)
            status(secondary_cluster_name(cluster_members), secondary_client)

            logging.info(f'{cluster} has been upgraded & parameter groups attached')

        except Exception as error:
            logging.error(f'Unexpected error {str(error)}')

def status(client, cluster):
    '''log status of cluster'''

    cluster_response = client.describe_db_clusters(DBClusterIdentifier=cluster)
    cluster_status = cluster_response['DBClusters'][0]['Status'] == 'available'
    cluster_engine = cluster_response['DBClusters'][0]['EngineVersion'] == ENGINE_VERSION
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

    parser = argparse.ArgumentParser(description='Upgrade 5.6 RDS Cluster to 5.7')

    parser.add_argument('file', type=argparse.FileType('r'), help='file with list of clusters names to upgrade')
    parser.add_argument('-c', "--check", action='store_true', help='check wether cluster can be upgraded')
    parser.add_argument('-r', "--reboot", action='store_true', help='reboot cluster instances')

    args = parser.parse_args()

    with args.file as f:
        cluster_list = list(filter(None, f.read().splitlines()))

    session = boto3.session.Session()
    primary_rds_client = session.client('rds', region_name='eu-west-1')

    global_clusters = []
    clusters = []
    for cluster in cluster_list:
        try:
            primary_rds_client.describe_global_clusters(GlobalClusterIdentifier=cluster)
            global_clusters.append(cluster)
            secondary_rds_client = session.client('rds', region_name='eu-west-2')
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'GlobalClusterNotFoundFault':
                clusters.append(cluster)
            else:
                raise error

    if args.check:
        with ThreadPoolExecutor() as executor:
            if len(global_clusters) > 0:
                futures = [executor.submit(check_upgradability, cluster, primary_rds_client, secondary_rds_client) for cluster in global_clusters]
            else:
                futures = [executor.submit(check_upgradability, cluster, primary_rds_client) for cluster in clusters]

            wait(futures)

    elif args.reboot:
        with ThreadPoolExecutor() as executor:
            if len(global_clusters) > 0:
                futures = [executor.submit(reboot_global_cluster, cluster, primary_rds_client, secondary_rds_client) for cluster in global_clusters]
            else:
                futures = [executor.submit(reboot_cluster_instances, cluster, primary_rds_client) for cluster in clusters]

            wait(futures)
    else:
        with ThreadPoolExecutor() as executor:
            if len(global_clusters) > 0:
                futures = [executor.submit(upgrade_global_cluster, cluster, primary_rds_client, secondary_rds_client) for cluster in global_clusters]
            else:
                futures = [executor.submit(upgrade_cluster, cluster, primary_rds_client) for cluster in clusters]

            wait(futures)

    logging.info('Finished')

if __name__ == '__main__':
    main()
