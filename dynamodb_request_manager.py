import boto3
from ast import literal_eval
from botocore.exceptions import ClientError
from constants import CACHE_TABLE_NAME, QUERY_CACHE_NAME


class DydbRequestManager:
    
    def __init__(self, aws_access_key, aws_secret_key, region='us-east-2'):
        self.client = boto3.client(
                        'dynamodb',
                        aws_access_key_id=aws_access_key, 
                        aws_secret_access_key=aws_secret_key, 
                        region_name=region
                    )
        self.clear_cache()
        
    def load_table_key_mapping(self, objects, key):
        return self.client.batch_write_item(RequestItems=generate_cache_table_request(objects, key))

    def load_query_cache(self, key, messages):
        response = self.client.put_item(
            Item={
                'request_key': {
                    'S' : key
                    },
                'message' : {
                    'S' : str(messages)
                    }
            },
            TableName=QUERY_CACHE_NAME,
        )     
        return response
    
    def retrieve_from_query_cache(self, key):
        response = self.client.get_item(
            TableName=QUERY_CACHE_NAME,
            Key={"request_key":{
                'S' : key
                },
            },
            AttributesToGet=["message"]
        )
        return literal_eval(response["Item"]["message"]["S"])

    def clear_cache(self):
        self.rebuild_object_key_table()
        self.rebuild_query_cache_table()
        
    def rebuild_object_key_table(self):
        try:
            self.client.delete_table(TableName=CACHE_TABLE_NAME)
            waiter = self.client.get_waiter('table_not_exists')
            waiter.wait(TableName=CACHE_TABLE_NAME)
        except ClientError:
            pass
        response = self.client.create_table(
            TableName=CACHE_TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'object',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'cache_key',
                    'KeyType': 'RANGE'
                },
            ],
            AttributeDefinitions= [
                {
                    'AttributeName': 'cache_key',
                    'AttributeType': 'S'
                },
                  {
                    'AttributeName': 'object',
                    'AttributeType': 'S'
                },
                
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 2,
                'WriteCapacityUnits': 2
            }
        )
        return response

    def rebuild_query_cache_table(self):
        try:
            self.client.delete_table(TableName=QUERY_CACHE_NAME)
            waiter = self.client.get_waiter('table_not_exists')
            waiter.wait(TableName=QUERY_CACHE_NAME)
        except ClientError:
            pass
        response = self.client.create_table(
            TableName=QUERY_CACHE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'request_key',
                    'KeyType': 'HASH'
                },
                #   {
                #     'AttributeName': 'message',
                #     'KeyType': 'RANGE'
                # },
            ],
            AttributeDefinitions= [
                {
                    'AttributeName': 'request_key',
                    'AttributeType': 'S'
                },
                #   {
                #     'AttributeName': 'message',
                #     'AttributeType': 'S'
                # },
                
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 2,
                'WriteCapacityUnits': 2
            }
        )
        return response
    


def cache_batch_template(obj, cache_key):
    return {'PutRequest': {'Item': {'object': {'S': obj,},'cache_key': {'S': cache_key,}}}}

def generate_cache_table_request(objects, key):
    put_requests = [cache_batch_template(obj, key)
                    for obj in objects
                    ]
    return {CACHE_TABLE_NAME: put_requests}


            
