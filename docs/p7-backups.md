# DynamoDB Backups

There are a few different options for backing up data with DynamoDB. 

## Point-in-time Recovery (PITR)

Once a DynamoDB table is created you can enable continuous backups which allow you to restore a table to any point in time after those continuous backups were enabled. For an example of this you can review [this post](https://aws.amazon.com/blogs/aws/new-amazon-dynamodb-continuous-backups-and-point-in-time-recovery-pitr/).

## On-demand Backup and Restore

You can also create on-demand backups where you create a full backup of the table at any time. You can then restore from any on-demand backup even if the table is deleted.

## What's in a Backup?

- Data from the table
- Global secondary indexes (GSIs)
- Local secondary indexes (LSIs)
- The provisioned read and write capacity for the table

You will have to manually reconfigure any:

- Auto scaling policies
- AWS Identity and Access Management (IAM) policies
- Amazon CloudWatch metrics and alarms
- Tags
- Stream settings
- Time To Live (TTL) settings

## Previous - [DynamoDB Global Tables](p6-global-tables.md)
## Next - [DynamoDB Single Table Design - Demo](p8-single-table-design.md)
