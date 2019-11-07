# DynamoDB Streams
DynamoDB Streams Stuff
	Lambda, Elasticsearch, Algolia
	DynamoDB Auorora Sync code

## Demo 

An example of using DynamoDB streams to integrate between services is shown in the example code [here](https://github.com/fernando-mc/dynamodb-training/) under the examples by section in the `p9-dynamodb-streams` folder.

This folder contains two services:

- `service-with-ddb-table-for-stream` is a service with a DynamoDB table that outputs a Stream ARN for the table using the Serverless Dashboard `outputs` feature
- `service-with-stream-reader` loads the output from the first service and then has a stream processor to parse through the data.

Deploy the service with the DynamoDB table first, making sure that you've set it up with your own dashboard account. Then deploy the stream reader service with your own dashboard account. Assuming these two are both deployed in the same stage (`dev` by default) and region then you should have an output that is accessible by the other service. 

You can check this in the [Serverless Dashboard](http://dashboard.serverless.com/) by going to the service and reviewing the outputs for the service with the table.

With both services deployed, go ahead and add an item to the `aSimpleTable` table. The key we defined for the table was a simple primary key (just a partition key). The partition key attribute was called `someKeyName`. We can write some JavaScript to add an item to the table like this:

```js
// Load the AWS SDK for Node.js
var AWS = require('aws-sdk');
// Set the region 
AWS.config.update({region: 'us-east-1'});

// Create the DynamoDB service object
var ddb = new AWS.DynamoDB({apiVersion: '2012-08-10'});

var params = {
  TableName: 'aSimpleTable',
  Item: {
    'someKeyName' : {S: 'MyNewKey'},
    'data' : {S: 'Some new data'}
  }
};

// Call DynamoDB to add the item to the table
ddb.putItem(params, function(err, data) {
  if (err) {
    console.log("Error", err);
  } else {
    console.log("Success", data);
  }
});
```

We can also go directly to the table in the AWS console and add a new item or two. When we're done with this, we should be able to check inside the logs for our stream reader service to show the recent invocation from reading the stream! 

### Stream Reading into VPC Resources

For a more complex implementation of a stream reader that integrates with an Amazon Aurora RDS Resources you can take a look [here](https://github.com/fernando-mc/serverless-jams-stream-reader). This example assumes an output using the Serverless Dashboard outputs feature to share output values between services in the same region.

You may also end up wanting to stream data into a tool like ElasticSearch (also inside of an AWS VPC) or a third party service like [Algolia](https://www.algolia.com/) which simply requires an API key and a library to send data over from Lambda.

## Previous - [DynamoDB Single Table Design - Demo](p8-single-table-design.md)
## Next - [Recommended Resources](p10-resources.md)
