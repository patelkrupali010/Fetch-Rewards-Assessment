from datetime import datetime
import json
import psycopg2
import subprocess
import hashlib
import logging


# Constants
SQS_QUEUE_URL = "http://localstack:4566/000000000000/login-queue"
DB_CONNECTION_STRING = "dbname=postgres user=postgres password=postgres host=postgres port=5432"
MASKED_FIELD_LENGTH = 256

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

conn = psycopg2.connect(DB_CONNECTION_STRING)
cursor = conn.cursor()



def mask_field(value):
    """Mask PII data using consistent hashing algorithm - duplicate values handled"""
    encoded_value = hashlib.sha256(value.encode()).hexdigest()
    return encoded_value

def insert_data_into_postgres(data):
    """
    Insert data into the PostgreSQL database.
    
    Args:
        data (dict): Data to be inserted.
    """
    try:
        # Insert data into the user_logins table
        insert_query = """
        INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
        VALUES (%(user_id)s, %(device_type)s, %(masked_ip)s, %(masked_device_id)s, %(locale)s, %(app_version)s, %(create_date)s)
        """
        cursor.execute(insert_query, data)
        
        conn.commit()
        
        logger.info("Data inserted successfully.")  

    except Exception as e:
        logger.error(f"Error inserting data into PostgreSQL: {str(e)}")


def process_message(message):
    """
    Process a message from SQS, mask PII fields, and insert into PostgreSQL database.
    
    Args:
        message (dict): JSON message from SQS.
    """
    try:
        # Parse the JSON message from SQS
        data = json.loads(message["Body"])

        
        # Mask PII fields
        data["masked_ip"] = mask_field(data["ip"])
        data["masked_device_id"] = mask_field(data["device_id"])
        
        # Flatten the data for insertion
        flattened_data = {
            "user_id": data["user_id"],
            "device_type": data["device_type"],
            "masked_ip": data["masked_ip"],
            "masked_device_id": data["masked_device_id"],
            "locale": data["locale"],
            "app_version": data["app_version"],
            "create_date": datetime.now()
        }


        # Insert data into PostgreSQL database
        insert_data_into_postgres(flattened_data)

    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")

        # Log the error record to the error table
        error_message = str(e)
        
        # Create an error table
        create_error_table_query = """
        CREATE TABLE IF NOT EXISTS error_records (
        error_id serial PRIMARY KEY,
        error_message text,
        message jsonb,
        message_body jsonb
        );
        """
        cursor.execute(create_error_table_query)

        cursor.execute("INSERT INTO error_records (error_message, message, message_body) VALUES (%s, %s, %s)",
                       (error_message, json.dumps(message) ,json.dumps(data)))  
        
        conn.commit()
        logger.info("Error message logged successfully.")



def main():
    # Initialize SQS client

    # alter table schema to fix the app_version datatype
    alter_query = """
    alter table public.user_logins alter column app_version type varchar(10)
    """
    cursor.execute(alter_query)

    

    # Continuously poll SQS for messages
    while True:

        # Get the approximate number of messages in the queue
        max_no_of_messages_response = subprocess.run(['awslocal', "--endpoint-url=http://localstack:4566", 'sqs', 'get-queue-attributes', '--queue-url',
                                   SQS_QUEUE_URL, "--attribute-names", "ApproximateNumberOfMessages"], capture_output=True)


        max_no_of_messages = json.loads(max_no_of_messages_response.stdout)['Attributes']['ApproximateNumberOfMessages']
      
        logger.info(f"Number of messages in the queue: {max_no_of_messages}")
        

        # Check if there are messages to process
        if  max_no_of_messages != "0":
            logger.info("No messages to process. Exiting.")

            response = subprocess.run(['awslocal', "--endpoint-url=http://localstack:4566", 'sqs', 'receive-message', '--queue-url',
                            SQS_QUEUE_URL], capture_output=True)
            
            # Extract the message body
            response_body = json.loads(response.stdout)
            if "Messages" in response_body:
                for message in response_body["Messages"]:
                    process_message(message)     
                    
                    # Remove the processed message from the queue to avoid continuous polling and avoid duplicacy.
                    subprocess.run(['awslocal', "--endpoint-url=http://localstack:4566", 'sqs', 'delete-message', '--queue-url', SQS_QUEUE_URL, '--receipt-handle',message["ReceiptHandle"]], capture_output=True, text=True)

                    logger.info("Message deleted successfully.")
          

        else:
          cursor.close()
          conn.close()
          break
 



if __name__ == "__main__":
    main()
