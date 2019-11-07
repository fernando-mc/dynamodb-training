import boto3

dynamodb = boto3.client('dynamodb')

dynamodb.update_table(
    TableName='Music',
	BillingMode='PAY_PER_REQUEST'
)