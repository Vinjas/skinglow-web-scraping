import boto3
from boto3.dynamodb.conditions import Key, Attr
import time


# get the service resource.
dynamodb = boto3.resource('dynamodb')

# instantiate the table resource object
table = dynamodb.Table('skinglow-products')


def query_ingredients():
    try:
        response = table.query(
            KeyConditionExpression=Key('year').eq(year)
        )
    except ClientError as err:
        logger.error(
            "Couldn't query for movies released in %s. Here's why: %s: %s", year,
            err.response['Error']['Code'], err.response['Error']['Message'])
        raise
    else:
        return response['Items']
