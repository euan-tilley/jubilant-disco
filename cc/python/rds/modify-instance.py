import argparse
import concurrent.futures
import time
import logging
import boto3
import botocore.exceptions
import botocore.errorfactory
from operator import itemgetter

ENGINE_VERSION = "5.7.mysql_aurora.2.10.2"

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
    instance_param_status = all(groups["ParameterApplyStatus"] == "in-sync" for i in instance_response['DBInstances'] for groups in i['DBParameterGroups'])

    if cluster_status and cluster_engine and cluster_param_group_status and instance_status and instance_param_status:
        print(f'{cluster} has been upgraded & parameter groups attached')
    else:
        print(f"{cluster}, cluster available: {cluster_status}, engine upgraded: {cluster_engine}, param groups in-sync: {cluster_param_group_status}, instances available: {instance_status}, instance param groups in-sync: {instance_param_status}")


def attach_db_param_group(instance, client):
    group = 'sand1-upgrade-test-aurora20221007090101582200000002'
    # group = 'default.aurora-mysql5.7'

    response = client.modify_db_instance(
                ApplyImmediately=True,
                DBInstanceIdentifier=instance,
                DBParameterGroupName=group)

    print(f"{response['DBInstance']['DBInstanceIdentifier']} attaching db parameter groups...")

def attach_cluster_param_group(cluster, client):
    '''attach custom parameter groups to cluster'''

    group = 'sand1-upgrade-test-aurora20221007090101579000000001'
    # group = 'default.aurora-mysql5.7'

    response = client.modify_db_cluster(
                ApplyImmediately=True,
                DBClusterIdentifier=cluster,
                DBClusterParameterGroupName=group)

    print(f"{response['DBCluster']['DBClusterIdentifier']} attaching cluster parameter groups...")

def wait(client):

    t_end = time.time() + 5 * 60
    while time.time() < t_end:
        response = client.describe_db_instances(
                Filters=[
                {
                    'Name': 'db-cluster-id',
                    'Values': [
                        'sand1-upgrade-test-aurora-cluster',
                    ]
                },
            ])

        reboot = all(groups["ParameterApplyStatus"] != "applying" for i in response['DBInstances'] for groups in i['DBParameterGroups'])

        # for instance in response['DBInstances']:
        #     for group in instance['DBParameterGroups']:
        #         print(f"{instance['DBInstanceIdentifier']} - {group['ParameterApplyStatus']}")
        #         reboot = group['ParameterApplyStatus'] != 'applying'

        if reboot:
            break

        print("Sleeping...")
        time.sleep(5)

def reboot_cluster_instances(cluster, client):
    '''Reboots clusters instances'''

    response = client.describe_db_clusters(DBClusterIdentifier=cluster)

    sorted_instances = sorted(response['DBClusters'][0]['DBClusterMembers'], key=itemgetter('IsClusterWriter'), reverse=True)

    for instance in sorted_instances:
        print(f'Rebooting {instance["DBInstanceIdentifier"]}')
        client.reboot_db_instance(
            DBInstanceIdentifier=instance['DBInstanceIdentifier'],
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
        # waiter.wait(DBInstanceIdentifier=instance['DBInstanceIdentifier'],
        #             WaiterConfig={
        #                 'Delay': 10,
        #                 'MaxAttempts': 30
        #             })

session = boto3.session.Session()
rds_client = session.client('rds')

attach_cluster_param_group('sand1-upgrade-test-aurora-cluster', rds_client)
time.sleep(5)
# reboot_cluster_instances('sand1-upgrade-test-aurora-cluster', rds_client)

attach_db_param_group('sand1-upgrade-test-aurora-node-0', rds_client)
attach_db_param_group('sand1-upgrade-test-aurora-node-1', rds_client)

wait(rds_client)

reboot_cluster_instances('sand1-upgrade-test-aurora-cluster', rds_client)

status(rds_client, 'sand1-upgrade-test-aurora-cluster')

# print('Read to reboot')

