import boto3
from botocore.exceptions import ClientError, WaiterError



# def wait_for_instance():
#     session = boto3.session.Session()
#     client = session.client('rds')

#     waiter = client.get_waiter('db_instance_available')
#     tries = 3
#     for i in range(3):
#         try:
#             waiter.wait(
#                 DBInstanceIdentifier='et-restore-test',
#                 WaiterConfig={
#                     'Delay': 2,
#                     'MaxAttempts': 2
#                 }
#             )

#             print("avaliable")
#         except ClientError as client_error:
#             if client_error.response['Error']['Code'] == 'ThrottlingException':
#                 if i < tries:
#                     print(client_error)
#                     continue
#                 else:
#                     raise        
#             else:
#                 raise

def wait_for_instance():
    session = boto3.session.Session()
    client = session.client('rds')

    waiter = client.get_waiter('db_instance_available')
    tries = 3
    while tries:
        tries -= 1
        try:
            waiter.wait(
                DBInstanceIdentifier='et-restore-test',
                WaiterConfig={
                    'Delay': 30,
                    'MaxAttempts': 120
                }
            )

            break
        except ClientError as client_error:
            if client_error.response['Error']['Code'] == 'ThrottlingException':
                print(client_error)
                continue
    else:
        raise EnvironmentError("Retried...")


try:
    wait_for_instance()
    print("available")
except Exception as error:
    print(error)