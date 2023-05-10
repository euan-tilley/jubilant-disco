cluster_details = {
    "transaction_monitoring": {
        "actual": {
            "aurora_instances": 2,
            "instance_type": "db.t3.medium",
            "performance_insights_enabled": False,
            "cluster_members": [
                {
                    "instance_identifier": "sand1-transaction-monitoring-aurora-node-1",
                    "is_writer": False
                },
                {
                    "instance_identifier": "sand1-transaction-monitoring-aurora-node-0",
                    "is_writer": True
                }
            ],
            "reader_instance": "sand1-transaction-monitoring-aurora-node-1"
        },
        "expected": {
            "aurora_instances": 2,
            "instance_type": "db.r4.large",
            "performance_insights_enabled": False
        },
        "cluster_identifier": "sand1-transaction-monitoring-aurora-cluster"
    },
    "web-aurora-db": {
        "actual": {
            "aurora_instances": 1,
            "instance_type": "db.t3.medium",
            "performance_insights_enabled": False,
            "cluster_members": [
                {
                    "instance_identifier": "sand1-web-aurora-db-aurora-node-0",
                    "is_writer": True
                }
            ],
            "reader_instance": None
        },
        "expected": {
            "aurora_instances": 1,
            "instance_type": "db.t3.medium",
            "performance_insights_enabled": False
        },
        "cluster_identifier": "sand1-web-aurora-db-aurora-cluster"
    }
}

instances = []
for cluster, details in cluster_details.items():
    if details['actual']['instance_type'] == 'db.t3.medium':
        for member in details['actual']['cluster_members']:
            instances.append(member)



# r = [(k,v) for k,v in cluster_details.items() if v['actual']['instance_type'] ==  'db.t3.medium']

print(instances)