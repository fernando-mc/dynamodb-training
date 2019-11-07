# Deploying a New DynamoDB Table

Let's take a look at the steps required to deploy a simple DynamoDB table. Don't worry too much about how "attributes" and "keys" work for DynamoDB at this point. We'll look more at them soon.

## Updating serverless.yml

Let's start with a simple Node.js service we generate from running the `serverless` command. You should end up with a handler.js and something that looks like the top part of the below code:

```yaml
# Example node.js service code generated from running the `serverless` command

service: simple-ddb-table
app: simple-ddb-table-app
org: workshop

provider:
  name: aws
  runtime: nodejs10.x

functions:
  hello:
    handler: handler.hello

# Add this resources section to include a table
resources:
  Resources:
    someTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: aSimpleTable
        AttributeDefinitions:
          - AttributeName: someKeyName
            AttributeType: S
        KeySchema:
          - AttributeName: someKeyName
            KeyType: HASH
        ProvisionedThroughput:
          ReadCapacityUnits: 1
          WriteCapacityUnits: 1
```

Then add in the `resources` section to the bottom of the `serverless.yml` file and run `serverless deploy` to deploy the service and the table.

When it's done, it should automatically be deployed into a `dev` stage. But let's say we're ready to deploy it to production too and we run `serverless deploy --stage prod`. What happens?

We probably end up seeing something like this:

```
Serverless: Operation failed!
Serverless: View the full error output: https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stack/detail?stackId=arn%3Aaws%3Acloudformation%3Aus-east-1%3A757370802528%3Astack%2Fsimple-ddb-table-prod%2F60f1f120-010e-11ea-ba36-0e348661d726
Serverless: Publishing service to the Serverless Dashboard...
Serverless: Successfully published your service to the Serverless Dashboard: https://dashboard.serverless.com/tenants/workshop/applications/simple-ddb-table-app/services/simple-ddb-table/stage/prod/region/us-east-1
 
  Serverless Error ---------------------------------------
 
  An error occurred: someTable - aSimpleTable already exists in stack arn:aws:cloudformation:us-east-1:757370802528:stack/simple-ddb-table-dev/28ff4790-010e-11ea-912a-12c270bd7978.
 
  Get Support --------------------------------------------
     Docs:          docs.serverless.com
     Bugs:          github.com/serverless/serverless/issues
     Issues:        forum.serverless.com
 
  Your Environment Information ---------------------------
     Operating System:          darwin
     Node Version:              6.10.3
     Framework Version:         1.55.1
     Plugin Version:            3.2.1
     SDK Version:               2.1.2
```

The part about `aSimpleTable already exists in stack . . .` means that the table we created inside of our `dev` stage is having a naming conflict with the table in our `prod` stage. In order to fix this we can take use parameters.

## Avoiding Namespace Conflicts with Parameters

Using parameters will allow us to deploy stage-specific tables. But we'll also want to set the names of those tables as environment variables so that our code can reference the table name from the environment variable instead of having to hard-code it in the function code.

### Updating serverless.yml

First, we probably want to remove our old service with `serverless remove`. That way we wont have that other table lingering around.

Next, we want to update a few parts of the `serverless.yml` file. I've left comments next to the added sections below:

```yaml
# Example node.js service code generated from running the `serverless` command

service: simple-ddb-table
app: simple-ddb-table-app
org: workshop

provider:
  name: aws
  runtime: nodejs10.x
  # These two new lines set an environment variable
  environment:
    DYNAMODB_TABLE: ${self:service}-${opt:stage, self:provider.stage}-someTable

functions:
  hello:
    handler: handler.hello

resources:
  Resources:
    someTable:
      Type: AWS::DynamoDB::Table
      Properties:
        # This next line now refers to the new value set in the provider section
        TableName: ${self:provider.environment.DYNAMODB_TABLE}
        AttributeDefinitions:
          - AttributeName: someKeyName
            AttributeType: S
        KeySchema:
          - AttributeName: someKeyName
            KeyType: HASH
        ProvisionedThroughput:
          ReadCapacityUnits: 1
          WriteCapacityUnits: 1
```

