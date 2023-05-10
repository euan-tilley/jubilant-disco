# l = ["prod1-apiserver-prod-aurora-cluster","prod2-apiserver-prod-aurora-cluster"]

# print([m for m in l if '1' in m])
# print([m for m in l if '2' in m])

# data = {
#     "meters": [
#         {
#             "id": "1",
#             "registers": [
#                 {
#                     "reg_id": "1",
#                     "status": "B"
#                 },
#                 {
#                     "reg_id": "2",
#                     "status": "C"
#                 }
#             ]
#         }
#     ]
# }

# result = any(xds["status"] == "C" for meters in data.values() for ds in meters for xds in ds["registers"])

data = {
    "DBInstances": [
        {
            "DBInstanceIdentifier": "sand1-test-upgrade-sandbox-aurora-cluster-0",
            "DBInstanceClass": "db.r5.large",
            "Engine": "aurora-mysql",
            "DBInstanceStatus": "available",
            "MasterUsername": "root",
            "DBName": "test_upgrade",
            "Endpoint": {
                "Address": "sand1-test-upgrade-sandbox-aurora-cluster-0.cgivs49svu8n.eu-west-1.rds.amazonaws.com",
                "Port": 3306,
                "HostedZoneId": "Z29XKXDKYMONMX"
            },
            "AllocatedStorage": 1,
            "InstanceCreateTime": "2022-10-06T12:19:22.649000+00:00",
            "PreferredBackupWindow": "02:00-03:00",
            "BackupRetentionPeriod": 7,
            "DBSecurityGroups": [],
            "VpcSecurityGroups": [
                {
                    "VpcSecurityGroupId": "sg-0bef6db93bcea62f9",
                    "Status": "active"
                }
            ],
            "DBParameterGroups": [
                {
                    "DBParameterGroupName": "default.aurora-mysql5.7",
                    "ParameterApplyStatus": "pending-reboot"
                }
            ],
            "AvailabilityZone": "eu-west-1b",
            "DBSubnetGroup": {
                "DBSubnetGroupName": "test-upgrade",
                "DBSubnetGroupDescription": "Database subnet group for test-upgrade",
                "VpcId": "vpc-05b4aebd14ac877b1",
                "SubnetGroupStatus": "Complete",
                "Subnets": [
                    {
                        "SubnetIdentifier": "subnet-014357a0a066214b3",
                        "SubnetAvailabilityZone": {
                            "Name": "eu-west-1c"
                        },
                        "SubnetOutpost": {},
                        "SubnetStatus": "Active"
                    },
                    {
                        "SubnetIdentifier": "subnet-06008f2e5c5e103b0",
                        "SubnetAvailabilityZone": {
                            "Name": "eu-west-1a"
                        },
                        "SubnetOutpost": {},
                        "SubnetStatus": "Active"
                    },
                    {
                        "SubnetIdentifier": "subnet-0114320bdc09b7cc7",
                        "SubnetAvailabilityZone": {
                            "Name": "eu-west-1b"
                        },
                        "SubnetOutpost": {},
                        "SubnetStatus": "Active"
                    }
                ]
            },
            "PreferredMaintenanceWindow": "sun:05:00-sun:06:00",
            "PendingModifiedValues": {},
            "MultiAZ": False,
            "EngineVersion": "5.7.mysql_aurora.2.10.2",
            "AutoMinorVersionUpgrade": True,
            "ReadReplicaDBInstanceIdentifiers": [],
            "LicenseModel": "general-public-license",
            "OptionGroupMemberships": [
                {
                    "OptionGroupName": "default:aurora-mysql-5-7",
                    "Status": "in-sync"
                }
            ],
            "PubliclyAccessible": False,
            "StorageType": "aurora",
            "DbInstancePort": 0,
            "DBClusterIdentifier": "sand1-test-upgrade-sandbox-aurora-cluster",
            "StorageEncrypted": True,
            "KmsKeyId": "arn:aws:kms:eu-west-1:405805805891:key/51ad22df-e3ce-4d20-8f6d-cab839245381",
            "DbiResourceId": "db-CUCCRFAJYUJFE7LYZPR2F7OD4A",
            "CACertificateIdentifier": "rds-ca-2019",
            "DomainMemberships": [],
            "CopyTagsToSnapshot": False,
            "MonitoringInterval": 0,
            "PromotionTier": 0,
            "DBInstanceArn": "arn:aws:rds:eu-west-1:405805805891:db:sand1-test-upgrade-sandbox-aurora-cluster-0",
            "IAMDatabaseAuthenticationEnabled": False,
            "PerformanceInsightsEnabled": False,
            "DeletionProtection": False,
            "AssociatedRoles": [],
            "TagList": [
                {
                    "Key": "GithubRepo",
                    "Value": "terraform-aws-rds-aurora"
                },
                {
                    "Key": "GithubOrg",
                    "Value": "terraform-aws-modules"
                },
                {
                    "Key": "Example",
                    "Value": "test-upgrade"
                }
            ],
            "CustomerOwnedIpEnabled": False,
            "BackupTarget": "region",
            "NetworkType": "IPV4"
        },
        {
            "DBInstanceIdentifier": "sand1-test-upgrade-sandbox-aurora-cluster-1",
            "DBInstanceClass": "db.r5.large",
            "Engine": "aurora-mysql",
            "DBInstanceStatus": "available",
            "MasterUsername": "root",
            "DBName": "test_upgrade",
            "Endpoint": {
                "Address": "sand1-test-upgrade-sandbox-aurora-cluster-1.cgivs49svu8n.eu-west-1.rds.amazonaws.com",
                "Port": 3306,
                "HostedZoneId": "Z29XKXDKYMONMX"
            },
            "AllocatedStorage": 1,
            "InstanceCreateTime": "2022-10-06T12:15:39.003000+00:00",
            "PreferredBackupWindow": "02:00-03:00",
            "BackupRetentionPeriod": 7,
            "DBSecurityGroups": [],
            "VpcSecurityGroups": [
                {
                    "VpcSecurityGroupId": "sg-0bef6db93bcea62f9",
                    "Status": "active"
                }
            ],
            "DBParameterGroups": [
                {
                    "DBParameterGroupName": "default.aurora-mysql5.7",
                    "ParameterApplyStatus": "in-sync"
                }
            ],
            "AvailabilityZone": "eu-west-1a",
            "DBSubnetGroup": {
                "DBSubnetGroupName": "test-upgrade",
                "DBSubnetGroupDescription": "Database subnet group for test-upgrade",
                "VpcId": "vpc-05b4aebd14ac877b1",
                "SubnetGroupStatus": "Complete",
                "Subnets": [
                    {
                        "SubnetIdentifier": "subnet-014357a0a066214b3",
                        "SubnetAvailabilityZone": {
                            "Name": "eu-west-1c"
                        },
                        "SubnetOutpost": {},
                        "SubnetStatus": "Active"
                    },
                    {
                        "SubnetIdentifier": "subnet-06008f2e5c5e103b0",
                        "SubnetAvailabilityZone": {
                            "Name": "eu-west-1a"
                        },
                        "SubnetOutpost": {},
                        "SubnetStatus": "Active"
                    },
                    {
                        "SubnetIdentifier": "subnet-0114320bdc09b7cc7",
                        "SubnetAvailabilityZone": {
                            "Name": "eu-west-1b"
                        },
                        "SubnetOutpost": {},
                        "SubnetStatus": "Active"
                    }
                ]
            },
            "PreferredMaintenanceWindow": "sun:05:00-sun:06:00",
            "PendingModifiedValues": {},
            "MultiAZ": False,
            "EngineVersion": "5.7.mysql_aurora.2.10.2",
            "AutoMinorVersionUpgrade": True,
            "ReadReplicaDBInstanceIdentifiers": [],
            "LicenseModel": "general-public-license",
            "OptionGroupMemberships": [
                {
                    "OptionGroupName": "default:aurora-mysql-5-7",
                    "Status": "in-sync"
                }
            ],
            "PubliclyAccessible": False,
            "StorageType": "aurora",
            "DbInstancePort": 0,
            "DBClusterIdentifier": "sand1-test-upgrade-sandbox-aurora-cluster",
            "StorageEncrypted": True,
            "KmsKeyId": "arn:aws:kms:eu-west-1:405805805891:key/51ad22df-e3ce-4d20-8f6d-cab839245381",
            "DbiResourceId": "db-P7AZGOVTH333NSQ3RTBD5N4J7Q",
            "CACertificateIdentifier": "rds-ca-2019",
            "DomainMemberships": [],
            "CopyTagsToSnapshot": False,
            "MonitoringInterval": 0,
            "PromotionTier": 0,
            "DBInstanceArn": "arn:aws:rds:eu-west-1:405805805891:db:sand1-test-upgrade-sandbox-aurora-cluster-1",
            "IAMDatabaseAuthenticationEnabled": False,
            "PerformanceInsightsEnabled": False,
            "DeletionProtection": False,
            "AssociatedRoles": [],
            "TagList": [
                {
                    "Key": "GithubRepo",
                    "Value": "terraform-aws-rds-aurora"
                },
                {
                    "Key": "GithubOrg",
                    "Value": "terraform-aws-modules"
                },
                {
                    "Key": "Example",
                    "Value": "test-upgrade"
                }
            ],
            "CustomerOwnedIpEnabled": False,
            "BackupTarget": "region",
            "NetworkType": "IPV4"
        }
    ]
}

type(data)

result = any(groups["ParameterApplyStatus"] != "applying" for i in data['DBInstances'] for groups in i['DBParameterGroups'])

print(result)