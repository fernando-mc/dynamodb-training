import boto3

dynamodb = boto3.client('dynamodb')

dynamodb.create_table(
    TableName='Music',
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    },
    AttributeDefinitions=[
        {
            'AttributeName': 'Artist',
            'AttributeType': 'S'
        },
    ],
    KeySchema=[
        {
            'AttributeName': 'Artist',
            'KeyType': 'HASH'
        },
    ],
)
