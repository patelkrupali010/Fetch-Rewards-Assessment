# FETCH REWARDS - PII Masking Assessment

## Decisions made to develop my solution:
<b> 1. How will you read messages from the queue?</b>
<br />In my solution, I’m using the AWS CLI (awslocal) to interact with the local SQS queue by running a python subprocess.

<b> 2. What type of data structures should be used?</b>
<br />I have used dictionaries (Python dictionaries) to represent and manipulate the JSON data from the queue. This is a reasonable choice, as dictionaries provide a flexible way to work with structured data. In a more complex system, I might also consider using object-relational mapping (ORM) libraries to work with database records in a more object-oriented manner.

<b> 3. How will you mask the PII data so that duplicate values can be identified?</b>
<br />My approach of using a consistent hashing algorithm (SHA-256) to mask the PII data is a suitable method for masking sensitive information while still allowing for duplicate identification.

<b> 4. What will be your strategy for connecting and writing to Postgres?</b>
<br />I am using ‘psycopg2’ library in python to connect to Postgres and write data into Postgres. This library allows you to establish a connection to the database, execute SQL queries, and manage transactions.

## Questions:
<b> 1. How would you deploy this application in production?</b>
<br />For production environment, I would have typically deployed the application in a containerized orchestration platform like Kubernetes to ensure scalability and high availability. <br />The steps taken:
 - Packaged my application and its dependencies into Docker containers
 - Kubernetes to manage and deploy docker containers
 - AWS SQS queue for messaging system
 - Launch an RDS instance to create Postgres database
 - Apache Spark for distributed data processing and add transformation logic python code
 - Apache Airflow to orchestrate the ETL pipeline
 - Monitoring can be implemented to track health and performance of the application. AWS CloudWatch, Grafana can be used.


<b> 2. What other components would you want to add to make this production ready?</b><br />
 - Error handling and recovery: Robust error handling to handle failures in message processing or database operations.
 - Run Pytests for testing the desired behavior of the application
 - Monitoring: track health and performance of application
 - Configuration management: No code level config changes required
 - Documentation of process, architectural decisions, setup and installations 
 - Version Control: Git actions and hooks can be implemented for smooth deployments and review


<b> 3. How can this application scale with a growing dataset?</b>
 - Enabling auto-scaling rules in the orchestration platform to increase/ decrease the containers
 - Load balancing to distribute incoming messages across multiple processing instances.
 - Caching mechanism to reduce the load on the database for frequently accessed data
 - Amazon RDS (postgres) for autoscaling capabilities
 - Apache Spark for parallel distribution capabilities while processing the data
 - Database sharding

<b> 4. How can PII be recovered later on?</b>
 - My approach involves utilizing hashed representations of PII (Personally Identifiable Information) as a reference point and verifying it against the original data that underwent hashing. This verification process entails applying the same hash function to the initial data and comparing the resulting output to the stored hashed value. When there's a match between the two values, it suggests that the original data was likely used to generate the hash.

 - We can also use a Key Management System to encrypt and decrypt the PII data. Only authorized personnel should have access to the decryption keys, and strict access controls should be in place.

<b> 5. What are the assumptions you made?</b><br />
I would clarify the requirements by collaborating with different team members and stakeholders, but in this case, I made a few assumptions:
 - There’s an issue with the table schema given in the problem statement since app_version field is a varchar value and if converted to integer like mentioned in the schema structure, data will be inaccurate.
 - SQS messages to be deleted once read to avoid records being loaded multiple times into postgres.
 - SQS messages may not be in the same format throughout and if the message body does not contain all fields, write into error_tables in postgres
 - “Messages” will always be there in response body on running “receive-message” query.
 - No AWS credentials are required as we are given localstack setup and If we’re using localstack (awslocal), we don’t need aws credentials (AWS access key id and token)

## Project Setup

1. Install Docker desktop it has Docker Compose Inbuilt.

```https://docs.docker.com/get-docker/```

2. Install Postgress psql

```https://www.postgresql.org/download/```

## Steps to run the code

1. Clone this repo in CLI
```git clone https://github.com/patelkrupali010/Fetch-Rewards-Assessment.git```

2. go to cloned repo.
```bash
cd Fetch-Rewards-Assessment
```
3. run docker compose

```bash
docker-compose up -d
```
![image](https://github.com/patelkrupali010/Fetch-Rewards-Assessment/assets/91221231/9d13c91b-4e7d-49b3-8141-a507e480e318)

![image](https://github.com/patelkrupali010/Fetch-Rewards-Assessment/assets/91221231/f57355a0-9d71-4907-a88f-7054292f2d0c)



 
 

## Testing the result:
Postgres:
* If you have installed postgres correctly on your system, go to your cmd and type following:  

 ```bash
psql -d postgres -U postgres -p 5432 -h localhost -W 
```

 ```bash
 select * from user_logins;
```

* If <b>NOT</b>,
   - go to docker "postgres" container
   - goto terminal
   - connect to postgres database using the above (i) command
   - run select query to see the records.

## Error Handling
I have handled the errors while reading from SQS into error_records

Example: Out of 100 messages in SQS, 1 message contains “{"bar": "123", "foo": "oops_wrong_msg_type"}” in the body instead of the fields present in the schema structure.

![image](https://github.com/patelkrupali010/Fetch-Rewards-Assessment/assets/91221231/d5d12abe-a1ee-4141-a796-3663d8c00179)

 

Docker Container (Postgres + localstack + app)

![image](https://github.com/patelkrupali010/Fetch-Rewards-Assessment/assets/91221231/0e466c55-74f7-485d-b1f0-aab7932d6db4)

Connect to postgres:

![image](https://github.com/patelkrupali010/Fetch-Rewards-Assessment/assets/91221231/8275740b-5e48-4c3e-b958-cb050efdddfd)

 
List of tables in postgres db along with table count:

![image](https://github.com/patelkrupali010/Fetch-Rewards-Assessment/assets/91221231/4b8a5a39-1abc-4a41-a16b-dd0933e34e0c)

 

Output:

![image](https://github.com/patelkrupali010/Fetch-Rewards-Assessment/assets/91221231/d040b2c7-e601-4f47-8a26-6062a03d5beb)

 

App Container logs:

![image](https://github.com/patelkrupali010/Fetch-Rewards-Assessment/assets/91221231/c7b54ab3-9b24-4553-b423-e75198b3b707)



