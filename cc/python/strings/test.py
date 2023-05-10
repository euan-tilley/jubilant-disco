# s='/aws/rds/cluster/stg1-account-settings-trust-aurora-cluster/general'

# s1='stg1-account-settings-trust-aurora-cluster'

# print(s.split('/')[-2])

# print(s1.replace("-",""))


# cluster_name = "prod-web-aurora-db"
cluster_name = "prod-apiserver-prod-aurora-global-cluster"

# group_name = cluster_name[:cluster_name.rfind("-")]

c = cluster_name.split('-')
del c[-3:]
c.pop(0)
print('_'.join(c))
