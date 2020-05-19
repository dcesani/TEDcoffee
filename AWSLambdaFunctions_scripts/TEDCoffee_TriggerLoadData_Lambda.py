# Set up logging
import json
import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Import Boto 3 for AWS Glue libreria che permette di collegarsi ad AWS
import boto3
client = boto3.client('glue')

# Variables for the job: 
glueJobName = "TEDCoffee_LoadData"
#DOBBIAMO DARE IL PERMESSO ALLA FUNCTION
# Define Lambda function
def lambda_handler(event, context): #questo è effettivamente quello che parte

    response = client.start_job_run(JobName = glueJobName)
    logger.info('## STARTED GLUE JOB: ' + glueJobName)
    logger.info('## GLUE JOB RUN ID: ' + response['JobRunId'])
    return response
    