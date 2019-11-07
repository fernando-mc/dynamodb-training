# DynamoDB Single Table Design

This is where things get weird. In most previous examples we've used relatively simple DynamoDB tables with straightforward use cases and data models. But what happens when you try to model typical relational style access patterns against a more complex data set? Well, in that case you'll need to stop and think for a moment before you create your service.

With a combination of secondary indexes and a technique called index overloading, DynamoDB can actually be used to model lots of different access patterns - as long as you take the time to think about those patterns when designing your table.

We'll be following the steps and demo used in [this post](https://www.trek10.com/blog/dynamodb-single-table-relational-modeling/) for working with DynamoDB. I've put the modified code we need in [the demos](https://github.com/fernando-mc/dynamodb-training/) for this section. For this demo, I'm using PAY_PER_REQUEST pricing so the demo may cost a few pennies to run.

To recap, there are a few steps we need to take when modeling our data in DynamoDB:

## Step 1 - Define Our Access Patterns

We need to model our entire table around the access patterns we require. We can't take the SQL approach and define keys that we can loosely optimize unknown access patterns around. Instead, for each new service, we think about all the queries and relationships we need and how we can support them in a single table design. Later on, we may include additional global secondary indexes to help us with this process or substantially different services with unrelated data may split into other services.

## Step 2 - Overload Our Attributes and Indexes

We'll want to use generic index names like `pk` for the partition key and `sk` for the sort key. We'll also have a `data` attribute. In the northwind example, we use these three generic attributes to support the main table (which uses `pk` as a partition key and `sk` as a sort key) and one GSI (which uses `sk` as a partition key and `data` as a sort key). The other attributes in the table can be anything else - we're not currently using them to query on.

## Step 3 - Create Records for Each Entity

In the northwind example - For every Customer, for every Order, for every Shipper - we create an entirely new record in the DynamoDB table.

The `pk` attribute will be key of the relational record (the orderID) and the `sk` and `data` attributes will differ depending on how we use them to help us construct access patterns.

## Step 4 - Modeling Many-to-Many Relationships

For the order details relationship we insert multiple records - one for each product ordered in the order. We're effectively writing a substantial amount more data into the table than we would in a SQL database. But in exchange we can perform lookups exceptionally fast.

## Step 5 - Add More GSIs for Additional Usage Patterns

Sometimes, you'll need more GSIs to support access patterns that were previously unthought of. That's when you might modify the table and bring in another GSI.

## Previous - [DynamoDB Backups](p7-backups.md)
## Next - [DynamoDB Streams](p9-dynamodb-streams.md)
