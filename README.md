<!-- # FETCH REWARDS - PII Masking Assessment

## Decisions made to develop my solution:
● How will you read messages from the queue?
In my solution, I’m using the AWS CLI (awslocal) to interact with the local SQS queue by running a python subprocess.

● What type of data structures should be used?
I have used dictionaries (Python dictionaries) to represent and manipulate the JSON data from the queue. This is a reasonable choice, as dictionaries provide a flexible way to work with structured data. In a more complex system, I might also consider using object-relational mapping (ORM) libraries to work with database records in a more object-oriented manner.

● How will you mask the PII data so that duplicate values can be identified?
My approach of using a consistent hashing algorithm (SHA-256) to mask the PII data is a suitable method for masking sensitive information while still allowing for duplicate identification.

● What will be your strategy for connecting and writing to Postgres?
I am using ‘psycopg2’ library in python to connect to Postgres and write data into Postgres. This library allows you to establish a connection to the database, execute SQL queries, and manage transactions.

## Questions:
● How would you deploy this application in production?
For production environment, I would have typically deployed the application in a containerized orchestration platform like Kubernetes to ensure scalability and high availability. The steps taken:
o	Packaged my application and its dependencies into Docker containers
o	Kubernetes to manage and deploy docker containers
o	AWS SQS queue for messaging system
o	Launch an RDS instance to create Postgres database
o	Apache Spark for distributed data processing and add transformation logic python code
o	Apache Airflow to orchestrate the ETL pipeline
o	Monitoring can be implemented to track health and performance of the application. AWS CloudWatch, Grafana can be used.
o	
● What other components would you want to add to make this production ready?
o	Error handling and recovery: Robust error handling to handle failures in message processing or database operations.
o	Run Pytests for testing the desired behavior of application
o	Monitoring: track health and performance of application
o	Configuration management: No code level config changes required
o	Documentation of process, architectural decisions, setup and installations 
o	Version Control: Git actions and hooks can be implemented for smooth deployments and review


● How can this application scale with a growing dataset.
o	Enabling auto-scaling rules in orchestration platform to increase/ decrease the containers
o	Load balancing to distribute incoming messages across multiple processing instances.
o	Caching mechanism to reduce the load on the database for frequently accessed data
o	Amazon RDS (postgres) for autoscaling capabilities
o	Apache Spark for parallel distribution capabilities while processing the data
o	Database sharding
● How can PII be recovered later on?
My approach involves utilizing hashed representations of PII (Personally Identifiable Information) as a reference point and verifying it against the original data that underwent hashing. This verification process entails applying the same hash function to the initial data and comparing the resulting output to the stored hashed value. When there's a match between the two values, it suggests that the original data was likely used to generate the hash.

We can also use a Key Management System to encrypt and decrypt the PII data. Only authorized personnel should have access to the decryption keys, and strict access controls should be in place.

● What are the assumptions you made?
I would clarify the requirements by collaborating with different team members and stakeholders, but in this case, I made a few assumptions:
1.	There’s an issue with the table schema given in the problem statement since app_version field is a varchar value and if converted to integer like mentioned in the schema structure, data will be inaccurate.
2.	SQS messages to be deleted once read to avoid records being loaded multiple times into postgres.
3.	SQS messages may not be in the same format throughout and if the message body does not contain all fields, write into error_tables in postgres
4.	“Messages” will always be there in response body on running “receive-message” query.
5.	No AWS credentials are required as we are given localstack setup and If we’re using localstack (awslocal), we don’t need aws credentials (AWS access key id and token)

## Project Setup

1. Install Docker desktop it has Docker Compose Inbuilt.

```https://docs.docker.com/get-docker/```

2. Install Postgress psql

```https://www.postgresql.org/download/```

## Steps to run the code

1. Clone this repo in CLI
```git clone https://github.com/ ```

2. go to cloned repo.
```bash
cd fetch-pii_masking
```
3. run docker compose

```bash
docker-compose up -d
```

 
 

>	Testing the result:
>	Postgres:
If you have installed postgres correctly on your system, go to your cmd and type following:
Connect to the Postgres database, verify the table is created
i. psql -d postgres -U postgres -p 5432 -h localhost -W
ii. postgres=# select * from user_logins;

if not, go to docker "postgres" container -> goto terminal and connect to postgres database using the above (i) command and then run select query to see the records.

Error_records -> this table is additionally added by python script to record any errors while reading data from SQS.
Example: Out of 100 messages in SQS, 1 message contains “{"bar": "123", "foo": "oops_wrong_msg_type"}” in the body instead of the fields present in schema structure.
 



Docker Container (Postgres + localstack + app)

 


Connect to postgres:
 

List of tables in postgres db along with table count:

 


Output:
 

App Container logs:
 


