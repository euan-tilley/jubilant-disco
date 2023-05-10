import boto3

def read_ssm_parameters(myNextToken='None'):
    while myNextToken:
        page_iterator = paginator.paginate(
            Path='path_to_the_parameters',
            Recursive=True,
            PaginationConfig={
                'MaxItems': 10,
                'PageSize': 10,
                'StartingToken': myNextToken
            }
        )

        for page in page_iterator:
            if 'NextToken' in page.keys():
                print('# This is a new page')
                myNextToken=page['NextToken']
                print(page['Parameters'])
            else:
                # Exit if there are no more pages to read
                myNextToken=False

session = boto3.session.Session()
client = session.client('rds')

all_cpg_groups = []
paginator = client.get_paginator('describe_db_parameter_groups')
response_iterator = paginator.paginate(Filters=[
                                        {'Name': 'engine',
                                            'Values': ['aurora-mysql']
                                        }])

for page in response_iterator:
    all_cpg_groups.extend(page['DBParameterGroups'])




# myNextToken='None'

# paginate = client.get_paginator('describe_db_parameter_groups')
# while myNextToken:
#     page_iterator = paginate.paginate(Filters=[
#                                     {'Name': 'engine',
#                                         'Values': ['aurora-mysql']
#                                     }],
#                                     PaginationConfig={
#                                         'MaxItems': 20,
#                                         'PageSize': 20,
#                                         'StartingToken': myNextToken
#                                     })

#     for page in page_iterator:
#         if 'Marker' in page.keys():
#             print('# This is a new page')
#             myNextToken=page['Marker']
#             all_cpg_groups.extend(page['DBParameterGroups'])
#         else:
#             # Exit if there are no more pages to read
#             myNextToken=False


print('here')
