cluster_details = {
    "transaction_monitoring": {
        "actual": {
            "aurora_instances": 1,
            "instance_type": "db.r2.large",
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

# all = []
# for c in cluster_details.values():
#     for m in c['actual']['cluster_members']:
#         all.append(m['instance_identifier'])

all = [m['instance_identifier'] for c in cluster_details.values() for m in c['actual']['cluster_members']]

readers = [m['instance_identifier'] for c in cluster_details.values() for m in c['actual']['cluster_members'] if m['is_writer'] is False]

for c in cluster_details.values():
    if c['expected']['instance_type'] != c['actual']['instance_type']:
        up = [(m['instance_identifier'],c['actual']['instance_type']) for m in c['actual']['cluster_members']]

create_readers = [c for c in cluster_details.values() if c['actual']['aurora_instances'] < c['expected']['aurora_instances']]

# up = [(m['instance_identifier'],c['actual']['instance_type']) for c in cluster_details.values() if c['expected']['instance_type'] != c['actual']['instance_type'] for m in c['actual']['cluster_members']]

# readers = []
# for c in cluster_details.values():
#     for m in c['actual']['cluster_members']:
#         if m['is_writer'] is False:
#             readers.append(m['instance_identifier'])

diff = set(all) - set(readers)

f = [(a, "TEST") for a in all]

for d in diff:
    print(d[0],d[1])

print(all, readers, diff)
print(type(diff))