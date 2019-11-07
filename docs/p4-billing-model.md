# DynamoDB Billing Model

DynamoDB currently offers two methods of billing:
	- Provisioned
	- Pay per Request (On-demand capacity)

## Provisioned

Provisioned DynamoDB capacity is the the more traditional approach to DynamoDB billing. It's also included in the [AWS free tier](https://aws.amazon.com/free/).

When you *provision* capacity on a DynamoDB table you specify how many read and write operations can be made against a table within one second. The more read and write units *provisioned* the more available throughput you have on your table.

Provisioned capacity can either remain the same or it can use auto-scaling.

When you provision a a capacity without auto scaling the table will run through a small amount of burst capacity proportional to the provisioned capacity and then start serving requests along the same speed as the provisioned capacity. When excess reads or writes from an SDK come in to an under-provisioned table they will use exponential backoff until they succeed or hit a max retries limit and fail.

### DynamoDB Auto Scaling

DynamoDB also has provisioned capacity that can scale automatically. In that model, you set a minimum and a maximum capacity for a table and DynamoDB will attempt to match your actual capacity requirements within that capacity range. This means it will manage increasing and decreasing provisioned capacity on the table periodically. Read more about this [here](https://aws.amazon.com/blogs/aws/new-auto-scaling-for-amazon-dynamodb/).

## Pay per Request

There are also options that don't take provisioned capacity into account *at all*. You can use pay per request pricing to pay for the actual consumed capacity of a DynamoDB table and not worry about provisioning the table at all. This method can be slightly more expensive per request but it can help you provide a better user experience because you can let AWS completely handle capacity planning for you.

### DynamoDB Reserved Capacity

If you have heavy utilization with DynamoDB you can pay upfront and commit to paying for a certain usage amount at a discounted rate. But you can only do this with provisioned capacity. As of right now you can do this with the Pay per Request, on-demand capacity model.

#### Demo Time - Implementing Pay-per-request On-demand Capacity

Let's see what the difference looks like between DynamoDB provisioned capacity and Pay-per-request capacity. You can see the code for this example [here](https://github.com/fernando-mc/dynamodb-training/) under examples-by-section and `p4-billing-model`.

First, I will going to create a DynamoDB table with the minium provisioned capacity using the `create_table.py` file. But you can also do this in the AWS console or in a new Serverless Framework service.

Then, I'm going to write a bunch of data from `songs.json` into the table over and over again until it starts to hit the table's actual capacity using the `overload.py` script.

After that we can change the table's billing method with `change_to_pay_per_request.py` or by updating it in the AWS console or with changes to `serverless.yml` and a redeploy with `serverless deploy`. If we keep running `overload.py` we should see changes to the performance of the write requests.

Make sure that if you try this on your own you don't run these scripts forever as that may drive up the cost of your DynamoDB bill.

For a more in-depth example of how to do this this you can look at [this post](https://serverless.com/blog/dynamodb-on-demand-serverless/) on how to implement these different billing options in your own Serverless Applications.
        
## Previous - [DynamoDB Table Basics](p3-table-basics.md)
## Next - [DynamoDB Indexes](p5-indexes.md)