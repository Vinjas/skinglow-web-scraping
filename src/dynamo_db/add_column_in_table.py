import boto3

# get the service resource.
dynamodb = boto3.resource('dynamodb')


def add_column_in_table(pk, sk, column, table_name, data):
    print('###########################')

    # instantiate the table resource object
    table = dynamodb.Table(table_name)

    response = table.query(
        TableName=table_name,
        KeyConditionExpression="#pk = :pk And #sk = :sk",
        ExpressionAttributeValues={
            ":pk": int(pk),
            ":sk": sk
        },
        ExpressionAttributeNames={
            "#pk": "PK",
            "#sk": "SK"
        }
    )

    item = response['Items'][0]

    item[column] = data

    table.put_item(Item=item)

    print(f'[SUCCESS] Put item {pk} in table')


add_column_in_table(47860, "product#data_EN", "key-ingredients", "skinglow-products", [{"test": "enabled", "reasons": ["many"]}])
