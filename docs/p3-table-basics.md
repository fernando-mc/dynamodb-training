# DynamoDB Table Basics

In this section we'll look at a few core concepts of DynamoDB.

## Part 1 - Core Concepts

- Tables
- Items
- Attributes
- Primary Keys
	- Partition Keys (Hash Keys)
	- Sort Keys (Range Keys)
	- Simple Primary Keys (just partition keys)
	- Composite Primary Keys (partition and sort keys)

You can use [this](https://www.dynamodbguide.com/key-concepts) as a reference for these concepts.

## Demo 1 - AWS DynamoDB Console Demo 

- Creating a DynamoDB Table in the AWS Console
- Table keys
- Creating and editing items and attributes
- Item and attribute limitations

## Part 2 - Reads and Writes

- Reading items
- Strong vs. eventually consistent
- Writing items
- Atomic writes
- Conditional Writes
- Transactions

Writes
Atomic Writes
Conditional Writes
Transactions

### Atomic Writes (aka, Atomic Counters)

Imagine a DynamoDB item that has two attributes:

```json
{
    "siteUrl": "https://www.fernandomc.com/",
    "visits": "0"
}
```

Say we wanted to record all site visits and increment on top of this ongoing count. How could we do this with DynamoDB? Well, we could get the item, modify it, and then write it. But that would be two round trip operations and we would risk writing over someone other changes in the time between the operations. Instead, we can use an atomic write to avoid this.

Here's an example:

```py
import boto3
dynamodb = boto3.client('dynamodb')
response = dynamodb.update_item(
    TableName='siteVisits', 
    Key={
        'siteUrl':{'S': "https://www.fernandomc.com/"}
    },
    UpdateExpression='SET visits = visits + :inc',
    ExpressionAttributeValues={
        ':inc': {'N': '1'}
    },
    ReturnValues="UPDATED_NEW"
)
print("UPDATING ITEM")
print(response)
```

A [more detailed](https://www.fernandomc.com/posts/nandolytics-serverless-website-analytics/) demo of atomic counters.


### Conditional Writes

Another powerful tool to control your writing to a table are conditional writes. They can help you control if writes should occur based on the state of an item. For example, if an attribute already exists maybe they should not actually overwrite the item. This can be helpful if you need to do any sort of item locking and unlocking or if you simply don't want to overwrite some fields if they are already written. 

Maybe we're designing a music catalog and the 100th rating from a user is information we want to keep around to reward them later but our system sometimes sends two writes at once when a bunch of users rate a new song at the same time. Let's look at some Python code that would help us fix this with conditional writes:

```python
import boto3

dynamodb = boto3.client('dynamodb')

try:
    dynamodb.put_item(
		TableName="Music",
        Item={
            'HundredthUserRating': {'N': '9'},
            'HundredthUserEmail': {'S': 'music.lover98@gmail.com'},
        },
        ConditionExpression='attribute_not_exists(HundredthUserRating) AND attribute_not_exists(HundredthUserEmail)'
    )
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
        raise
```

This way, we can write our code to support writing this sort of information only if our conditions are satisfied. You can review [the documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html) for more information on the types of conditional writes supported.

### Transactions

In addition to conditional writes of single items, you also have the ability to use DynamoDB transactions to take all-or-nothing operations on items in one or more tables. This can be especially useful when fulfilling and managing orders or doing other tasks that might require multiple changes to take place simultaneously or not at all.

Here is an example of what this might look like to write with a transaction between two tables, though frequently you'll use this process on a single table.

```javascript
data = await dynamoDb.transactWriteItems({
    TransactItems: [
        {
            Update: {
                TableName: 'items',
                Key: { id: { S: itemId } },
                ConditionExpression: 'available = :true',
                UpdateExpression: 'set available = :false, ' +
                    'ownedBy = :player',
                ExpressionAttributeValues: {
                    ':true': { BOOL: true },
                    ':false': { BOOL: false },
                    ':player': { S: playerId }
                }
            }
        },
        {
            Update: {
                TableName: 'players',
                Key: { id: { S: playerId } },
                ConditionExpression: 'coins >= :price',
                UpdateExpression: 'set coins = coins - :price, ' +
                    'inventory = list_append(inventory, :items)',
                ExpressionAttributeValues: {
                    ':items': { L: [{ S: itemId }] },
                    ':price': { N: itemPrice.toString() }
                }
            }
        }
    ]
}).promise();
```


## Previous - [Important DynamoDB vs. SQL Considerations](p2-important-dynamodb-vs-sql-considerations.md)
## Next - [DynamoDB Billing Model](p4-billing-model.md)