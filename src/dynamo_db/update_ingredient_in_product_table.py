import boto3
from boto3.dynamodb.conditions import Key, Attr
import time
from decimal import Decimal

# get the service resource.
dynamodb = boto3.resource('dynamodb')

# instantiate the table resource object
table = dynamodb.Table('skinglow-products')


def check_if_item_exists(pk, sk):
    result = table.query(
        KeyConditionExpression=Key('PK').eq(pk) & Key('SK').eq(sk)
    )

    if result['Count'] > 0:
        return True
    else:
        return False


def put_item_in_table(item):
    start_time = time.time()

    print('###########################')

    item_pk = int(item['PK'])
    item_sk = item['SK']

    is_duplicated = check_if_item_exists(item_pk, item_sk)

    if is_duplicated:
        print(f'[WARN] Omitted duplicated item [{item_pk}]')
        pass
    else:
        print(f'[LOG] Start putting item [{item_pk}] in DynamoDB')
        table.put_item(Item=item)

        execution_time = time.time() - start_time
        execution_time_rounded = round(execution_time, 2)
        print(f'[SUCCESS] Put item [{item_pk}] in {"--- %.2f seconds ---" % execution_time_rounded}')

    print('###########################')