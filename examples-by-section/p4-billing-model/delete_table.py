import boto3

dynamodb = boto3.client('dynamodb')

dynamodb.delete_table(TableName='Music')