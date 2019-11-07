# DynamoDB Global Tables

When developing applications that need to be exceptionally resilient and have very low latency you may want to use [DynamoDB Global Tables](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html). 

These tables are essentially a managed way to have one DynamoDB synced between multiple AWS regions around the world. The data in the table in one region is propagated between tables in other regions using [DynamoDB streams](p9-dynamodb-streams.md). This can be useful if you have an application service in one region performing and maybe need to shift the workload to another region to mitigate the failures.

This style of multi-region architecture comes with a decent amount of overhead but depending on how critical a service may be it can be useful to consider. For more details you can look at the AWS blog post [here](https://aws.amazon.com/blogs/database/how-to-use-amazon-dynamodb-global-tables-to-power-multiregion-architectures/).

In my experience, multi-region architectures like this are somewhat less common, especially for newer products and services.

## Previous - [DynamoDB Indexes](p5-indexes.md)
## Next - [DynamoDB Backups](p7-backups.md)
