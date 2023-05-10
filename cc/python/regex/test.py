import re

all_db_pg_groups = [
    {
        "DBClusterParameterGroupName": "default.aurora5.6",
        "DBParameterGroupFamily": "aurora5.6",
        "Description": "Default cluster parameter group for aurora5.6",
        "DBClusterParameterGroupArn": "arn:aws:rds:eu-west-1:606009918109:cluster-pg:default.aurora5.6"
    },
    {
        "DBClusterParameterGroupName": "default.aurora-mysql5.7",
        "DBParameterGroupFamily": "aurora-mysql5.7",
        "Description": "Default cluster parameter group for aurora-mysql5.7",
        "DBClusterParameterGroupArn": "arn:aws:rds:eu-west-1:606009918109:cluster-pg:default.aurora-mysql5.7"
    },
    {
        "DBClusterParameterGroupName": "default.aurora-mysql8.0",
        "DBParameterGroupFamily": "aurora-mysql8.0",
        "Description": "Default cluster parameter group for aurora-mysql8.0",
        "DBClusterParameterGroupArn": "arn:aws:rds:eu-west-1:606009918109:cluster-pg:default.aurora-mysql8.0"
    },
    {
        "DBClusterParameterGroupName": "stg1-account-settings-trust-aurora20220921081044842300000002",
        "DBParameterGroupFamily": "aurora-mysql5.7",
        "Description": "stg1-account-settings-trust-aurora-cluster-parameter-group",
        "DBClusterParameterGroupArn": "arn:aws:rds:eu-west-1:606009918109:cluster-pg:stg1-account-settings-trust-aurora20220921081044842300000002"
    },
    {
        "DBClusterParameterGroupName": "stg1-et-test-aurora20220921081044842300000002",
        "DBParameterGroupFamily": "aurora-mysql5.7",
        "Description": "stg1-account-settings-trust-aurora-cluster-parameter-group",
        "DBClusterParameterGroupArn": "arn:aws:rds:eu-west-1:606009918109:cluster-pg:stg1-account-settings-trust-aurora20220921081044842300000002"
    },
    {
        "DBClusterParameterGroupName": "stg1-et-test-eight-aurora20220921081044842300000003",
        "DBParameterGroupFamily": "aurora-mysql5.7",
        "Description": "stg1-account-settings-trust-aurora-cluster-parameter-group",
        "DBClusterParameterGroupArn": "arn:aws:rds:eu-west-1:606009918109:cluster-pg:stg1-account-settings-trust-aurora20220921081044842300000002"
    }
]

# s1 = "stg1-et-test-eigth-aurora20230328102044860500000001"
group_name = "stg1-et-test-eight-aurora"

print([x['DBClusterParameterGroupName'] for x in all_db_pg_groups if bool(re.search(f"{group_name}[0-9]+", x['DBClusterParameterGroupName']))])
# r = re.search(f"{group_name}[0-9]+", s1)
# r = bool(re.search(f"{group_name}[0-9]+", s1))
# print(r)