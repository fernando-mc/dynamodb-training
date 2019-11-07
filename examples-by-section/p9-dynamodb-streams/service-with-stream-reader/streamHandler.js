var AWS = require("aws-sdk");
  
exports.handler = async (event, context) => {
    console.log(event)
    const records = await event.Records;
    console.log(records)
    for (record in records) { 
        console.log('Stream record: ', JSON.stringify(records[record], null, 2));
        if (records[record].eventName == 'INSERT' || records[record].eventName == 'MODIFY') {
            var newRecord = records[record].dynamodb.NewImage;
            console.log(JSON.stringify(newRecord));
            // Do something else with the data when it is an INSERT or MODIFICATION
            // For example, email a user a welcome email on an insert
        }
    }
}