With the addition to the provider section, we will now always get a table unique to the stage. If we deploy the same serverless.yml file using `serverless deploy` and `serverless deploy --stage prod` we'll end up with two tables:

- In `dev` we will get `simple-ddb-table-dev-someTable`.
- In `prod` we get `simple-ddb-table-prod-someTable`.

Try it yourself using the deployment commands above and then check what tables appear in your AWS account. When you confirm that this is indeed working you can also try adding a parameterized IAM role!

## Scoping Permissions with Parameters

In order to scope permissions down extensively you can use the parameter in the IAM role statement for the service to make sure that a `dev` service can't act on a `prod` table or vice versa. Here's how:

In the provider section, add a section for the `iamRoleStatements` as shown below:

```yaml
provider:
  name: aws
  runtime: nodejs10.x
  environment:
    DYNAMODB_TABLE: ${self:service}-${opt:stage, self:provider.stage}-someTable
  iamRoleStatements:
    - Effect: Allow
      Action:
        - dynamodb:GetItem
        - dynamodb:PutItem
        - dynamodb:UpdateItem
      Resource: "*" # Generally, don't do this. We'll fix it below.
```

Now if we were lazy, we could add this permission to our entire service and give it permission to take the actions listed on any resource in our AWS account. But that's not best practice at all! We want to scope our permissions down much further. So instead of `"*"` we can use: `"arn:aws:dynamodb:${opt:region, self:provider.region}:*:table/${self:provider.environment.DYNAMODB_TABLE}"`.

Let's break down what this does:

- `arn:aws:dynamodb:` is the start of ARNs for all DynamoDB tables. The `:` character separates parts of the ARN.
- `${opt:region, self:provider.region}` will get the region from the `--region` flag and fallback to the `provider` region set in `serverless.yml`.
- `:*:` the colons are used to delineate parts of the arn, but the asterisk is a wildcard for _any_ AWS account, you could also change it to your account number but in this case it doesn't actually grant permissions to other folks' accounts because we don't have permissions to do that. 
- `table/` is the start of all DynamoDB table resources 
- `${self:provider.environment.DYNAMODB_TABLE}` is the table name defined in the provider environment section

Our final `provider` section should look like this:

```yaml
provider:
  name: aws
  runtime: nodejs10.x
  environment:
    DYNAMODB_TABLE: ${self:service}-${opt:stage, self:provider.stage}-someTable
  iamRoleStatements:
    - Effect: Allow
      Action:
        - dynamodb:GetItem
        - dynamodb:PutItem
        - dynamodb:UpdateItem
      Resource: "arn:aws:dynamodb:${opt:region, self:provider.region}:*:table/${self:provider.environment.DYNAMODB_TABLE}"
```

So essentially, it scopes our permissions narrowly to the particular stage, region, and table that we want to grant permissions on without being overly permissive.

## Quirks

There are a few quirks when deploying DynamoDB tables using CloudFormation (what the Serverless Framework translate your `serverless.yml` into). Here are some of the most common to look out for.

### Managing Multiple DynamoDB Index Changes

When deploying multiple table indexes you can only change one at a time.

This means that when provisioning a table with more than one global or local secondary index `serverless.yml` you can't add, remove, or edit more than one at a time. To solve this issue, you can add one index, redeploy the service, then add another. Or if you need to remove an index, you can remove a single index then redeploy, and remove or add another.

### Avoiding Naming Conflicts with resources you RETAIN

To help you avoid inadvertently deleting a bunch of production data when removing a service you can add the RETAIN property to DynamoDB in order to keep the table around even after running a command like `serverless remove`. If you do this, just be aware that you may run into naming conflicts when trying to redeploy the service. Essentially, because you keep the table around after removing the service, you have a table that causes a naming conflict for CloudFormation. 

If you get into this state you can backup your retained table, delete the table, deploy the service again and load the backup into the new, now empty, table created by the service.

## Previous - [Important DynamoDB vs. SQL Considerations](p1-important-dynamodb-vs-sql-considerations.md)
## Next - [DynamoDB Table Basics](p3-table-basics.md)
