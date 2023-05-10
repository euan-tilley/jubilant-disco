#!/bin/bash

# cluster_pg="sand1-test-upgrade-sandbox-aurora20221006121006129300000002"
# db_pg="sand1-test-upgrade-sandbox-aurora20221006121006129100000001"

cluster_pg="default.aurora-mysql5.7"
db_pg="default.aurora-mysql5.7"

aws rds modify-db-cluster --db-cluster-identifier sand1-test-upgrade-sandbox-aurora-cluster --db-cluster-parameter-group-name "$cluster_pg" --apply-immediately

aws rds  modify-db-instance --db-instance-identifier sand1-test-upgrade-sandbox-aurora-cluster-0 --db-parameter-group-name "$db_pg" --apply-immediately
aws rds wait db-instance-available --db-instance-identifier sand1-test-upgrade-sandbox-aurora-cluster-0
aws rds  modify-db-instance --db-instance-identifier sand1-test-upgrade-sandbox-aurora-cluster-1 --db-parameter-group-name "$db_pg" --apply-immediately
aws rds wait db-instance-available --db-instance-identifier sand1-test-upgrade-sandbox-aurora-cluster-1

aws rds reboot-db-instance --db-instance-identifier sand1-test-upgrade-sandbox-aurora-cluster-0
aws rds wait db-instance-available --db-instance-identifier sand1-test-upgrade-sandbox-aurora-cluster-0
aws rds reboot-db-instance --db-instance-identifier sand1-test-upgrade-sandbox-aurora-cluster-1
aws rds wait db-instance-available --db-instance-identifier sand1-test-upgrade-sandbox-aurora-cluster-1
